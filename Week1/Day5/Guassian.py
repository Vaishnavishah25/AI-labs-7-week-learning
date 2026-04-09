import numpy as np

def gaussian(x, mu, sigma):
    """Calculate the Gaussian function value for given x, mean (mu), and standard deviation (sigma)."""
    coefficient = 1 / (sigma * np.sqrt(2 * np.pi))
    # Calculate the exponent part of the Gaussian function
    exponent = np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))
    return coefficient * exponent

# Example usage
x = 80
mu = 70
sigma = 10

gaussian_value = gaussian(x, mu, sigma)
print("Gaussian value is:", gaussian_value)