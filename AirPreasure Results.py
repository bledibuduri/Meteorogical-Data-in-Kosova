import pandas as pd
import matplotlib.pyplot as plt

# Lexo file-in CSV duke përdorur pandas
df = pd.read_csv(r'C:\Users\Admin\Desktop\krahasimi_airpreasure.csv')

# Shfaq kolonat e dataset-it
print("Kolonat e dataset-it:")
print(df.columns)

# Përcakto formatin e datës në kolonën 'SARIMA'
df['SARIMA'] = pd.to_datetime(df['SARIMA'], format='%m/%d/%Y %H:%M', errors='coerce')

# Përzgjidh vetëm kolonat e interesuara për 'AirPressure'
selected_columns_airpressure = df[['SARIMA', 'Unnamed: 12']]

# Vendos kolonën 'SARIMA' si indeks
selected_columns_airpressure.set_index('SARIMA', inplace=True)

# Riemëro kolonën 'Unnamed: 12' si 'Rezultati SARIMA'
selected_columns_airpressure.rename(columns={'Unnamed: 12': 'Rezultati SARIMA'}, inplace=True)

# Vizualizo rezultatet për 'AirPressure' me kolonën e riemëruar
plt.figure(figsize=(10, 6))
for column in selected_columns_airpressure.columns:
    plt.plot(selected_columns_airpressure.index, selected_columns_airpressure[column], label=column)

plt.title('Vizualizimi i rezultateve për AirPressure')
plt.xlabel('Të dhënat kohore')
plt.ylabel('Vlerat e rezultateve')
plt.legend()
plt.show()
