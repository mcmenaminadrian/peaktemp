import pandas as pd

def fix_data_frame(temp_data_frame) -> pd.DataFrame:
    fixed_data_frame = {}
    # fix types of dataframe columns
    fix_temp_cols(temp_data_frame)
    # Convert all 12 hour observations into 24 hour obseravtions
    fixed_data_frame = one_day_observations(temp_data_frame)
    # Fix nissing days in the dataframe
    fixed_data_frame = report_missing_days(fixed_data_frame)
    return fixed_data_frame

def fix_temp_cols(temp_data_frame):
    # Convert the columns to appropriate types
    temp_data_frame['ob_end_time'] = pd.to_datetime(temp_data_frame['ob_end_time'], errors='coerce')
    try:
        temp_data_frame['ob_hour_count'] = temp_data_frame['ob_hour_count'].astype(float)
    except:
        print("Error converting 'ob_hour_count' to float. Please check the data for non-numeric values.")
    try:
        temp_data_frame['max_air_temp'] = temp_data_frame['max_air_temp'].astype(float)
    except:
        print("Error converting 'max_air_temp' to float. Please check the data for non-numeric values.")
    try:
        temp_data_frame['min_air_temp'] = temp_data_frame['min_air_temp'].astype(float)
    except:
        print("Error converting 'min_air_temp' to float. Please check the data for non-numeric values.")

def one_day_observations(temp_data_frame) -> pd.DataFrame:
    # Convert all 12 hour observations into 24 hour observations
    # Create a new dataframe to store the fixed data
    fixed_data_frame = pd.DataFrame(columns=temp_data_frame.columns)

    for index, row in temp_data_frame.iterrows():
        if row['ob_hour_count'] == 12:
            if row['ob_end_time'].hour == 21:
                # if observation is at 9pm then update the following days 9am observation to collective min/max
                temp_data_frame.loc[index + 1, 'max_air_temp'] = max(row['max_air_temp'], temp_data_frame.loc[index + 1, 'max_air_temp'])
                temp_data_frame.loc[index + 1, 'min_air_temp'] = min(row['min_air_temp'], temp_data_frame.loc[index + 1, 'min_air_temp'])
                #update the observation hour count to 24
                temp_data_frame.loc[index + 1, 'ob_hour_count'] = 24
            elif row['ob_end_time'].hour == 9:
                print(f"DID NOT FIX: Observation at 9am on {row['ob_end_time']} with 12 hour count, skipping for now.")
            else:
                print(f"STRANGE TIME: Observation at {row['ob_end_time']} with {row['ob_hour_count']} hour count, skipping for now.")
                continue
        
        fixed_data_frame = pd.concat([fixed_data_frame, row.to_frame().T], ignore_index=True)

    return fixed_data_frame
    
    

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