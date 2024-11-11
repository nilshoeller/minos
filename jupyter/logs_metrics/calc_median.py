import pandas as pd
from datetime import datetime

def calculate_median(func_name: str) -> float:
    today_date = datetime.now().strftime("%Y-%m-%d")
    # Load CSV data into a DataFrame
    data = pd.read_csv(f'./logs_archive/{today_date}-{func_name}-logs.csv')
    # Calculate the mean of the 'functionexectime' column
    median_execution_time = data['execution_time'].median()

    return median_execution_time

def calc_median_for_funcs():
    median_optimized = calculate_median("optimizedFunction")
    median_baseline = calculate_median("baselineFunction")

    print(f"The median of OPTIMIZED function execution time is: {median_optimized}")
    print(f"The median of BASELINE function execution time is: {median_baseline}")

def calc_median_OPTIMIZED():
    median_optimized = calculate_median("optimizedFunction")
    print(f"The median of OPTIMIZED function execution time is: {median_optimized}")

def calc_median_BASELINE():
    median_baseline = calculate_median("baselineFunction")
    print(f"The median of BASELINE function execution time is: {median_baseline}")   