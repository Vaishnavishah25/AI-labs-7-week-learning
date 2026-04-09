import numpy as np
tosses = np.random.choice(['H', 'T'], size=4)
prob_heads = np.sum(tosses == 'H') / len(tosses)
print("Probability of getting heads:", prob_heads)

