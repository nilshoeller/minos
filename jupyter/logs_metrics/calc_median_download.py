import pandas as pd
from datetime import datetime

def calculate_median_download(func_name: str) -> float:
    today_date = datetime.now().strftime("%Y-%m-%d")
    # Load CSV data into a DataFrame
    data = pd.read_csv(f'./logs_archive/{today_date}-{func_name}-logs.csv')
    
    # Convert 'download_duration' to numeric, setting errors='coerce' to handle non-numeric values
    data = data[data['download_duration'] != "---"]

    data['download_duration'] = data['download_duration'].astype(int)
    # Calculate the mean of the 'download_duration' column
    median_download_time = data['download_duration'].median()

    return median_download_time

def calc_median_download_for_funcs():
    median_optimized = calculate_median_download("optimizedFunction")
    median_baseline = calculate_median_download("baselineFunction")

    print(f"The median of OPTIMIZED function download duration is: {median_optimized}")
    print(f"The median of BASELINE function download duration is: {median_baseline}")

def calc_median_download_OPTIMIZED():
    median_optimized = calculate_median_download("optimizedFunction")
    print(f"The median of OPTIMIZED function download duration is: {median_optimized}")

def calc_median_download_BASELINE():
    median_baseline = calculate_median_download("baselineFunction")
    print(f"The median of BASELINE function download duration is: {median_baseline}")   