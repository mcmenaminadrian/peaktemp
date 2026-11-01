import csv
import pandas as pd

years = range(1874, 2026)
rows = []
Observation_End_Time = []
Observation_Hour_Count = []
Max_Air_Temp = []
Min_Air_Temp = []

zip_strip = ['ob_end_time', 'ob_hour_count', 'max_air_temp', 'min_air_temp']
file_name_string = "midas-open_uk-daily-temperature-obs_dv-202607_western-isles_00054_stornoway-airport_qcv-1_"
path_base = "../raw_data/places/STORNOWAY/"
for year in years:
    file_path = path_base + file_name_string + str(year) + ".csv"
    with open(file_path) as readings_file:
        for n in range(93):
            readings_file.readline()
        csv_readings = csv.DictReader(readings_file)
        #fields = next(csv_readings)
        for row in csv_readings:
            if row.get(zip_strip[0]) == 'end data':
                break
            Observation_End_Time.append(row.get(zip_strip[0]))
            Observation_Hour_Count.append(row.get(zip_strip[1]))
            Max_Air_Temp.append(row.get(zip_strip[2]))
            Min_Air_Temp.append(row.get(zip_strip[3]))

data = {
    zip_strip[0]:Observation_End_Time,
    zip_strip[1]:Observation_Hour_Count,
    zip_strip[2]:Max_Air_Temp,
    zip_strip[3]:Min_Air_Temp
}
temp_data_frame = pd.DataFrame(data)
print(temp_data_frame)
processtempframe.report_missing_days(temp_data_frame)