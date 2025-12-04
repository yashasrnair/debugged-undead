# zombie_code_survival/debug_generator.py
import textwrap
from dataclasses import dataclass
from typing import Dict

@dataclass
class ChallengeData:
    buggy_code: str
    solution: str
    error_type: str
    expected_output: str
    title: str

class DebugGenerator:
    """
    Produces 20 C++ debugging challenges.
    Each ChallengeData.expected_output is the exact stdout the correct program should produce.
    If a challenge requires stdin for testing, the expected_output includes a note of the stdin value to use.
    """

    def generate_1_missing_semicolon(self):
        buggy_code = textwrap.dedent(r'''
            #include <iostream>
            using namespace std;

            int main() {
                cout << "Survivors: ";
                int s
                cin >> s;
                cout << "Survivors: " << s << endl;
                return 0;
            }
        ''')
        solution = textwrap.dedent(r'''
            #include <iostream>
            using namespace std;

            int main() {
                cout << "Survivors: ";
                int s;
                cin >> s;
                cout << "Survivors: " << s << endl;
                return 0;
            }
        ''')
        # Test: stdin = "5" -> expected output "Survivors: 5\n"
        return ChallengeData(buggy_code, solution, "syntax", "Survivors: 5", "Missing semicolon (syntax)")

    def generate_2_off_by_one_sum(self):
        buggy_code = textwrap.dedent(r'''
            #include <iostream>
            using namespace std;

            int main() {
                int arr[] = {3, 5, 2};
                int sum = 0;
                for (int i = 0; i <= 3; ++i) { // off-by-one: reads out of bounds
                    sum += arr[i];
                }
                cout << sum << endl;
                return 0;
            }
        ''')
        solution = textwrap.dedent(r'''
            #include <iostream>
            using namespace std;

            int main() {
                int arr[] = {3, 5, 2};
                int sum = 0;
                for (int i = 0; i < 3; ++i) {
                    sum += arr[i];
                }
                cout << sum << endl;
                return 0;
            }
        ''')
        return ChallengeData(buggy_code, solution, "logic", "10", "Off-by-one loop (logic)")

    def generate_3_substr_bounds(self):
        buggy_code = textwrap.dedent(r'''
            #include <iostream>
            #include <string>
            using namespace std;

            int main() {
                string s = "zombies";
                cout << s.substr(0, 100) << endl; // misuse of substr arguments
                return 0;
            }
        ''')
        solution = textwrap.dedent(r'''
            #include <iostream>
            #include <string>
            using namespace std;

            int main() {
                string s = "zombies";
                cout << s.substr(0, s.size()) << endl;
                return 0;
            }
        ''')
        return ChallengeData(buggy_code, solution, "index", "zombies", "String substr bounds (index)")

    def generate_4_wrong_condition_and(self):
        buggy_code = textwrap.dedent(r'''
            #include <iostream>
            using namespace std;

            int main() {
                int x = 10;
                if (x > 5 && x < 20) { // intended: check outside range, bug uses &&
                    cout << "Out of range" << endl;
                } else {
                    cout << "In range" << endl;
                }
                return 0;
            }
        ''')
        solution = textwrap.dedent(r'''
            #include <iostream>
            using namespace std;

            int main() {
                int x = 10;
                if (x < 5 || x > 20) { // correct: out of range when less than 5 or greater than 20
                    cout << "Out of range" << endl;
                } else {
                    cout << "In range" << endl;
                }
                return 0;
            }
        ''')
        # Correct program prints "In range"
        return ChallengeData(buggy_code, solution, "logic", "In range", "Wrong conditional operator (logic)")

    def generate_5_missing_return_in_main(self):
        buggy_code = textwrap.dedent(r'''
            #include <iostream>
            using namespace std;

            int main() {
                cout << "Mission started" << endl;
            }
        ''')
        solution = textwrap.dedent(r'''
            #include <iostream>
            using namespace std;

            int main() {
                cout << "Mission started" << endl;
                return 0;
            }
        ''')
        return ChallengeData(buggy_code, solution, "syntax", "Mission started", "Missing return in main (syntax)")

    def generate_6_uninitialized_variable(self):
        buggy_code = textwrap.dedent(r'''
            #include <iostream>
            using namespace std;

            int main() {
                int health;
                if (health > 0) {
                    cout << "Alive" << endl;
                } else {
                    cout << "Dead" << endl;
                }
                return 0;
            }
        ''')
        solution = textwrap.dedent(r'''
            #include <iostream>
            using namespace std;

            int main() {
                int health = 10;
                if (health > 0) {
                    cout << "Alive" << endl;
                } else {
                    cout << "Dead" << endl;
                }
                return 0;
            }
        ''')
        return ChallengeData(buggy_code, solution, "runtime", "Alive", "Uninitialized variable (runtime)")

    def generate_7_integer_division(self):
        buggy_code = textwrap.dedent(r'''
            #include <iostream>
            using namespace std;

            int main() {
                int a = 5, b = 2;
                double avg = a / b; // integer division bug
                cout << avg << endl;
                return 0;
            }
        ''')
        solution = textwrap.dedent(r'''
            #include <iostream>
            using namespace std;

            int main() {
                int a = 5, b = 2;
                double avg = (double)a / b;
                cout << avg << endl;
                return 0;
            }
        ''')
        # Will print "2.5" (note: string comparison expects "2.5")
        return ChallengeData(buggy_code, solution, "logic", "2.5", "Integer division -> float (logic)")

    def generate_8_array_index_order(self):
        buggy_code = textwrap.dedent(r'''
            #include <iostream>
            using namespace std;

            int main() {
                int a[3] = {1, 2, 3};
                cout << a[3] << endl; // out-of-bounds: prints garbage
                return 0;
            }
        ''')
        solution = textwrap.dedent(r'''
            #include <iostream>
            using namespace std;

            int main() {
                int a[3] = {1, 2, 3};
                cout << a[2] << endl;
                return 0;
            }
        ''')
        return ChallengeData(buggy_code, solution, "index", "3", "Array index out-of-bounds (index)")

    def generate_9_wrong_initialization_memory(self):
        buggy_code = textwrap.dedent(r'''
            #include <iostream>
            using namespace std;

            int main() {
                int *p = nullptr;
                *p = 5; // dereference null
                cout << *p << endl;
                return 0;
            }
        ''')
        solution = textwrap.dedent(r'''
            #include <iostream>
            using namespace std;

            int main() {
                int value = 5;
                int *p = &value;
                cout << *p << endl;
                return 0;
            }
        ''')
        return ChallengeData(buggy_code, solution, "runtime", "5", "Null pointer dereference (runtime)")

    def generate_10_wrong_loop_direction(self):
        buggy_code = textwrap.dedent(r'''
            #include <iostream>
            using namespace std;

            int main() {
                for (int i = 10; i >= 0; ++i) { // ++i when should decrement -> infinite loop
                    if (i == 0) {
                        cout << "Blast off!" << endl;
                    }
                }
                return 0;
            }
        ''')
        solution = textwrap.dedent(r'''
            #include <iostream>
            using namespace std;

            int main() {
                for (int i = 10; i >= 0; --i) {
                    if (i == 0) {
                        cout << "Blast off!" << endl;
                    }
                }
                return 0;
            }
        ''')
        return ChallengeData(buggy_code, solution, "logic", "Blast off!", "Wrong loop direction (logic)")

    def generate_11_string_compare_bug(self):
        buggy_code = textwrap.dedent(r'''
            #include <iostream>
            #include <string>
            using namespace std;

            int main() {
                string secret = "z";
                if (secret == "Z") {
                    cout << "Match" << endl;
                } else {
                    cout << "No match" << endl;
                }
                return 0;
            }
        ''')
        solution = textwrap.dedent(r'''
            #include <iostream>
            #include <string>
            #include <algorithm>
            using namespace std;

            int main() {
                string secret = "z";
                // case-insensitive compare
                if (tolower(secret[0]) == tolower('Z')) {
                    cout << "Match" << endl;
                } else {
                    cout << "No match" << endl;
                }
                return 0;
            }
        ''')
        return ChallengeData(buggy_code, solution, "logic", "Match", "Case-sensitivity bug (logic)")

    def generate_12_wrong_modulo_usage(self):
        buggy_code = textwrap.dedent(r'''
            #include <iostream>
            using namespace std;

            int main() {
                int n = 10;
                if (n % 2 = 0) { // assignment used instead of comparison
                    cout << "Even" << endl;
                } else {
                    cout << "Odd" << endl;
                }
                return 0;
            }
        ''')
        solution = textwrap.dedent(r'''
            #include <iostream>
            using namespace std;

            int main() {
                int n = 10;
                if (n % 2 == 0) {
                    cout << "Even" << endl;
                } else {
                    cout << "Odd" << endl;
                }
                return 0;
            }
        ''')
        return ChallengeData(buggy_code, solution, "syntax", "Even", "Assignment vs comparison (syntax)")

    def generate_13_missing_break_switch(self):
        buggy_code = textwrap.dedent(r'''
            #include <iostream>
            using namespace std;

            int main() {
                int code = 2;
                switch (code) {
                    case 1:
                        cout << "One" << endl;
                    case 2:
                        cout << "Two" << endl;
                    case 3:
                        cout << "Three" << endl;
                }
                return 0;
            }
        ''')
        solution = textwrap.dedent(r'''
            #include <iostream>
            using namespace std;

            int main() {
                int code = 2;
                switch (code) {
                    case 1:
                        cout << "One" << endl;
                        break;
                    case 2:
                        cout << "Two" << endl;
                        break;
                    case 3:
                        cout << "Three" << endl;
                        break;
                }
                return 0;
            }
        ''')
        # With break statements, output should be "Two"
        return ChallengeData(buggy_code, solution, "logic", "Two", "Missing breaks in switch (logic)")

    def generate_14_string_length_off_by_one(self):
        buggy_code = textwrap.dedent(r'''
            #include <iostream>
            #include <string>
            using namespace std;

            int main() {
                string s = "abc";
                for (int i = 0; i <= s.length(); ++i) {
                    cout << s[i];
                }
                cout << endl;
                return 0;
            }
        ''')
        solution = textwrap.dedent(r'''
            #include <iostream>
            #include <string>
            using namespace std;

            int main() {
                string s = "abc";
                for (int i = 0; i < (int)s.length(); ++i) {
                    cout << s[i];
                }
                cout << endl;
                return 0;
            }
        ''')
        return ChallengeData(buggy_code, solution, "index", "abc", "String length off-by-one (index)")

    def generate_15_bad_swap_logic(self):
        buggy_code = textwrap.dedent(r'''
            #include <iostream>
            using namespace std;

            void swap_values(int a, int b) {
                int temp = a;
                a = b;
                b = temp;
            }

            int main() {
                int x = 1, y = 2;
                swap_values(x, y);
                cout << x << " " << y << endl;
                return 0;
            }
        ''')
        solution = textwrap.dedent(r'''
            #include <iostream>
            using namespace std;

            void swap_values(int &a, int &b) {
                int temp = a;
                a = b;
                b = temp;
            }

            int main() {
                int x = 1, y = 2;
                swap_values(x, y);
                cout << x << " " << y << endl;
                return 0;
            }
        ''')
        return ChallengeData(buggy_code, solution, "logic", "2 1", "Swap by value vs reference (logic)")

    def generate_16_buffer_overflow_like(self):
        buggy_code = textwrap.dedent(r'''
            #include <iostream>
            using namespace std;

            int main() {
                char buf[4] = "hello"; // too large for buffer
                cout << buf << endl;
                return 0;
            }
        ''')
        solution = textwrap.dedent(r'''
            #include <iostream>
            using namespace std;

            int main() {
                const char* buf = "hello";
                cout << buf << endl;
                return 0;
            }
        ''')
        return ChallengeData(buggy_code, solution, "runtime", "hello", "Buffer overflow / C-string (runtime)")

    def generate_17_wrong_recursion_base(self):
        buggy_code = textwrap.dedent(r'''
            #include <iostream>
            using namespace std;

            int factorial(int n) {
                if (n == 0) return 0; // bug: should return 1
                return n * factorial(n - 1);
            }

            int main() {
                cout << factorial(5) << endl;
                return 0;
            }
        ''')
        solution = textwrap.dedent(r'''
            #include <iostream>
            using namespace std;

            int factorial(int n) {
                if (n == 0) return 1;
                return n * factorial(n - 1);
            }

            int main() {
                cout << factorial(5) << endl;
                return 0;
            }
        ''')
        # factorial(5) = 120
        return ChallengeData(buggy_code, solution, "logic", "120", "Wrong recursion base case (logic)")

    def generate_18_wrong_vector_resize(self):
        buggy_code = textwrap.dedent(r'''
            #include <iostream>
            #include <vector>
            using namespace std;

            int main() {
                vector<int> v;
                v.resize(3);
                for (int i = 0; i <= 3; ++i) { // off-by-one, will access out-of-range
                    v[i] = i + 1;
                }
                for (int x : v) cout << x;
                cout << endl;
                return 0;
            }
        ''')
        solution = textwrap.dedent(r'''
            #include <iostream>
            #include <vector>
            using namespace std;

            int main() {
                vector<int> v;
                v.resize(3);
                for (int i = 0; i < 3; ++i) {
                    v[i] = i + 1;
                }
                for (int x : v) cout << x;
                cout << endl;
                return 0;
            }
        ''')
        return ChallengeData(buggy_code, solution, "index", "123", "Vector indexing off-by-one (index)")

    def generate_19_missing_include_for_stringstream(self):
        buggy_code = textwrap.dedent(r'''
            #include <iostream>
            #include <string>
            using namespace std;

            int main() {
                string s = "10 20";
                std::stringstream ss(s); // stringstream not included -> compile error
                int a, b;
                ss >> a >> b;
                cout << (a + b) << endl;
                return 0;
            }
        ''')
        solution = textwrap.dedent(r'''
            #include <iostream>
            #include <string>
            #include <sstream>
            using namespace std;

            int main() {
                string s = "10 20";
                std::stringstream ss(s);
                int a, b;
                ss >> a >> b;
                cout << (a + b) << endl;
                return 0;
            }
        ''')
        return ChallengeData(buggy_code, solution, "compile", "30", "Missing include (compile)")

    def generate_20_incorrect_format_output(self):
        buggy_code = textwrap.dedent(r'''
            #include <iostream>
            using namespace std;

            int main() {
                int minutes = 90;
                int hr = minutes / 60;
                int min = minutes % 60;
                cout << hr << ":" << min << endl; // prints 1:30 but format should be 1:30 with two-digit minutes if needed (here okay)
                return 0;
            }
        ''')
        solution = textwrap.dedent(r'''
            #include <iostream>
            #include <iomanip>
            using namespace std;

            int main() {
                int minutes = 90;
                int hr = minutes / 60;
                int min = minutes % 60;
                cout << hr << ":" << setw(2) << setfill('0') << min << endl;
                return 0;
            }
        ''')
        # For minutes=90 expected "1:30"
        return ChallengeData(buggy_code, solution, "format", "1:30", "Output formatting (format)")

    def generate_all_challenges(self) -> Dict[int, ChallengeData]:
        """
        Return a mapping from level number (1..20) to ChallengeData.
        You can edit/extend each generator above to create variations.
        """
        return {
            1: self.generate_1_missing_semicolon(),
            2: self.generate_2_off_by_one_sum(),
            3: self.generate_3_substr_bounds(),
            4: self.generate_4_wrong_condition_and(),
            5: self.generate_5_missing_return_in_main(),
            6: self.generate_6_uninitialized_variable(),
            7: self.generate_7_integer_division(),
            8: self.generate_8_array_index_order(),
            9: self.generate_9_wrong_initialization_memory(),
            10: self.generate_10_wrong_loop_direction(),
            11: self.generate_11_string_compare_bug(),
            12: self.generate_12_wrong_modulo_usage(),
            13: self.generate_13_missing_break_switch(),
            14: self.generate_14_string_length_off_by_one(),
            15: self.generate_15_bad_swap_logic(),
            16: self.generate_16_buffer_overflow_like(),
            17: self.generate_18_wrong_vector_resize(),  # small intentional shuffle to keep variety
            18: self.generate_17_wrong_recursion_base(),
            19: self.generate_19_missing_include_for_stringstream(),
            20: self.generate_20_incorrect_format_output(),
        }
