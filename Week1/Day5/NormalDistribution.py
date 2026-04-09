import numpy as np
import matplotlib.pyplot as plt

# generate data (normal distribution)
data = np.random.normal(loc=70, scale=10, size=1000)

# stats
print("Mean:", np.mean(data))
print("Std Dev:", np.std(data))

# plot
plt.hist(data, bins=30)
plt.title("Normal Distribution (Marks Example)")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.show()