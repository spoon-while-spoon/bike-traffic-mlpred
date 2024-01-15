import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
sns.set(color_codes=True)

df = pd.read_csv("clean_df.csv", sep=",")
'''

clean_df.csv wurde eigenständig aus den rohen Quelldatensätzen erstellt und schon grob bereinigt.  
Das Vorgehen ist dokumentiert in einem Jupyter Notebook zu finden unter: 

'https://colab.research.google.com/drive/1qyLI53fHqJtWuZdn4FPWjr5ISydRSJtF'

'''

df['NIEDERSCHLAGSHOEHE'] = pd.to_numeric(df['NIEDERSCHLAGSHOEHE'], errors='coerce')
df['MESS_DATUM'] = pd.to_datetime(df['MESS_DATUM'])
df.info()

# Korrelations Heatmap
correlation_matrix = df.corr()
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Korrelationsmatrix (Seaborn)")
plt.show()


df['WOCHENTYP'] = np.where(df['MESS_DATUM'].dt.dayofweek < 5, 'Wochentag', 'Wochenende')
df['MONAT'] = df['MESS_DATUM'].dt.month

# Boxplot 
plt.figure(figsize=(10, 6))
sns.boxplot(x='WOCHENTYP', y='RAD_GESAMT', data=df)
plt.title('Vergleich des Radverkehrs: Wochentag vs. Wochenende')
plt.xlabel('Wochentyp')
plt.ylabel('Radverkehr (Gesamt)')
plt.show()

#Balkendiagramm 
monthly_avg = df.groupby('MONAT')['RAD_GESAMT'].mean()
plt.figure(figsize=(10, 6))
sns.barplot(x=monthly_avg.index, y=monthly_avg.values)
plt.title('Durchschnittlicher Radverkehr pro Monat')
plt.xlabel('Monat')
plt.ylabel('Durchschnittlicher Radverkehr (Gesamt)')
plt.xticks(ticks=range(12), labels=['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez'])
plt.show()

# Scatterplot 
# Radverkehrsnutzung | Sonnenstunden
sns.jointplot(x='SONNENSCHEINDAUER', y='RAD_GESAMT', kind='reg', data=df, height=8)
plt.suptitle('Radverkehrsnutzung gegen Sonnenstunden', y=1.03) # Verschiebung der Überschrift nach oben
plt.xlabel('Sonnenscheindauer (in Stunden)')
plt.ylabel('Radverkehr (Gesamt)')
plt.show()

# Scatterplot
# Radverkehrsnutzung | Temperatur
sns.jointplot(x='LUFTTEMPERATUR', y='RAD_GESAMT', kind='reg', data=df, height=8)
plt.suptitle('Radverkehrsnutzung gegen Temperatur', y=1.03) # Verschiebung der Überschrift nach oben
plt.xlabel('Lufttemperatur (in °C)')
plt.ylabel('Radverkehr (Gesamt)')
plt.show()


# Features und Target festlegen
features = df[['SONNENSCHEINDAUER', 'LUFTTEMPERATUR', 'LUFTFEUCHTIGKEIT', 'WINDGESCHWINDIGKEIT', 'WOCHENTYP', 'MONAT']]
target = df['RAD_GESAMT']

# One-Hot-Encoding für WOCHENTYP 
one_hot_encoder = OneHotEncoder()
encoded_features = one_hot_encoder.fit_transform(features[['WOCHENTYP']]).toarray()
encoded_feature_labels = one_hot_encoder.get_feature_names_out(['WOCHENTYP'])
features_encoded = pd.DataFrame(encoded_features, columns=encoded_feature_labels)
features = features.drop('WOCHENTYP', axis=1)
features = pd.concat([features, features_encoded], axis=1)

# Daten autteilen 
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
X_train.head(), y_train.head()

# Random Forest Modell trsainieren
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Vorhersage
y_pred = rf_model.predict(X_test)

# Bewertung des Modells
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

mse, r2

'''Ergebnis

(47199.95319719929, 0.41313892891045323)

'''
