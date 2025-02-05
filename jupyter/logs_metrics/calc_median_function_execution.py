import pandas as pd
from datetime import datetime

def calculate_median_function_execution(func_name: str, execution_count: int) -> float:
    today_date = datetime.now().strftime("%Y-%m-%d")
    # Load CSV data into a DataFrame
    data = pd.read_csv(f'./logs_analysis/{today_date}/execution_{execution_count}/{today_date}-{func_name}-logs.csv')
    # Calculate the mean of the 'functionexectime' column
    median_execution_time = data['execution_time'].median()

    return median_execution_time

# def calc_median_function_execution_for_funcs():
#     median_optimized = calculate_median_function_execution("optimizedFunction")
#     median_baseline = calculate_median_function_execution("baselineFunction")

#     print(f"The median of OPTIMIZED function execution time is: {median_optimized}")
#     print(f"The median of BASELINE function execution time is: {median_baseline}")

def calc_median_function_execution_OPTIMIZED(execution_count: int):
    median_optimized = calculate_median_function_execution("optimizedFunction", execution_count)
    print(f"The median of OPTIMIZED function execution time is: {median_optimized}")

def calc_median_function_execution_BASELINE(execution_count: int):
    median_baseline = calculate_median_function_execution("baselineFunction", execution_count)
    print(f"The median of BASELINE function execution time is: {median_baseline}")   

def return_median_function_execution_OPTIMIZED(execution_count: int):
    return calculate_median_function_execution("optimizedFunction", execution_count)

def return_median_function_execution_BASELINE(execution_count: int):
    return calculate_median_function_execution("baselineFunction", execution_count)

# func_name = "baselineFunction" | "optimizedFunction"
def return_median_function_execution(date: str, execution_count: int, func_name: str):
    # Load CSV data into a DataFrame
    data = pd.read_csv(f'./logs_analysis/{date}/execution_{execution_count}/{date}-{func_name}-logs.csv')
    
    # Calculate the mean of the 'functionexectime' column
    median_execution_time = data['execution_time'].median()
    
    return median_execution_time