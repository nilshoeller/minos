import pandas as pd

# Load CSV data into a DataFrame
data_optimized = pd.read_csv('./logs_archive/2024-10-30-optimizedFunction-logs.csv')
data_baseline = pd.read_csv('./logs_archive/2024-10-30-baselineFunction-logs.csv')
# Calculate the mean of the 'functionexectime' column
median_optimized_functionexectime = data_optimized['functionexectime'].median()
median_baseline_functionexectime = data_baseline['functionexectime'].median()

# Print the result
print(f"The median of OPTIMIZED function execution time is: {median_optimized_functionexectime}")
print(f"The median of BASELINE function execution time is: {median_baseline_functionexectime}")