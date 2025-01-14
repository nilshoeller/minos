import pandas as pd
from datetime import datetime

def calculate_median_lr_duration(func_name: str, execution_count: int) -> float:
    today_date = datetime.now().strftime("%Y-%m-%d")
    # Load CSV data into a DataFrame
    data = pd.read_csv(f'./logs_archive/{today_date}/execution_{execution_count}/{today_date}-{func_name}-logs.csv')
    
    # Convert 'lr_duration_duration' to numeric, setting errors='coerce' to handle non-numeric values
    data = data[data['lr_duration'] != 0]

    data['lr_duration'] = data['lr_duration'].astype(int)
    # Calculate the mean of the 'lr_duration_duration' column
    median_lr_duration_time = data['lr_duration'].median()

    return median_lr_duration_time

# def calc_median_lr_duration_for_funcs():
#     median_optimized = calculate_median_lr_duration("optimizedFunction")
#     median_baseline = calculate_median_lr_duration("baselineFunction")

#     print(f"The median of OPTIMIZED function linear-regression duration is: {median_optimized}")
#     print(f"The median of BASELINE function linear-regression duration is: {median_baseline}")

def calc_median_lr_duration_OPTIMIZED(execution_count: int):
    median_optimized = calculate_median_lr_duration("optimizedFunction", execution_count)
    print(f"The median of OPTIMIZED function linear-regression duration is: {median_optimized}")

def calc_median_lr_duration_BASELINE(execution_count: int):
    median_baseline = calculate_median_lr_duration("baselineFunction", execution_count)
    print(f"The median of BASELINE function linear-regression duration is: {median_baseline}")   

def return_median_lr_duration_OPTIMIZED(execution_count: int):
    return calculate_median_lr_duration("optimizedFunction", execution_count)

def return_median_lr_duration_BASELINE(execution_count: int):
    return calculate_median_lr_duration("baselineFunction", execution_count)