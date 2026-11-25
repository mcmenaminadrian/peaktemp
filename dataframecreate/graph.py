import pandas as pd
import matplotlib.pyplot as plt

new_data_frame = pd.read_pickle("fixed_temp_data_frame.pkl")
new_data_frame.plot(kind='line', x='ob_end_time', y=['max_air_temp'], title='Stornoway Airport Daily Max and Min Temperatures', grid=True)
plt.show()