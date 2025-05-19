import random
import shutil

def load_dice(filename):
    with open(filename, 'r') as f:
        rolls = [int(line.strip()) for line in f if line.strip().isdigit()]
    return rolls

def simulate_dice(rolls, num_simulations=10):
    results = [random.choice(rolls) for _ in range(num_simulations)]
    return results

def append_rolls_to_copy(original_file, new_rolls):
    copy_file = original_file.replace('.txt', '_copy.txt')
    #shutil.copyfile(original_file, copy_file)
    with open(original_file, 'a') as f:
        for roll in new_rolls:
            f.write(f"{roll}\n")
    return copy_file

if __name__ == "__main__":
    filename = input("Enter dice roll file (e.g., d20.txt): ")
    rolls = load_dice(filename)
    num_simulations = int(input("How many times to roll? "))
    results = simulate_dice(rolls, num_simulations)
    print("Simulated rolls:", results)
    copy_filename = append_rolls_to_copy(filename, results)
