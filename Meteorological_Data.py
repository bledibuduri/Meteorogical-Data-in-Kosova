#Import neccessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
sns.set(style="darkgrid")

#Bejme leximin e Dataseteve
#Temperature
df1 = pd.read_csv(r'C:\Users\Admin\Desktop\Projekti Hulumtues\temperature.csv')
#Humidity
df2 = pd.read_csv(r'C:\Users\Admin\Desktop\Projekti Hulumtues\humidity.csv')
#AirPreasure
df3 = pd.read_csv(r'C:\Users\Admin\Desktop\Projekti Hulumtues\airpreasure.csv')
#WindSpeed
df4 = pd.read_csv(r'C:\Users\Admin\Desktop\Projekti Hulumtues\windspeed.csv')

#Filtrojme te dhenat per periudhen 2017-2022
#Temperature
df1_2017_2022 = df1[(df1['datetime'] >= '1/1/2017 0:00') & (df1['datetime'] <= '12/31/2021 23:00')]
#Humidity
df2_2017_2022 = df2[(df2['datetime'] >= '1/1/2017 0:00') & (df2['datetime'] <= '12/31/2021 23:00')]
#AirPreasure
df3_2017_2022 = df3[(df3['datetime'] >= '01.01.2017 00:00:00') & (df3['datetime'] <= '31.12.2022 23:00:00')]
#WindSpeed
df4_2017_2022 = df4[(df4['datetime'] >= '15.03.2018 10:00:00') & (df4['datetime'] <= '29.12.2022 17:15:00')]


#Convert date column to datetime
df1_2017_2022['datetime'] = pd.to_datetime(df1_2017_2022['datetime'], utc=True, errors='coerce')
df2_2017_2022['datetime'] = pd.to_datetime(df2_2017_2022['datetime'], utc=True, errors='coerce')
df3_2017_2022['datetime'] = pd.to_datetime(df3_2017_2022['datetime'], utc=True, errors='coerce')
df4_2017_2022['datetime'] = pd.to_datetime(df4_2017_2022['datetime'], utc=True, errors='coerce')

# Generate complete date range
start_date = '2017-01-01 00:00:00'
end_date = '2022-12-31 23:00:00'
date_range = pd.date_range(start=start_date, end=end_date, freq='H')

# Create DataFrames with the complete date range
complete_df1 = pd.DataFrame({'datetime': date_range})

# Convert datetime to UTC
complete_df1['datetime'] = complete_df1['datetime'].dt.tz_localize('UTC')

# Perform left join to include all dates
merged_dataset = pd.merge(complete_df1, df1_2017_2022, on='datetime', how='left')
merged_dataset = pd.merge(merged_dataset, df2_2017_2022, on='datetime', how='left', suffixes=('_Temperature', '_Humidity'))
merged_dataset = pd.merge(merged_dataset, df3_2017_2022, on='datetime', how='left', suffixes=('_Humidity', '_AirPressure'))
merged_dataset = pd.merge(merged_dataset, df4_2017_2022, on='datetime', how='left', suffixes=('_AirPressure', '_WindSpeed'))

#To save the merged DateFrame to a new CSV file
merged_dataset.to_csv('datasetprova1.csv', index=False)

#dataseti i bashkum
df = pd.read_csv('datasetprova1.csv')

# Save the updated DataFrame to a new CSV file
df1 = pd.DataFrame(df)

# Rename columns
df.rename(columns={'T_mu': 'Temperature', 'H_mu_Humidity': 'Humidity', 'H_mu_AirPressure': 'AirPressure', 'H_mu': 'WindSpeed'}, inplace=True)

# Save the updated DataFrame to a new CSV file
df.to_csv('dataseti1.csv', index=False)

# Load the updated DataFrame
df = pd.read_csv('dataseti1.csv')

def calculate_apparent_temperature( temperature, humidity):
    # Constants for the heat index formula
    c1 = -42.379
    c2 = 2.04901523
    c3 = 10.14333127
    c4 = -0.22475541
    c5 = -6.83783e-03
    c6 = -5.481717e-02
    c7 = 1.22874e-03
    c8 = 8.5282e-04
    c9 = -1.99e-06

    # Calculate the heat index
    heat_index = c1 + (c2 * temperature) + (c3 * humidity) + (c4 * temperature * humidity) + (c5 * temperature ** 2) + (c6 * humidity ** 2) + (c7 * temperature ** 2 * humidity) + (c8 * temperature * humidity ** 2) + (c9 * temperature ** 2 * humidity ** 2)

    return heat_index

# Apply the function to create a new column 'ApparentTemperature'
df['ApparentTemperature'] = df.apply(lambda row: calculate_apparent_temperature(row['Temperature'], row['Humidity']), axis=1)

# Save the updated DataFrame to a new CSV file
df.to_csv('updated.csv', index=False)

# Load the updated DataFrame
df = pd.read_csv('updated.csv')

#Shfaq vetem rreshtat 5 rreshtat e pare
print(df.head())

#Shfaq 5 rreshtat e fundit
print(df.tail())

print(df.shape)
print(df.describe())


# Exclude 'datetime' column from correlation calculation
columns_for_correlation = df.columns.difference(['datetime'])

# Calculate correlation
correlation_matrix = df[columns_for_correlation].corr(method='pearson')

# Print correlation matrix
print(correlation_matrix)

# Print the count of null values for each column
print(df.isnull().sum())
# Check if any column has null values
print(df.isna().any())

#Convert date column to datetime
df['datetime'] = pd.to_datetime(df['datetime'], utc=True, errors='coerce')

df.info()

#Creating a new dataframe and normalising Apparent Temperature
df_scaled = df.copy()
df_scaled['ApparentTemperature'] = (df_scaled['ApparentTemperature'] - df_scaled['ApparentTemperature'].min()) / (df_scaled['ApparentTemperature'].max() - df_scaled['ApparentTemperature'].min())
print(df_scaled.head())

# Check for NaN values in the original DataFrame
#print(df.isnull().sum())

# Fill NaN values with the mean of each column
df = df.apply(lambda x: x.fillna(x.mean()))

# Resample according to month and year
monthly_data = df.set_index('datetime').resample('M').mean()
yearly_data = df.set_index('datetime').resample('Y').mean()
df_monthly_scaled = df_scaled.set_index('datetime').resample('M').mean()


# Reset the index
monthly_data.reset_index(inplace=True)
yearly_data.reset_index(inplace=True)
df_monthly_scaled.reset_index(inplace=True)

# Print the first few rows of the resulting DataFrame
print(monthly_data.head())

#e morrem pjesen e tail per me shiku nese ka ndryshime ne resultate
print(monthly_data.tail())

# Print the first few rows of the resulting DataFrame
print(yearly_data.head())

df1 = df[['datetime','ApparentTemperature']]

#Maximum and minimum temperature per year
max_temp = df1.set_index('datetime').resample('Y').max()[1:]
min_temp = df1.set_index('datetime').resample('Y').min()[1:]
max_temp.reset_index(inplace=True)
min_temp.reset_index(inplace=True)
max_temp.rename(columns={'ApparentTemperature': 'Max Apparent Temperature (C)'}, inplace=True)
min_temp.rename(columns={'ApparentTemperature': 'Min Apparent Temperature (C)'}, inplace=True)
min_max_temp = pd.merge(max_temp, min_temp, how='inner',  on='datetime')
min_max_temp['datetime'] = min_max_temp['datetime'].dt.year

print(min_max_temp)

# Visualizing data

# Apparent Temperature From 2017-2022
plt.figure(figsize=(20, 10))
plt.title("Apparent Temperature From 2017-2022")
sns.lineplot(x=df['datetime'], y=df['ApparentTemperature'], marker='o', color='red')
plt.xlabel("Year")

# Average Temperature From 2017-2022
plt.figure(figsize=(20, 10))
plt.title('Average Apparent Temperature From 2017-2022')
sns.lineplot(x=monthly_data['datetime'], y=monthly_data['ApparentTemperature'], marker='o', color='red')
plt.xlabel("Year")

# Humidity From 2017-2022
plt.figure(figsize=(20, 10))
plt.title("Humidity From 2017-2022")
sns.lineplot(x=df['datetime'], y=df['Humidity'], marker='o')
plt.xlabel("Year")

# Average Humidity From 2017-2022
plt.figure(figsize=(20, 10))
plt.title("Average Humidity From 2017-2022")
sns.lineplot(x=monthly_data['datetime'], y=monthly_data['Humidity'], marker='o')
plt.xlabel('Year')

# Average Humidity From 2017-2022
plt.figure(figsize=(20, 10))
plt.title("Average Apparent Temperature and Humidity From 2017-2022")
sns.lineplot(x=df_monthly_scaled['datetime'], y=df_monthly_scaled['ApparentTemperature'], marker='o', color='red',
             label='Apparent Temperature')
sns.lineplot(x=monthly_data['datetime'], y=monthly_data['Humidity'], marker='o', label='Humidity')
plt.xlabel('Year')

# Average Temperature From 2017-2022
plt.figure(figsize=(20, 10))
plt.title('Average Temperature From 2017-2022')
sns.lineplot(x=yearly_data['datetime'], y=yearly_data['ApparentTemperature'])
plt.xlabel("Year")

plt.figure(figsize=(12, 10))
plt.title("Correlation between all columns (excluding datetime)")
sns.heatmap(data=df.drop('datetime', axis=1).corr(), cmap="rocket", annot=True)
plt.show()

AT_H = monthly_data[['ApparentTemperature', 'Humidity']]
print(AT_H)

sns.pairplot(AT_H, kind='scatter').fig.set_size_inches(10, 10)

avg_monthly_temp = pd.DataFrame(df.groupby([df["datetime"].dt.month])["ApparentTemperature"].mean())
avg_monthly_humidity = pd.DataFrame(df.groupby([df["datetime"].dt.month])["Humidity"].mean())
avg_monthly_temp.reset_index(inplace=True)
avg_monthly_humidity.reset_index(inplace=True)
print(avg_monthly_temp)
print(avg_monthly_humidity)

# Monthly Average Temperature From 2017-2022
plt.figure(figsize=(20, 10))
plt.title("Monthly Average Temperature From 2017-2022")
sns.barplot(x='datetime', y='ApparentTemperature', data=avg_monthly_temp, palette="rocket")
plt.xlabel("Month")
plt.show()

#Monthly Average Humidity From 2017-2022
plt.figure(figsize=(20, 10))
plt.title("Monthly Average Humidity From 2017-2022")
sns.barplot(x=avg_monthly_humidity['datetime'], y=avg_monthly_humidity['Humidity'], palette="mako")
plt.xlabel("Month");
plt.show()

# Monthly Average Humidity From 2017-2022
plt.figure(figsize=(20, 10))
plt.title("Monthly Average Humidity From 2017-2022")
sns.lineplot(x='datetime', y='Humidity', data=avg_monthly_humidity)
plt.xlabel("Month")
plt.show()


#Minimum and Maximum Temperature per year from 2017-2022
X_axis = np.arange(len(min_max_temp['datetime']))

plt.figure(figsize=(20, 10))

plt.bar(X_axis - 0.2, min_max_temp['Min Apparent Temperature (C)'], 0.4, label='Min')
plt.bar(X_axis + 0.2, min_max_temp['Max Apparent Temperature (C)'], 0.4, label='Max')

plt.xticks(X_axis, min_max_temp['datetime'])
plt.xlabel("Year")
plt.ylabel("Apparent Temperature (C)")
plt.title("Minimum and Maximum Temperature per year from 2006-2016")
plt.legend()
plt.show()





