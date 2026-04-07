# given probabilities
P_disease = 0.01
P_positive_given_disease = 0.99
P_positive = 0.05  # assume total positives

# Bayes theorem
P_disease_given_positive = (P_positive_given_disease * P_disease) / P_positive

print("Probability of disease given positive:", P_disease_given_positive)


### Example 2: Spam Email Detection
P_spam = 0.3
P_free_given_spam = 0.8
P_free = 0.4

P_spam_given_free = (P_free_given_spam * P_spam) / P_free

print("P(Spam | FREE):", P_spam_given_free)


