import pandas as pd
from datetime import datetime

def calculate_median_download(func_name: str, execution_count: int) -> float:
    today_date = datetime.now().strftime("%Y-%m-%d")
    # Load CSV data into a DataFrame
    data = pd.read_csv(f'./logs_analysis/{today_date}/execution_{execution_count}/{today_date}-{func_name}-logs.csv')
    
    # Convert 'download_duration' to numeric, setting errors='coerce' to handle non-numeric values
    data = data[data['download_duration'] != "---"]

    data['download_duration'] = data['download_duration'].astype(int)
    # Calculate the mean of the 'download_duration' column
    median_download_time = data['download_duration'].median()

    return median_download_time

# def calc_median_download_for_funcs():
#     median_optimized = calculate_median_download("optimizedFunction")
#     median_baseline = calculate_median_download("baselineFunction")

#     print(f"The median of OPTIMIZED function download duration is: {median_optimized}")
#     print(f"The median of BASELINE function download duration is: {median_baseline}")

def calc_median_download_OPTIMIZED(execution_count: int):
    median_optimized = calculate_median_download("optimizedFunction", execution_count)
    print(f"The median of OPTIMIZED function download duration is: {median_optimized}")

def calc_median_download_BASELINE(execution_count: int):
    median_baseline = calculate_median_download("baselineFunction", execution_count)
    print(f"The median of BASELINE function download duration is: {median_baseline}")   

def return_median_download_OPTIMIZED(execution_count: int):
    return calculate_median_download("optimizedFunction",execution_count)

def return_median_download_BASELINE(execution_count: int):
    return calculate_median_download("baselineFunction", execution_count)

# func_name = "baselineFunction" | "optimizedFunction"
def return_median_download(date: str, execution_count: int, func_name: str):
    # Load CSV data into a DataFrame
    data = pd.read_csv(f'./logs_analysis/{date}/execution_{execution_count}/{date}-{func_name}-logs.csv')
    
    # Convert 'download_duration' to numeric, setting errors='coerce' to handle non-numeric values
    data = data[data['download_duration'] != "---"]
    data['download_duration'] = data['download_duration'].astype(int)

    # Calculate the median of the 'download_duration' column
    median_download_time = data['download_duration'].median()

    return median_download_time