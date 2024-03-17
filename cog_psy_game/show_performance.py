"""
File:   show_performance.py
Authors: Jakub Janicek (j.janicek@student.rug.nl)

Description:
    This program creates a plot showcasing which terms you are good on and which not.
"""

import csv
from collections import defaultdict
import matplotlib.pyplot as plt


def calculate_success_rate(correct_count, total_count):
    if total_count == 0:
        return 0
    return correct_count / total_count * 100


def process_csv_data(filename):
    term_data = defaultdict(lambda: (0, 0))

    terms = []

    with open(filename, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        next(reader)

        for row in reader:
            term, _, is_correct = row
            terms.append(term)

            correct, total = term_data[term]
            term_data[term] = (
                correct + (1 if is_correct.lower() == "true" else 0),
                total + 1,
            )

    success_rates = {
        term: calculate_success_rate(correct, total)
        for term, (correct, total) in term_data.items()
    }

    total_correct = sum(correct for _, correct in term_data.values())
    total_count = sum(total for _, total in term_data.values())
    total_success_rate = calculate_success_rate(total_correct, total_count)

    return terms, success_rates, total_success_rate


terms, success_rates, total_success_rate = process_csv_data("history.csv")
success_rate_values = [success_rates[term] for term in terms]


plt.figure(figsize=(10, 6))

sorted_indices = sorted(
    range(len(success_rate_values)), key=success_rate_values.__getitem__
)
sorted_terms = [terms[i] for i in sorted_indices]
sorted_success_rates = [success_rate_values[i] for i in sorted_indices]

plt.bar(sorted_terms, sorted_success_rates, color="skyblue")
plt.xlabel("Term")
plt.ylabel("Success Rate (%)")
plt.title("Success Rate of Unique Terms (Sorted)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
