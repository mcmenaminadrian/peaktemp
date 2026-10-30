import os
cur_dir = os.getcwd()
print(cur_dir)
readings_file = open("../raw_data/places/STORNOWAY/midas-open_uk-daily-temperature-obs_dv-202607_western-isles_00054_stornoway-airport_qcv-1_1874.csv")
print(readings_file.read())
readings_file.close()