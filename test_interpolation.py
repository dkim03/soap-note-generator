import random
import math
import matplotlib.pyplot as plt

def get_guaranteed_staircase_path(start, target, total_runs):
    path = [start]
    current_val = start
    
    for i in range(1, total_runs + 1):
        # 1. On the last step, force the target to guarantee the hit
        if i == total_runs:
            path.append(target)
            break
            
        # 2. Calculate the 'Ideal' next step to stay on track
        remaining_runs = total_runs - i
        distance_to_go = target - current_val
        ideal_step = distance_to_go / remaining_runs
        
        # 3. Apply Staircase Logic
        # We use a bias: if we are behind the 'ideal' path, increase up_chance
        up_chance = 0.1
        down_chance = 0.9 * (0.90 ** i) # Your adaptive down chance
        
        noise = 0
        if random.random() < up_chance:
            noise = random.randint(0, 3)
        elif target < current_val and random.random() < down_chance:
            noise = -random.randint(0, 1)
            
        # 4. Move toward target + noise
        current_val = round(min(max(int(current_val + noise + round(ideal_step * 0.75)), target), 10))
        path.append(current_val)
        
    return path

# --- Simulation Parameters ---
current_val = 8    # Starting point
target_val = 3     # The goal we want to trend toward
steps = 20          # Number of iterations

get_guaranteed_staircase_path(current_val, target_val, steps)

# --- Graphing the Results ---
plt.figure(figsize=(10, 5))
plt.plot(get_guaranteed_staircase_path(current_val, target_val, steps), marker='o', linestyle='-', color='b', label='Current Value')
plt.axhline(y=target_val, color='r', linestyle='--', label='Target Baseline')

plt.title(f"Random Walk with Trend Toward {target_val}")
plt.xlabel("Step / Iteration")
plt.ylabel("Value")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()