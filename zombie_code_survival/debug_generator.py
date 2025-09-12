import random
import textwrap
from dataclasses import dataclass
from typing import Dict

@dataclass
class ChallengeData:
    buggy_code: str
    solution: str
    error_type: str
    expected_output: any

class DebugGenerator:
    ERROR_TYPES = ["syntax", "type", "index", "attribute", "logic", "value"]
    
    def generate_challenge_1(self):
        """Syntax error - missing parenthesis"""
        buggy_code = textwrap.dedent("""
            def calculate_supplies(survivors, days):
                water_per_person = 2
                food_per_person = 1.5
                total_water = survivors * water_per_person * days
                total_food = survivors * food_per_person * days
                return total_water, total_food
                
            result = calculate_supplies(5, 7
            print(result)
        """)
        
        solution = textwrap.dedent("""
            def calculate_supplies(survivors, days):
                water_per_person = 2
                food_per_person = 1.5
                total_water = survivors * water_per_person * days
                total_food = survivors * food_per_person * days
                return total_water, total_food
                
            result = calculate_supplies(5, 7)
            print(result)
        """)
        
        expected_output = "(70, 52.5)"
        return ChallengeData(buggy_code, solution, "syntax", expected_output)
    
    def generate_challenge_2(self):
        """Syntax error - missing colon"""
        buggy_code = textwrap.dedent("""
            def check_danger_level(speed)
                if speed > 7:
                    return "EXTREME"
                elif speed > 5
                    return "HIGH"
                else
                    return "LOW"
                    
            print(check_danger_level(6))
        """)
        
        solution = textwrap.dedent("""
            def check_danger_level(speed):
                if speed > 7:
                    return "EXTREME"
                elif speed > 5:
                    return "HIGH"
                else:
                    return "LOW"
                    
            print(check_danger_level(6))
        """)
        
        expected_output = "HIGH"
        return ChallengeData(buggy_code, solution, "syntax", expected_output)
    
    def generate_challenge_3(self):
        """Type error - string concatenation with number"""
        buggy_code = textwrap.dedent("""
            def create_alert_message(zombie_count, location):
                return "Alert: " + zombie_count + " zombies spotted near " + location
                
            message = create_alert_message(5, "downtown")
            print(message)
        """)
        
        solution = textwrap.dedent("""
            def create_alert_message(zombie_count, location):
                return "Alert: " + str(zombie_count) + " zombies spotted near " + location
                
            message = create_alert_message(5, "downtown")
            print(message)
        """)
        
        expected_output = "Alert: 5 zombies spotted near downtown"
        return ChallengeData(buggy_code, solution, "type", expected_output)
    
    def generate_challenge_4(self):
        """Index error - accessing out of bounds"""
        buggy_code = textwrap.dedent("""
            def get_safe_route(routes):
                # Should return the safest route (lowest zombie count)
                safest_index = 0
                min_zombies = routes[0]
                for i in range(len(routes)):
                    if routes[i] < min_zombies:
                        min_zombies = routes[i]
                        safest_index = i
                return safest_index, routes[safest_index]
                
            zombie_counts = [15, 8, 3, 12]
            result = get_safe_route(zombie_counts)
            print(result)
        """)
        
        solution = textwrap.dedent("""
            def get_safe_route(routes):
                if not routes:
                    return None
                safest_index = 0
                min_zombies = routes[0]
                for i in range(len(routes)):
                    if routes[i] < min_zombies:
                        min_zombies = routes[i]
                        safest_index = i
                return safest_index, routes[safest_index]
                
            zombie_counts = [15, 8, 3, 12]
            result = get_safe_route(zombie_counts)
            print(result)
        """)
        
        expected_output = "(2, 3)"
        return ChallengeData(buggy_code, solution, "index", expected_output)
    
    def generate_challenge_5(self):
        """Attribute error - wrong method name"""
        buggy_code = textwrap.dedent("""
            def analyze_zombie_dna(dna_sequence):
                return dna_sequence.uppercase().count("X")
                
            result = analyze_zombie_dna("axbxcxdx")
            print(result)
        """)
        
        solution = textwrap.dedent("""
            def analyze_zombie_dna(dna_sequence):
                return dna_sequence.upper().count("X")
                
            result = analyze_zombie_dna("axbxcxdx")
            print(result)
        """)
        
        expected_output = "4"
        return ChallengeData(buggy_code, solution, "attribute", expected_output)
    
    def generate_challenge_6(self):
        """Logic error - incorrect condition"""
        buggy_code = textwrap.dedent("""
            def should_evacuate(zombie_count, distance):
                # Evacuate if zombies > 10 AND distance < 100
                return zombie_count > 10 or distance < 100
                
            print(should_evacuate(5, 50))
            print(should_evacuate(15, 150))
        """)
        
        solution = textwrap.dedent("""
            def should_evacuate(zombie_count, distance):
                # Evacuate if zombies > 10 AND distance < 100
                return zombie_count > 10 and distance < 100
                
            print(should_evacuate(5, 50))
            print(should_evacuate(15, 150))
        """)
        
        expected_output = "(False, False)"
        return ChallengeData(buggy_code, solution, "logic", expected_output)
    
    def generate_challenge_7(self):
        """Value error - invalid conversion"""
        buggy_code = textwrap.dedent("""
            def parse_zombie_data(data_str):
                values = data_str.split(",")
                return [int(val) for val in values]
                
            result = parse_zombie_data("10,5,8,abc,12")
            print(result)
        """)
        
        solution = textwrap.dedent("""
            def parse_zombie_data(data_str):
                values = data_str.split(",")
                result = []
                for val in values:
                    try:
                        result.append(int(val))
                    except ValueError:
                        result.append(0)  # Default value for invalid data
                return result
                
            result = parse_zombie_data("10,5,8,abc,12")
            print(result)
        """)
        
        expected_output = "[10, 5, 8, 12]"
        return ChallengeData(buggy_code, solution, "value", expected_output)
    
    def generate_challenge_8(self):
        """Syntax error - incorrect indentation"""
        buggy_code = textwrap.dedent("""
            def calculate_infection_risk(exposure_time, proximity):
            if exposure_time > 10:
                return "HIGH"
            elif exposure_time > 5:
            return "MEDIUM"
                else:
                return "LOW"
                
            print(calculate_infection_risk(8, 3))
        """)
        
        solution = textwrap.dedent("""
            def calculate_infection_risk(exposure_time, proximity):
                if exposure_time > 10:
                    return "HIGH"
                elif exposure_time > 5:
                    return "MEDIUM"
                else:
                    return "LOW"
                    
            print(calculate_infection_risk(8, 3))
        """)
        
        expected_output = "MEDIUM"
        return ChallengeData(buggy_code, solution, "syntax", expected_output)
    
    def generate_challenge_9(self):
        """Type error - wrong operation order"""
        buggy_code = textwrap.dedent("""
            def calculate_survival_chance(skills, resources):
                return skills + resources / 2
                
            result = calculate_survival_chance(8, 4)
            print(result)
        """)
        
        solution = textwrap.dedent("""
            def calculate_survival_chance(skills, resources):
                return (skills + resources) / 2
                
            result = calculate_survival_chance(8, 4)
            print(result)
        """)
        
        expected_output = "6.0"
        return ChallengeData(buggy_code, solution, "logic", expected_output)
    
    def generate_challenge_10(self):
        """Index error - wrong list access"""
        buggy_code = textwrap.dedent("""
            def get_resource_priority(resources):
                # Should return the two most critical resources
                sorted_resources = sorted(resources, reverse=True)
                return sorted_resources[0], sorted_resources[1]
                
            resources = ["water", "food", "medicine", "fuel"]
            result = get_resource_priority(resources)
            print(result)
        """)
        
        solution = textwrap.dedent("""
            def get_resource_priority(resources):
                # Should return the two most critical resources
                priority_order = ["medicine", "water", "food", "fuel"]
                critical = []
                for resource in priority_order:
                    if resource in resources:
                        critical.append(resource)
                        if len(critical) == 2:
                            break
                return tuple(critical)
                
            resources = ["water", "food", "medicine", "fuel"]
            result = get_resource_priority(resources)
            print(result)
        """)
        
        expected_output = "('medicine', 'water')"
        return ChallengeData(buggy_code, solution, "logic", expected_output)
    
    def generate_challenge_11(self):
        """Attribute error - missing import"""
        buggy_code = textwrap.dedent("""
            def calculate_distance(point1, point2):
                return math.sqrt((point2[0]-point1[0])**2 + (point2[1]-point1[1])**2)
                
            result = calculate_distance((0, 0), (3, 4))
            print(result)
        """)
        
        solution = textwrap.dedent("""
            import math
            
            def calculate_distance(point1, point2):
                return math.sqrt((point2[0]-point1[0])**2 + (point2[1]-point1[1])**2)
                
            result = calculate_distance((0, 0), (3, 4))
            print(result)
        """)
        
        expected_output = "5.0"
        return ChallengeData(buggy_code, solution, "attribute", expected_output)
    
    def generate_challenge_12(self):
        """Logic error - off-by-one error"""
        buggy_code = textwrap.dedent("""
            def count_safe_houses(grid):
                count = 0
                for i in range(len(grid)):
                    for j in range(len(grid[0])):
                        if grid[i][j] == "S":
                            count += 1
                return count
                
            area = [["S", "Z", "S"], ["Z", "S", "Z"], ["S", "S", "Z"]]
            print(count_safe_houses(area))
        """)
        
        solution = textwrap.dedent("""
            def count_safe_houses(grid):
                count = 0
                for row in grid:
                    for house in row:
                        if house == "S":
                            count += 1
                return count
                
            area = [["S", "Z", "S"], ["Z", "S", "Z"], ["S", "S", "Z"]]
            print(count_safe_houses(area))
        """)
        
        expected_output = "5"
        return ChallengeData(buggy_code, solution, "logic", expected_output)
    
    def generate_challenge_13(self):
        """Type error - wrong variable type"""
        buggy_code = textwrap.dedent("""
            def create_emergency_plan(plan_data):
                plan_data["timestamp"] = "2024-01-01"
                return plan_data.update({"status": "active"})
                
            result = create_emergency_plan({"type": "evacuation"})
            print(result)
        """)
        
        solution = textwrap.dedent("""
            def create_emergency_plan(plan_data):
                plan_data = plan_data.copy()
                plan_data["timestamp"] = "2024-01-01"
                plan_data["status"] = "active"
                return plan_data
                
            result = create_emergency_plan({"type": "evacuation"})
            print(result)
        """)
        
        expected_output = "{'type': 'evacuation', 'timestamp': '2024-01-01', 'status': 'active'}"
        return ChallengeData(buggy_code, solution, "type", expected_output)
    
    def generate_challenge_14(self):
        """Syntax error - wrong keyword"""
        buggy_code = textwrap.dedent("""
            def check_quarantine_status(days_infected):
                if days_infected < 7:
                    return "Under quarantine"
                elseif days_infected < 14:
                    return "Monitoring"
                otherwise:
                    return "Clear"
                    
            print(check_quarantine_status(10))
        """)
        
        solution = textwrap.dedent("""
            def check_quarantine_status(days_infected):
                if days_infected < 7:
                    return "Under quarantine"
                elif days_infected < 14:
                    return "Monitoring"
                else:
                    return "Clear"
                    
            print(check_quarantine_status(10))
        """)
        
        expected_output = "Monitoring"
        return ChallengeData(buggy_code, solution, "syntax", expected_output)
    
    def generate_challenge_15(self):
        """Logic error - incorrect algorithm"""
        buggy_code = textwrap.dedent("""
            def find_best_hiding_spot(spots):
                # Should return spot with most resources and least zombies
                best_spot = None
                for spot in spots:
                    if best_spot is None or spot["resources"] > best_spot["resources"]:
                        best_spot = spot
                return best_spot["name"]
                
            spots = [
                {"name": "A", "resources": 5, "zombies": 2},
                {"name": "B", "resources": 8, "zombies": 6},
                {"name": "C", "resources": 6, "zombies": 1}
            ]
            print(find_best_hiding_spot(spots))
        """)
        
        solution = textwrap.dedent("""
            def find_best_hiding_spot(spots):
                # Should return spot with best resource/zombie ratio
                best_spot = None
                best_ratio = -1
                for spot in spots:
                    ratio = spot["resources"] / max(1, spot["zombies"])
                    if ratio > best_ratio:
                        best_ratio = ratio
                        best_spot = spot
                return best_spot["name"]
                
            spots = [
                {"name": "A", "resources": 5, "zombies": 2},
                {"name": "B", "resources": 8, "zombies": 6},
                {"name": "C", "resources": 6, "zombies": 1}
            ]
            print(find_best_hiding_spot(spots))
        """)
        
        expected_output = "C"
        return ChallengeData(buggy_code, solution, "logic", expected_output)
    
    def generate_challenge_16(self):
        """Value error - division by zero"""
        buggy_code = textwrap.dedent("""
            def calculate_success_rate(successes, attempts):
                return successes / attempts
                
            print(calculate_success_rate(3, 0))
        """)
        
        solution = textwrap.dedent("""
            def calculate_success_rate(successes, attempts):
                if attempts == 0:
                    return 0.0
                return successes / attempts
                
            print(calculate_success_rate(3, 0))
        """)
        
        expected_output = "0.0"
        return ChallengeData(buggy_code, solution, "value", expected_output)
    
    def generate_challenge_17(self):
        """Attribute error - wrong method usage"""
        buggy_code = textwrap.dedent("""
            def encrypt_message(message, key):
                return message.encode().encrypt(key)
                
            result = encrypt_message("urgent", "secret")
            print(result)
        """)
        
        solution = textwrap.dedent("""
            def encrypt_message(message, key):
                # Simple XOR encryption for demonstration
                encrypted = []
                for i, char in enumerate(message):
                    encrypted.append(chr(ord(char) ^ ord(key[i % len(key)])))
                return ''.join(encrypted)
                
            result = encrypt_message("urgent", "secret")
            print(result)
        """)
        
        expected_output = "\x1e\x01\x1a\x00\x01\x15"
        return ChallengeData(buggy_code, solution, "attribute", expected_output)
    
    def generate_challenge_18(self):
        """Logic error - wrong loop condition"""
        buggy_code = textwrap.dedent("""
            def simulate_outbreak(days, initial_infected):
                infected = initial_infected
                for day in range(days):
                    infected = infected * 2  # Double each day
                return infected
                
            print(simulate_outbreak(5, 1))
        """)
        
        solution = textwrap.dedent("""
            def simulate_outbreak(days, initial_infected):
                infected = initial_infected
                for day in range(days):
                    infected = infected * 1.5  # 50% increase each day
                return int(infected)
                
            print(simulate_outbreak(5, 1))
        """)
        
        expected_output = "7"
        return ChallengeData(buggy_code, solution, "logic", expected_output)
    
    def generate_challenge_19(self):
        """Type error - wrong data structure"""
        buggy_code = textwrap.dedent("""
            def track_zombie_movements(movements):
                result = {}
                for movement in movements:
                    result.append(movement["type"])
                return result
                
            data = [{"type": "chase", "speed": 5}, {"type": "wander", "speed": 2}]
            print(track_zombie_movements(data))
        """)
        
        solution = textwrap.dedent("""
            def track_zombie_movements(movements):
                result = []
                for movement in movements:
                    result.append(movement["type"])
                return result
                
            data = [{"type": "chase", "speed": 5}, {"type": "wander", "speed": 2}]
            print(track_zombie_movements(data))
        """)
        
        expected_output = "['chase', 'wander']"
        return ChallengeData(buggy_code, solution, "type", expected_output)
    
    def generate_challenge_20(self):
        """Complex logic error - multiple issues"""
        buggy_code = textwrap.dedent("""
            def optimize_defense_strategy(resources, threats):
                strategy = []
                for i in range(len(threats)):
                    if threats[i] > resources[i]:
                        strategy.append("Evacuate")
                    else:
                        strategy.append("Defend")
                return strategy
                
            resources = [10, 15, 8, 20]
            threats = [8, 20, 5, 15]
            print(optimize_defense_strategy(resources, threats))
        """)
        
        solution = textwrap.dedent("""
            def optimize_defense_strategy(resources, threats):
                strategy = []
                total_resources = sum(resources)
                total_threats = sum(threats)
                
                if total_threats > total_resources * 1.5:
                    return ["Evacuate" for _ in threats]
                
                for i in range(len(threats)):
                    if threats[i] > resources[i] * 1.2:
                        strategy.append("Request reinforcements")
                    elif threats[i] > resources[i]:
                        strategy.append("Set up barriers")
                    else:
                        strategy.append("Defend")
                return strategy
                
            resources = [10, 15, 8, 20]
            threats = [8, 20, 5, 15]
            print(optimize_defense_strategy(resources, threats))
        """)
        
        expected_output = "['Defend', 'Request reinforcements', 'Defend', 'Defend']"
        return ChallengeData(buggy_code, solution, "logic", expected_output)
    
    def generate_all_challenges(self) -> Dict[int, ChallengeData]:
        """Generates all 20 challenge levels with progressive difficulty"""
        return {
            1: self.generate_challenge_1(),
            2: self.generate_challenge_2(),
            3: self.generate_challenge_3(),
            4: self.generate_challenge_4(),
            5: self.generate_challenge_5(),
            6: self.generate_challenge_6(),
            7: self.generate_challenge_7(),
            8: self.generate_challenge_8(),
            9: self.generate_challenge_9(),
            10: self.generate_challenge_10(),
            11: self.generate_challenge_11(),
            12: self.generate_challenge_12(),
            13: self.generate_challenge_13(),
            14: self.generate_challenge_14(),
            15: self.generate_challenge_15(),
            16: self.generate_challenge_16(),
            17: self.generate_challenge_17(),
            18: self.generate_challenge_18(),
            19: self.generate_challenge_19(),
            20: self.generate_challenge_20(),
        }