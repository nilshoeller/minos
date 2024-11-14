import pandas as pd
from datetime import datetime

def calculate_median_function_execution(func_name: str) -> float:
    today_date = datetime.now().strftime("%Y-%m-%d")
    # Load CSV data into a DataFrame
    data = pd.read_csv(f'./logs_archive/{today_date}-{func_name}-logs.csv')
    # Calculate the mean of the 'functionexectime' column
    median_execution_time = data['execution_time'].median()

    return median_execution_time

def calc_median_function_execution_for_funcs():
    median_optimized = calculate_median_function_execution("optimizedFunction")
    median_baseline = calculate_median_function_execution("baselineFunction")

    print(f"The median of OPTIMIZED function execution time is: {median_optimized}")
    print(f"The median of BASELINE function execution time is: {median_baseline}")

def calc_median_function_execution_OPTIMIZED():
    median_optimized = calculate_median_function_execution("optimizedFunction")
    print(f"The median of OPTIMIZED function execution time is: {median_optimized}")

def calc_median_function_execution_BASELINE():
    median_baseline = calculate_median_function_execution("baselineFunction")
    print(f"The median of BASELINE function execution time is: {median_baseline}")   

def return_median_function_execution_OPTIMIZED():
    return calculate_median_function_execution("optimizedFunction")

def return_median_function_execution_BASELINE():
    return calculate_median_function_execution("baselineFunction")