# zombie_code_survival/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime
import os
import tempfile
import subprocess
import sys
from .extensions import db
from .models import Survivor, Challenge
from .debug_generator import DebugGenerator

main = Blueprint('main', __name__)
debug_gen = DebugGenerator()

# Detect platform: resource is POSIX-only
POSIX = True
try:
    import resource
except Exception:
    POSIX = False

# Resource-limiting function only available/used on POSIX systems
def _limit_resources():
    """
    This function will be used as preexec_fn on POSIX systems to limit CPU/memory for executed binaries.
    On Windows this will not be used.
    """
    if not POSIX:
        return
    # CPU time (seconds)
    resource.setrlimit(resource.RLIMIT_CPU, (2, 2))
    # Address space limit (200 MB)
    resource.setrlimit(resource.RLIMIT_AS, (200 * 1024 * 1024, 200 * 1024 * 1024))
    # Limit number of processes spawned by the child
    try:
        resource.setrlimit(resource.RLIMIT_NPROC, (20, 20))
    except Exception:
        # Some systems may restrict RLIMIT_NPROC; ignore if not available
        pass
    # Limit file size the child can create (10MB)
    try:
        resource.setrlimit(resource.RLIMIT_FSIZE, (10 * 1024 * 1024, 10 * 1024 * 1024))
    except Exception:
        pass

def compile_and_run_cpp(code_str, stdin_data=None, compile_timeout=5, run_timeout=2):
    """
    Compile provided C++ code using g++ and run the produced binary.
    On POSIX systems this uses preexec_fn=_limit_resources to limit child resources.
    On Windows, preexec_fn isn't used (not supported) and resource limits are not enforced here.
    Returns a dict: { success: bool, phase: 'compile'|'run', stdout: str, stderr: str }
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        cpp_path = os.path.join(tmpdir, "submission.cpp")
        exe_path = os.path.join(tmpdir, "submission")
        if sys.platform.startswith("win"):
            # On Windows provide .exe extension for binary name
            exe_path = os.path.join(tmpdir, "submission.exe")

        with open(cpp_path, "w", encoding="utf-8") as f:
            f.write(code_str)

        # Compile
        compile_cmd = ["g++", "-std=c++17", cpp_path, "-O2", "-o", exe_path]
        try:
            comp = subprocess.run(compile_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=compile_timeout, text=True)
            if comp.returncode != 0:
                return {'success': False, 'phase': 'compile', 'stdout': comp.stdout or "", 'stderr': comp.stderr or ""}
        except subprocess.TimeoutExpired:
            return {'success': False, 'phase': 'compile', 'stdout': '', 'stderr': 'Compilation timed out.'}
        except FileNotFoundError as e:
            # g++ not installed or not in PATH
            return {'success': False, 'phase': 'compile', 'stdout': '', 'stderr': f'g++ not found: {e}'}

        # Run the executable
        try:
            if POSIX:
                run_proc = subprocess.run([exe_path], input=(stdin_data or ""), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=run_timeout, text=True, preexec_fn=_limit_resources)
            else:
                # Windows: preexec_fn not available; don't pass it.
                run_proc = subprocess.run([exe_path], input=(stdin_data or ""), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=run_timeout, text=True)
            return {'success': run_proc.returncode == 0, 'phase': 'run', 'stdout': run_proc.stdout or "", 'stderr': run_proc.stderr or ""}
        except subprocess.TimeoutExpired:
            return {'success': False, 'phase': 'run', 'stdout': '', 'stderr': 'Execution timed out.'}
        except FileNotFoundError as e:
            return {'success': False, 'phase': 'run', 'stdout': '', 'stderr': f'Executable not found or permission error: {e}'}
        except Exception as e:
            return {'success': False, 'phase': 'run', 'stdout': '', 'stderr': f'Execution failed: {e}'}

@main.route('/', methods=['GET', 'POST'])
def entry():
    if request.method == 'POST':
        username = request.form.get('username')
        if not username:
            flash('Please enter a survivor name', 'info')
            return render_template('entry.html')
        survivor = Survivor.query.filter_by(username=username).first()
        if survivor:
            if not survivor.end_time:
                session['survivor_id'] = survivor.id
                return redirect(url_for('main.briefing'))
            else:
                flash('This survivor has already completed the mission.', 'info')
                return render_template('entry.html')

        survivor = Survivor(username=username)
        db.session.add(survivor)
        db.session.commit()

        # Seed C++ challenges
        challenges_data = debug_gen.generate_all_challenges()
        for level, data in challenges_data.items():
            challenge = Challenge(
                level=level,
                title=data.title,
                buggy_code=data.buggy_code,
                solution=data.solution,
                error_type=data.error_type,
                expected_output=str(data.expected_output),
                survivor_id=survivor.id
            )
            db.session.add(challenge)
        db.session.commit()
        session['survivor_id'] = survivor.id
        return redirect(url_for('main.briefing'))

    return render_template('entry.html')

@main.route('/briefing')
def briefing():
    if 'survivor_id' not in session:
        return redirect(url_for('main.entry'))
    survivor = Survivor.query.get(session['survivor_id'])
    return render_template('briefing.html', survivor=survivor)

@main.route('/level-select')
def level_select():
    if 'survivor_id' not in session:
        return redirect(url_for('main.entry'))
    survivor = Survivor.query.get(session['survivor_id'])
    if survivor is None:
        session.pop('survivor_id', None)
        flash('Session expired. Please log in again.', 'info')
        return redirect(url_for('main.entry'))
    challenges = Challenge.query.filter_by(survivor_id=survivor.id).order_by(Challenge.level).all()
    solved_count = Challenge.query.filter_by(survivor_id=survivor.id, is_solved=True).count()
    return render_template('level_select.html', challenges=challenges, solved_count=solved_count, survivor=survivor)

@main.route('/challenge/<int:level>', methods=['GET', 'POST'])
def challenge(level):
    if 'survivor_id' not in session:
        return redirect(url_for('main.entry'))
    survivor = Survivor.query.get(session['survivor_id'])
    if survivor is None:
        session.pop('survivor_id', None)
        flash('Session expired. Please log in again.', 'info')
        return redirect(url_for('main.entry'))
    challenge = Challenge.query.filter_by(survivor_id=survivor.id, level=level).first()
    if not challenge:
        flash('Invalid challenge level', 'info')
        return redirect(url_for('main.level_select'))

    if request.method == 'POST':
        user_code = request.form.get('code', '')
        stdin_data = request.form.get('stdin', '')

        # Compile & run C++ code
        result = compile_and_run_cpp(user_code, stdin_data=stdin_data)

        # Save last outputs to session for display
        session['last_run_phase'] = result.get('phase')
        session['last_run_stdout'] = result.get('stdout', '')
        session['last_run_stderr'] = result.get('stderr', '')

        if result['phase'] == 'compile' and not result['success']:
            flash('Compilation error. See compiler output below.', 'incorrect')
        elif result['phase'] == 'run' and not result['success']:
            flash('Runtime error or non-zero exit. See stderr below.', 'incorrect')
        else:
            # Successful run, compare output to expected_output (exact match after strip)
            expected = (challenge.expected_output or "").strip()
            got = (result.get('stdout') or "").strip()
            if expected and got == expected:
                challenge.is_solved = True
                challenge.end_time = datetime.utcnow()
                db.session.commit()

                unsolved = Challenge.query.filter_by(survivor_id=survivor.id, is_solved=False).count()
                if unsolved == 0:
                    survivor.end_time = datetime.utcnow()
                    db.session.commit()
                    flash('All systems restored! The cure has been synthesized!', 'correct')
                    return redirect(url_for('main.finished'))
                else:
                    flash('Correct! Level solved.', 'correct')
            else:
                if expected:
                    flash(f'Output mismatch. Expected: \"{expected}\", Got: \"{got}\"', 'incorrect')
                else:
                    flash('Run completed. No expected output configured for this level.', 'info')

        return redirect(url_for('main.challenge', level=level))

    all_challenges = Challenge.query.filter_by(survivor_id=survivor.id).order_by(Challenge.level).all()
    return render_template('challenge.html', challenge=challenge, all_challenges=all_challenges, survivor=survivor)

@main.route('/finished')
def finished():
    if 'survivor_id' not in session:
        return redirect(url_for('main.entry'))
    survivor = Survivor.query.get(session['survivor_id'])
    return render_template('finished.html', survivor=survivor)


@main.route('/logout')
def logout():
    """
    Clear the current survivor session so the user can 'switch identity'
    (matching the [SWITCH IDENTITY] link in base.html).
    """
    session.pop('survivor_id', None)
    flash('Switched identity. Please enter a new survivor name.', 'info')
    return redirect(url_for('main.entry'))


@main.route('/leaderboard')
def leaderboard():
    # Simple leaderboard: survivors who finished sorted by completion time
    survivors = Survivor.query.filter(Survivor.end_time.isnot(None)).all()
    # compute completion seconds and sort
    def comp_time(s):
        delta = s.end_time - s.start_time
        return delta.total_seconds()
    survivors = sorted(survivors, key=comp_time)
    # Build helper structure like before
    survivors_data = []
    for s in survivors:
        level_times = {}
        for c in s.challenges.order_by(Challenge.level).all():
            if c.end_time and c.start_time:
                level_times[c.level] = int((c.end_time - c.start_time).total_seconds())
        survivors_data.append({'survivor': s, 'completion_time': s.get_completion_time(), 'level_times': level_times})
    return render_template('leaderboard.html', survivors=survivors_data)
