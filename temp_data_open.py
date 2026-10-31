import csv
fields = []
rows = []

with open("../raw_data/places/STORNOWAY/midas-open_uk-daily-temperature-obs_dv-202607_western-isles_00054_stornoway-airport_qcv-1_1874.csv") as readings_file:
    for n in range(93):
        readings_file.readline()
    csv_readings = csv.reader(readings_file)
    fields = next(csv_readings)
    for row in csv_readings:
        rows.append(row)
    
    print('Field names are: ' + ', '.join(fields))

    print('\nFirst 5 rows are:\n')
    for row in rows[:5]:
        for col in row:
            print("%10s" % col, end=" ")
        print('\n')
    