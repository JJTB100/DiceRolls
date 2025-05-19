import numpy as np
from scipy.stats import chisquare

import matplotlib.pyplot as plt
while True:
    try:
        sides = int(input("Enter the number of sides on the die: ").strip())
        if sides > 1:
            break
        else:
            print("Please enter an integer greater than 1.")
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

fileName = ""
if not fileName:
    fileName = input("Enter the filename to save/load dice rolls: ").strip()
# Prompt the user to enter numbers and save them to the file until -1 is entered
while True:
    user_input = input("Enter a dice roll to save, or -1 to finish: ").strip()
    if user_input == "-1":
        break
    elif user_input.isdigit():
        roll = int(user_input)
        if 1 <= roll <= sides:
            with open(fileName, "a") as f_append:
                f_append.write(f"{roll}\n")
            avg_roll = np.mean([int(line.strip()) for line in open(fileName) if line.strip().isdigit()])
            total_rolls = sum(1 for _ in open(fileName))
            # ANSI escape codes for color (e.g., cyan)
            color_start = "\033[96m"
            color_end = "\033[0m"
            print(f"Current average roll: {color_start}{avg_roll:.2f}{color_end} out of {color_start}{total_rolls}{color_end} rolls.")
            print(f"Saved roll {roll} to {fileName}.")#
        else:
            print(f"Invalid roll. Please enter a number between 1 and {sides}.")
    elif user_input:
        print("Invalid input. Please enter a number between 1 and 20 or -1 to finish.")
numLines = 0
# Read the dice rolls from the file
with open(fileName, "r") as f:
    rolls = [int(line.strip()) for line in f if line.strip().isdigit()]
    numLines = len(rolls)


# Prepare the transition matrix
transitions = np.zeros((sides, sides), dtype=int)

for i in range(len(rolls) - 1):
    prev_roll = rolls[i] - 1  # zero-based index
    next_roll = rolls[i + 1] - 1
    transitions[next_roll, prev_roll] += 1

# Avoid division by zero
probabilities = np.divide(transitions, numLines)
average_roll = np.mean(rolls)
print(f"Average roll: {average_roll:.2f}")

# Plot the heatmap
# Normalize transitions by columns to get P(next | previous)
transition_sums = transitions.sum(axis=0, keepdims=True)
# Avoid division by zero
conditional_probabilities = np.divide(
    transitions, 
    transition_sums, 
    out=np.zeros_like(transitions, dtype=float), 
    where=transition_sums != 0
)

# Perform chi-squared test for uniformity
observed_counts = np.array([rolls.count(i + 1) for i in range(sides)])
expected_counts = np.full(sides, numLines / sides)
chi2_stat, p_value = chisquare(observed_counts, expected_counts)

print(f"Chi-squared statistic: {chi2_stat:.2f}")
print(f"P-value: {p_value:.4f}")
if p_value < 0.05:
    print("The distribution of rolls is significantly different from uniform (p < 0.05).")
else:
    print("The distribution of rolls is not significantly different from uniform (p >= 0.05).")

plt.figure(figsize=(8, 6))
plt.imshow(conditional_probabilities, cmap='hot', interpolation='nearest', origin='lower', vmin=0, vmax=max(conditional_probabilities.flatten()))
plt.colorbar(label='P(Next Roll | Previous Roll)')
plt.xlabel('Previous Roll')
plt.ylabel('Next Roll')
plt.title('Conditional Probability: P(Next Roll | Previous Roll)')
plt.xticks(np.arange(sides), np.arange(1, sides + 1))
plt.yticks(np.arange(sides), np.arange(1, sides + 1))
plt.tight_layout()
plt.show()
# Plot histogram of number of occurrences for each roll
plt.figure(figsize=(8, 4))
plt.hist(rolls, bins=np.arange(1, sides + 2) - 0.5, edgecolor='black', rwidth=0.8)
plt.xlabel('Die Face')
plt.ylabel('Occurrences')
plt.title('Histogram of Dice Roll Occurrences')
plt.xticks(np.arange(1, sides + 1))
plt.tight_layout()
# Plot the expected (uniform) count as a horizontal line
expected_count = numLines / sides
plt.axhline(expected_count, color='red', linestyle='dashed', linewidth=2, label='Expected (Uniform)')
plt.legend()
# Add probability labels on top of each bar
counts, bins, patches = plt.hist(rolls, bins=np.arange(1, sides + 2) - 0.5, edgecolor='black', rwidth=0.8)
for i, count in enumerate(counts):
    prob = count / numLines
    plt.text(i + 1, count + max(counts)*0.01, f"{prob:.2f}", ha='center', va='bottom', fontsize=8)
plt.show()

# Plot the rolling mean of the dice rolls
window_size = 50  # You can adjust this window size as needed
rolling_mean = np.convolve(rolls, np.ones(window_size)/window_size, mode='valid')

plt.figure(figsize=(10, 4))
plt.plot(range(window_size, window_size + len(rolling_mean)), rolling_mean, label=f'Rolling Mean (window={window_size})')
plt.axhline(average_roll, color='red', linestyle='dashed', label='Overall Mean')
plt.xlabel('Roll Number')
plt.ylabel('Rolling Mean')
plt.title('Rolling Mean of Dice Rolls')
plt.legend()
plt.tight_layout()
plt.show()

# Plot the cumulative mean of dice rolls over time
cumulative_mean = np.cumsum(rolls) / np.arange(1, len(rolls) + 1)

plt.figure(figsize=(10, 4))
plt.plot(range(1, len(rolls) + 1), cumulative_mean, label='Cumulative Mean')
plt.axhline(average_roll, color='red', linestyle='dashed', label='Overall Mean')
plt.xlabel('Roll Number')
plt.ylabel('Cumulative Mean')
plt.title('Cumulative Mean of Dice Rolls Over Time')
plt.legend()
plt.tight_layout()
plt.show()
"""
# Print the amount of times each X is followed by each Y
print("Count of transitions from X to Y (X -> Y):")
for prev in range(sides):
    for nxt in range(sides):
        count = transitions[nxt, prev]
        if count > 0:
            print(f"{prev + 1} -> {nxt + 1}: {count}")
        else:
            print(f"{prev + 1} -> {nxt + 1}: 0")
            
            
"""