import pandas as pd
import matplotlib.pyplot as plt
import datetime

new_data_frame = pd.read_pickle("fixed_temp_data_frame.pkl")

max_annual = []
first_time = True
start_year = 0
for row in new_data_frame.itertuples():
    if first_time == True:
        max_yearly_temp = row.max_air_temp
        start_year = row.ob_end_time.year
        first_time = False
    else:
        if row.ob_end_time.year > start_year:
            max_annual.append([start_year, max_yearly_temp])
            max_yearly_temp = row.max_air_temp
            start_year = row.ob_end_time.year
        else:
            if row.max_air_temp > max_yearly_temp:
                max_yearly_temp = row.max_air_temp
            

max_annual_df = pd.DataFrame(max_annual, columns=['year', 'max_air_temp'])
max_annual_df.plot(kind='line', x='year', y='max_air_temp', title='Stornoway Airport Annual Max Temperatures', grid=True)
plt.show()