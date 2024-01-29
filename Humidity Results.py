import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

# Assuming your dataset is in a CSV file
df = pd.read_csv(r'C:\Users\Admin\Desktop\humidity_krahasimi.csv')

#Print column names to check for typos or case sensitivity
print("Column Names:", df.columns)

# Combine datetime and humidity columns for each year
df['Unnamed: 0'] = pd.to_datetime(df['Unnamed: 0'], format='%m/%d/%Y %H:%M', utc=True, errors='coerce')
df['Unnamed: 2'] = pd.to_datetime(df['Unnamed: 2'], format='%m/%d/%Y %H:%M', utc=True, errors='coerce')
df['Unnamed: 4'] = pd.to_datetime(df['Unnamed: 4'], format='%m/%d/%Y %H:%M', utc=True, errors='coerce')
df['Unnamed: 6'] = pd.to_datetime(df['Unnamed: 6'], format='%m/%d/%Y %H:%M', utc=True, errors='coerce')
df['Unnamed: 8'] = pd.to_datetime(df['Unnamed: 8'], format='%m/%d/%Y %H:%M', utc=True, errors='coerce')
df['Unnamed: 10'] = pd.to_datetime(df['Unnamed: 10'], format='%m/%d/%Y %H:%M', utc=True, errors='coerce')

# Drop rows with NaT values in datetime columns
df = df.dropna(subset=['Unnamed: 0', 'Unnamed: 2', 'Unnamed: 4', 'Unnamed: 6', 'Unnamed: 8', 'Unnamed: 10'])

# Convert y-values to strings
humidity_columns = ['Unnamed: 1', 'Unnamed: 3', 'Unnamed: 5', 'Unnamed: 7', 'Unnamed: 9', 'Unnamed: 11', 'Unnamed: 13', 'Unnamed: 14']

for col in humidity_columns:
    df[col] = df[col].astype(str)

# Plot humidity data for each year
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(df['Unnamed: 0'], df['Unnamed: 1'], label='2017')
plt.plot(df['Unnamed: 2'], df['Unnamed: 3'], label='2018')
plt.plot(df['Unnamed: 4'], df['Unnamed: 5'], label='2019')
plt.plot(df['Unnamed: 6'], df['Unnamed: 7'], label='2020')
plt.plot(df['Unnamed: 8'], df['Unnamed: 9'], label='2021')
plt.plot(df['Unnamed: 10'], df['Unnamed: 11'], label='2022')

plt.title('Humidity Over Years')
plt.xlabel('Date')
plt.ylabel('Humidity')
plt.legend()

# Plot SARIMA results
plt.subplot(2, 1, 2)
plt.plot(df['SARIMA'], df['Unnamed: 13'], label='Upper Bound')
plt.plot(df['SARIMA'], df['Unnamed: 14'], label='Lower Bound')

# You can customize the SARIMA plot as needed
plt.fill_between(df['SARIMA'], df['Unnamed: 13'], df['Unnamed: 14'], color='gray', alpha=0.2)

# Format x-axis dates
plt.gca().xaxis.set_major_formatter(DateFormatter('%m/%d/%Y %H:%M'))

plt.title('SARIMA Results')
plt.xlabel('Date')
plt.ylabel('Values')
plt.legend()

plt.tight_layout()
plt.show()
