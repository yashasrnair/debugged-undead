from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime
import ast
import traceback
from .extensions import db
from .models import Survivor, Challenge
from .debug_generator import DebugGenerator

main = Blueprint('main', __name__)
debug_gen = DebugGenerator()

def execute_code_and_capture_output(code_string):
    """
    Execute code and capture the output variables and print statements
    Returns: (success, result_dict, output_text, error_message)
    """
    # Safe execution environment with built-in exceptions and math module
    import math
    
    safe_globals = {
        '__builtins__': {
            'print': print,
            'range': range,
            'len': len,
            'str': str,
            'int': int,
            'float': float,
            'bool': bool,
            'list': list,
            'dict': dict,
            'set': set,
            'tuple': tuple,
            'sum': sum,
            'max': max,
            'min': min,
            'abs': abs,
            'round': round,
            'sorted': sorted,
            'enumerate': enumerate,
            'chr': chr,             
            'ord': ord,
            # Add built-in exceptions
            'ValueError': ValueError,
            'TypeError': TypeError,
            'IndexError': IndexError,
            'KeyError': KeyError,
            'AttributeError': AttributeError,
            'SyntaxError': SyntaxError,
            'NameError': NameError,
            'ZeroDivisionError': ZeroDivisionError,
            'Exception': Exception,
        },
        # Add math module directly
        'math': math
    }
    safe_locals = {}
    
    # Capture print output
    output_lines = []
    
    def captured_print(*args, **kwargs):
        output_lines.append(' '.join(str(arg) for arg in args))
        # Also call the real print for debugging
        print(*args, **kwargs)
    
    safe_globals['print'] = captured_print
    
    try:
        # Remove import statements since we're providing math directly
        cleaned_code = code_string
        if 'import math' in cleaned_code:
            cleaned_code = cleaned_code.replace('import math', '').strip()
        
        # Execute the code
        exec(cleaned_code, safe_globals, safe_locals)
        
        # Return all local variables and captured output
        return True, safe_locals, '\n'.join(output_lines), None
        
    except Exception as e:
        return False, None, '\n'.join(output_lines), str(e)

def compare_outputs(user_output, expected_output, tolerance=0.001):
    """
    Compare two outputs with tolerance for floating point numbers
    """
    # Handle string comparisons
    if isinstance(expected_output, str) and isinstance(user_output, str):
        return user_output == expected_output
    
    # Handle None values
    if user_output is None or expected_output is None:
        return user_output == expected_output
    
    if type(user_output) != type(expected_output):
        return False
    
    if isinstance(user_output, (int, float)) and isinstance(expected_output, (int, float)):
        return abs(user_output - expected_output) < tolerance
    
    elif isinstance(user_output, tuple) and isinstance(expected_output, tuple):
        if len(user_output) != len(expected_output):
            return False
        return all(compare_outputs(u, e, tolerance) for u, e in zip(user_output, expected_output))
    
    elif isinstance(user_output, list) and isinstance(expected_output, list):
        if len(user_output) != len(expected_output):
            return False
        return all(compare_outputs(u, e, tolerance) for u, e in zip(user_output, expected_output))
    
    elif isinstance(user_output, dict) and isinstance(expected_output, dict):
        if set(user_output.keys()) != set(expected_output.keys()):
            return False
        return all(compare_outputs(user_output[k], expected_output[k], tolerance) for k in user_output.keys())
    
    else:
        return user_output == expected_output

def validate_by_execution(user_code, solution_code, expected_output_str):
    """
    Validate by executing both user code and solution code, then comparing outputs
    """
    try:
        # For string outputs, we don't need to eval them
        if expected_output_str.startswith('"') or expected_output_str.startswith("'"):
            expected_output = expected_output_str.strip('"\'')
        else:
            # Try to evaluate other types (numbers, tuples, lists, etc.)
            try:
                expected_output = eval(expected_output_str)
            except:
                expected_output = expected_output_str
        
        # Execute user's code
        user_success, user_locals, user_print, user_error = execute_code_and_capture_output(user_code)
        
        if not user_success:
            return False, f"Execution error: {user_error}"
        
        # Execute solution code
        solution_success, solution_locals, solution_print, solution_error = execute_code_and_capture_output(solution_code)
        
        if not solution_success:
            return False, f"Solution code error: {solution_error}"
        
        # Check print output first (most common case)
        user_print_clean = user_print.strip()
        if user_print_clean == str(expected_output):
            return True, f"Success! Output matches: {user_print_clean}"
        
        # Look for common output variables
        output_variables = ['result', 'output', 'final_result', 'answer', 'message']
        
        for var_name in output_variables:
            if var_name in user_locals:
                user_result = user_locals[var_name]
                
                # Handle string comparison
                if compare_outputs(user_result, expected_output):
                    return True, f"Success! {var_name} matches: {user_result}"
        
        # Check if any variable matches the expected output
        for var_name, var_value in user_locals.items():
            if compare_outputs(var_value, expected_output):
                return True, f"Success! {var_name} matches: {var_value}"
        
        # Check if the print output from solution matches
        solution_print_clean = solution_print.strip()
        if user_print_clean == solution_print_clean:
            return True, f"Success! Output matches: {user_print_clean}"
        
        return False, f"No matching output found. Expected: {expected_output}, Got print: {user_print_clean}"
        
    except Exception as e:
        return False, f"Validation error: {str(e)}"

def validate_code_structure(user_code, expected_solution):
    """
    Compare code structure for syntax challenges
    """
    try:
        def normalize(code):
            lines = []
            for line in code.split('\n'):
                if '#' in line:
                    line = line.split('#')[0]
                line = line.strip()
                if line:
                    lines.append(line)
            return '\n'.join(lines)
        
        user_normalized = normalize(user_code)
        solution_normalized = normalize(expected_solution)
        
        return user_normalized == solution_normalized, "Code structure matches solution!"
        
    except Exception as e:
        return False, f"Validation error: {str(e)}"

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
        
        challenges_data = debug_gen.generate_all_challenges()
        for level, data in challenges_data.items():
            challenge = Challenge(
                level=level,
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
        
        # Debug output
        print(f"=== Validating Level {level} ===")
        print(f"User code:\n{user_code}")
        print(f"Expected output: {challenge.expected_output}")
        
        # Use appropriate validation method
        if challenge.error_type == "syntax":
            is_valid, message = validate_code_structure(user_code, challenge.solution)
        else:
            is_valid, message = validate_by_execution(user_code, challenge.solution, challenge.expected_output)
        
        print(f"Validation result: {is_valid}, Message: {message}")
        
        if is_valid:
            challenge.is_solved = True
            challenge.end_time = datetime.utcnow()  # Record level completion time
            db.session.commit()
            
            # Check if all challenges are solved
            unsolved = Challenge.query.filter_by(survivor_id=survivor.id, is_solved=False).count()
            
            if unsolved == 0:
                survivor.end_time = datetime.utcnow()
                db.session.commit()
                flash('All systems restored! The cure has been synthesized!', 'correct')
                return redirect(url_for('main.finished'))
            else:
                flash(message, 'correct')
        else:
            flash(message, 'incorrect')
        
        return redirect(url_for('main.challenge', level=level))
    
    all_challenges = Challenge.query.filter_by(survivor_id=survivor.id).order_by(Challenge.level).all()
    
    return render_template('challenge.html', 
                          challenge=challenge, 
                          all_challenges=all_challenges,
                          survivor=survivor)

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
    
    solved_count = sum(1 for challenge in challenges if challenge.is_solved)
    
    return render_template('level_select.html', 
                         challenges=challenges, 
                         survivor=survivor,
                         solved_count=solved_count)

@main.route('/finished')
def finished():
    if 'survivor_id' not in session:
        return redirect(url_for('main.entry'))
    
    survivor = Survivor.query.get(session['survivor_id'])
    
    if survivor is None:
        session.pop('survivor_id', None)
        flash('Session expired. Please log in again.', 'info')
        return redirect(url_for('main.entry'))
    
    if not survivor.end_time:
        return redirect(url_for('main.level_select'))
    
    return render_template('finished.html', survivor=survivor)

@main.route('/leaderboard')
def leaderboard():
    # Get survivors who have completed all challenges
    completed_survivors = []
    survivors = Survivor.query.filter(Survivor.end_time.isnot(None)).all()
    
    for survivor in survivors:
        challenges = Challenge.query.filter_by(survivor_id=survivor.id).order_by(Challenge.level).all()
        
        # Check if all challenges are solved
        if all(challenge.is_solved for challenge in challenges):
            level_times = {}
            for challenge in challenges:
                if challenge.end_time and challenge.start_time:
                    level_time = (challenge.end_time - challenge.start_time).total_seconds()
                    level_times[challenge.level] = round(level_time, 2)
            
            total_time = (survivor.end_time - survivor.start_time).total_seconds()
            
            completed_survivors.append({
                'survivor': survivor,
                'total_time': total_time,
                'level_times': level_times,
                'completion_time': survivor.get_completion_time()
            })
    
    # Sort by total time (ascending - faster is better)
    completed_survivors.sort(key=lambda x: x['total_time'])
    
    return render_template('leaderboard.html', survivors=completed_survivors)
@main.route('/logout')
def logout():
    session.pop('survivor_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.entry'))