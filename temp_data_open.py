import csv
years = range(1874, 2026)
rows = []
zip_strip = ['ob_end_time', 'ob_hour_count', 'max_air_temp', 'min_air_temp']
file_name_string = "midas-open_uk-daily-temperature-obs_dv-202607_western-isles_00054_stornoway-airport_qcv-1_"
path_base = "../raw_data/places/STORNOWAY/"
#with open("../raw_data/places/STORNOWAY/midas-open_uk-daily-temperature-obs_dv-202607_western-isles_00054_stornoway-airport_qcv-1_1974.csv") as readings_file:
for year in years:
    file_path = path_base + file_name_string + str(year) + ".csv"
    with open(file_path) as readings_file:
        for n in range(93):
            readings_file.readline()
        csv_readings = csv.DictReader(readings_file)
        #fields = next(csv_readings)
        for row in csv_readings:
            rows.append(row)
        

    