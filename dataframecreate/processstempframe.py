import pandas as pd

def fix_data_frame(temp_data_frame) -> pd.DataFrame:
    fixed_data_frame = {}
    # fix dataframe column
    fix_temp_date_col(temp_data_frame)
    # Convert all 12 hour observations into 24 hour obseravtions
    fixed_data_frame = one_day_observations(temp_data_frame)
    # Fix nissing days in the dataframe
    report_missing_days(fixed_data_frame)
    return fixed_data_frame

def fix_temp_date_col(temp_data_frame):
    # Convert the date col to appropriate types
    temp_data_frame['ob_end_time'] = pd.to_datetime(temp_data_frame['ob_end_time'], errors='coerce')
    try:
        temp_data_frame['ob_hour_count'] = temp_data_frame['ob_hour_count'].astype(float)
    except:
        print("Error converting 'ob_hour_count' to float. Please check the data for non-numeric values.")

def one_day_observations(temp_data_frame) -> pd.DataFrame:
    # Convert all 12 hour observations into 24 hour observations
    # fix the type of the columns as we go along
    # Create a new dataframe to store the fixed data
    force_continue = False
    fixed_data_frame = pd.DataFrame(columns=temp_data_frame.columns)
    last_max = 0.0
    last_min = 0.0
    old_max = 0.0
    old_min = 0.0
    last_min_temp = 0.0
    last_max_temp = 0.0
    old_min_temp = 0.0
    old_max_temp = 0.0
    for index, row in temp_data_frame.iterrows():
        if force_continue:
            force_continue = False
            continue
        if row['ob_hour_count'] == 24:
            try:
                last_max = float(row['max_air_temp'])
                last_min = float(row['min_air_temp'])
                micro_data_frame = pd.DataFrame([[row['ob_end_time'],
                                                  row['ob_hour_count'],
                                                  last_max,
                                                  last_min]],
                                                columns=temp_data_frame.columns)
                old_max = last_max
                old_min = last_min
            except Exception as e:
                print(f"Error creating micro dataframe for observation:", row['ob_end_time'], f"with error: {e}")
                # fix by subsituting last value - not injecting any new temps then
                micro_data_frame = pd.DataFrame([[row['ob_end_time'],
                                                      row['ob_hour_count'],
                                                      old_max,
                                                      old_min]],
                                                    columns=temp_data_frame.columns)
            fixed_data_frame = pd.concat([fixed_data_frame, micro_data_frame], ignore_index=True)
            continue
        elif row['ob_end_time'].hour == 9:
            if (row['ob_hour_count'] != 12):
                print(f"***STRANGE LENGTH: Observation at {row['ob_end_time']} with {row['ob_hour_count']} hour count, skipping for now.")
            continue;
        else:
            if row['ob_end_time'].hour != 21:
                print(f"***STRANGE TIME: Observation at {row['ob_end_time']} with {row['ob_hour_count']} hour count, skipping for now.")
                continue
            else:
                try:
                    last_min_temp = min(float(row['min_air_temp']), float(temp_data_frame.loc[index + 1, 'min_air_temp']))
                    last_max_temp = max(float(row['max_air_temp']), float(temp_data_frame.loc[index + 1, 'max_air_temp']))
                    old_min_temp = last_min_temp
                    old_max_temp = last_max_temp
                except Exception as e:
                    print(f"Error occurred while processing min/maxobservation at {row['ob_end_time']}: {e}")
                    # again fix by subsituting last value - not injecting any new temps then
                    last_min_temp = old_min_temp
                    last_max_temp = old_max_temp
                micro_data_frame = pd.DataFrame([[temp_data_frame.loc[index + 1, 'ob_end_time'],
                                                 24,
                                                 last_max_temp,
                                                 last_min_temp]],
                                                columns=temp_data_frame.columns)
                fixed_data_frame = pd.concat([fixed_data_frame, micro_data_frame], ignore_index=True)
                force_continue = True

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