import random

def load_dice(filename):
    with open(filename, 'r') as f:
        rolls = [int(line.strip()) for line in f if line.strip().isdigit()]
    return rolls

def build_transition_matrix(rolls):
    transitions = {}
    for i in range(len(rolls) - 1):
        curr, nxt = rolls[i], rolls[i+1]
        if curr not in transitions:
            transitions[curr] = []
        transitions[curr].append(nxt)
    return transitions

def simulate_dice_markov(rolls, transitions, num_simulations=10):
    results = []
    if not rolls:
        return results
    current = random.choice(rolls)
    results.append(current)
    for _ in range(num_simulations - 1):
        next_options = transitions.get(current, rolls)
        current = random.choice(next_options)
        results.append(current)
    return results

def append_rolls_to_copy(original_file, new_rolls):
    copy_file = original_file.replace('.txt', '_copy.txt')
    with open(original_file, 'a') as f:
        for roll in new_rolls:
            f.write(f"{roll}\n")
    return copy_file

if __name__ == "__main__":
    filename = input("Enter dice roll file (e.g., d20.txt): ")
    rolls = load_dice(filename)
    transitions = build_transition_matrix(rolls)
    num_simulations = int(input("How many times to roll? "))
    results = simulate_dice_markov(rolls, transitions, num_simulations)
    print("Simulated rolls:", results)
    copy_filename = append_rolls_to_copy(filename, results)
