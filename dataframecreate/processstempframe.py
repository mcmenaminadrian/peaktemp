import pandas as pd

def report_missing_days(temp_data_frame):
    # Convert the 'ob_end_time' column to datetime format
    temp_data_frame['ob_end_time'] = pd.to_datetime(temp_data_frame['ob_end_time'], errors='coerce')

    # iterate through the dataframe and check for missing days
    missing_days = []
    for i in range(len(temp_data_frame) - 1):
        current_day = temp_data_frame['ob_end_time'].iloc[i]
        next_day = temp_data_frame['ob_end_time'].iloc[i + 1]
        if pd.notnull(current_day) and pd.notnull(next_day):
            if (next_day - current_day).days > 1:
                missing_days.append((current_day, next_day))
        
    if missing_days:
        print("Missing days found:")
        for start, end in missing_days:
            print(f"Missing days between {start.date()} and {end.date()}")