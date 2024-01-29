import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Assuming your dataset is in a CSV file
df = pd.read_csv(r'C:\Users\Admin\Desktop\Krahasimi_temperature.csv')

# Print column names to check for typos or case sensitivity
print("Column Names:", df.columns)

# Combine datetime and temperature columns for each year
df['2017'] = pd.to_datetime(df['2017'], format='%m/%d/%Y %H:%M', utc=True, errors='coerce')
df['2018'] = pd.to_datetime(df['2018'], format='%m/%d/%Y %H:%M', utc=True, errors='coerce')
df['2019'] = pd.to_datetime(df['2019'], format='%m/%d/%Y %H:%M', utc=True, errors='coerce')
df['2020'] = pd.to_datetime(df['2020'], format='%m/%d/%Y %H:%M', utc=True, errors='coerce')
df['2021'] = pd.to_datetime(df['2021'], format='%m/%d/%Y %H:%M', utc=True, errors='coerce')
df['2022'] = pd.to_datetime(df['2022'], format='%d.%m.%Y %H:%M:%S', utc=True, errors='coerce')

# Drop rows with NaT values in datetime columns
df = df.dropna(subset=['2017', '2018', '2019', '2020', '2021', '2022'])

# Plot temperature data for each year
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(df['2017'], df['Unnamed: 1'], label='2017')
plt.plot(df['2018'], df['Unnamed: 3'], label='2018')
plt.plot(df['2019'], df['Unnamed: 5'], label='2019')
plt.plot(df['2020'], df['Unnamed: 7'], label='2020')
plt.plot(df['2021'], df['Unnamed: 9'], label='2021')
plt.plot(df['2022'], df['Unnamed: 11'], label='2022')

plt.title('Temperature Over Years')
plt.xlabel('Date')
plt.ylabel('Temperature')
plt.legend()

# Plot SARIMA results
plt.subplot(2, 1, 2)
plt.plot(df['SARIMA'], df['lower T_mu_actual'], label='Upper Bound')
plt.plot(df['SARIMA'], df['upper T_mu_actual'], label='Lower Bound')

# You can customize the SARIMA plot as needed
plt.fill_between(df['SARIMA'], df['lower T_mu_actual'], df['upper T_mu_actual'], where=(~np.isnan(df['lower T_mu_actual']) & ~np.isnan(df['upper T_mu_actual'])), color='gray', alpha=0.2)

plt.title('SARIMA Results')
plt.xlabel('Date')
plt.ylabel('Values')
plt.legend()

plt.tight_layout()
plt.show()
