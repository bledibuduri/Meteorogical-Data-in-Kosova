import pandas as pd
import matplotlib.pyplot as plt

# Lexo file-in CSV duke përdorur pandas
df = pd.read_csv(r'C:\Users\Admin\Desktop\krahasimi_windspeed.csv')

# Shfaq kolonat e dataset-it
print("Kolonat e dataset-it:")
print(df.columns)

# Përcakto formatin e datës në kolonën 'SARIMA'
df['SARIMA'] = pd.to_datetime(df['SARIMA'], format='%m/%d/%Y %H:%M', errors='coerce')

# Përzgjidh vetëm kolonat e interesuara
selected_columns = df[['SARIMA', 'Unnamed: 11', 'Unnamed: 12']]

# Vendos kolonën 'SARIMA' si indeks
selected_columns.set_index('SARIMA', inplace=True)

# Vizualizo rezultatet në grafika të ndara për secilën kolonë
plt.figure(figsize=(10, 6))
for column in selected_columns.columns:
    plt.plot(selected_columns.index, selected_columns[column], label=column)

plt.title('Vizualizimi i rezultateve SARIMA')
plt.xlabel('Të dhënat kohore')
plt.ylabel('Vlerat e rezultateve')
plt.legend()
plt.show()
