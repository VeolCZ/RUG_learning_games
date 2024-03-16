import csv
from collections import defaultdict
import matplotlib.pyplot as plt


# Define functions to calculate success rate
def calculate_success_rate(correct_count, total_count):
    if total_count == 0:
        return 0  # Avoid division by zero
    return correct_count / total_count * 100  # Percentage


def process_csv_data(filename):
    # Initialize variables with correct tuple format
    term_data = defaultdict(
        lambda: (0, 0)
    )  # Dictionary to store (correct, total) counts

    terms = []

    # Read CSV file
    with open(filename, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        next(reader)  # Skip header row (assuming there's one)

        for row in reader:
            term, _, is_correct = row
            terms.append(term)

            # Update correct count based on lowercase comparison
            correct, total = term_data[term]
            term_data[term] = (
                correct + (1 if is_correct.lower() == "true" else 0),
                total + 1,
            )

    # Calculate success rates and total success rate
    success_rates = {
        term: calculate_success_rate(correct, total)
        for term, (correct, total) in term_data.items()
    }

    total_correct = sum(correct for _, correct in term_data.values())
    total_count = sum(total for _, total in term_data.values())
    total_success_rate = calculate_success_rate(total_correct, total_count)

    return terms, success_rates, total_success_rate


# Get data from CSV file (replace "your_file.csv" with the actual filename)
terms, success_rates, total_success_rate = process_csv_data("history.csv")
success_rate_values = [success_rates[term] for term in terms]


# Plot the bar graph (updated for sorting)
plt.figure(figsize=(10, 6))

# Sort terms and success_rate_values together based on success rates
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
