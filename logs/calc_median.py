import pandas as pd
from datetime import datetime

today_date = datetime.now().strftime("%Y-%m-%d")

# Load CSV data into a DataFrame
data_optimized = pd.read_csv(f'./logs_archive/{today_date}-optimizedFunction-logs.csv')
data_baseline = pd.read_csv(f'./logs_archive/{today_date}-baselineFunction-logs.csv')
# Calculate the mean of the 'functionexectime' column
median_optimized_functionexectime = data_optimized['functionexectime'].median()
median_baseline_functionexectime = data_baseline['functionexectime'].median()

# Print the result
print(f"The median of OPTIMIZED function execution time is: {median_optimized_functionexectime}")
print(f"The median of BASELINE function execution time is: {median_baseline_functionexectime}")