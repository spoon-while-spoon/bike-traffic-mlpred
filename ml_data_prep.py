
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

sns.set(color_codes=True)

# Konvertiert einen Integer-Zeitstempel in ein Datums-/Zeitformat
def parse_date(date_int):
    date_str = str(date_int) # Konvertiert den Integer in einen String
    return pd.to_datetime(date_str, format='%Y%m%d%H')

# Einlesen der CSV-Dateien sowie erste Anpassungen
wind_df = pd.read_csv("wind.csv", sep=";", index_col=1, parse_dates=True, date_parser=parse_date).drop(['eor', 'STATIONS_ID', 'QUALITAETS_NIVEAU', 'STRUKTUR_VERSION', 'WINDRICHTUNG'], axis=1)
sun_df = pd.read_csv("sun.csv", sep=";", index_col=1, parse_dates=True, date_parser=parse_date).drop(['STATIONS_ID', 'QUALITAETS_NIVEAU', 'STRUKTUR_VERSION', 'eor'], axis=1)
precipation_df = pd.read_csv("precipation.csv", sep=";", index_col=1, parse_dates=True, date_parser=parse_date).drop(['STATIONS_ID', 'QUALITAETS_NIVEAU', 'STRUKTUR_VERSION', 'eor'], axis=1)
airpressure_df = pd.read_csv("airpressure.csv", sep=";", index_col=1, parse_dates=True, date_parser=parse_date).drop(['STATIONS_ID', 'QUALITAETS_NIVEAU', 'STRUKTUR_VERSION', 'LUFTDRUCK_STATIONSHOEHE', 'eor'], axis=1)

air_temp_df = pd.read_csv("air_temp.csv", sep=";", index_col=1, parse_dates=True, date_parser=parse_date).drop(['STATIONS_ID', 'QUALITAETS_NIVEAU', 'STRUKTUR_VERSION', 'LUFTTEMPERATUR_FALSCH', 'STRAHLUNGSTEMPERATUR', 'eor'], axis=1)
air_temp_df['LUFTTEMPERATUR_RICHTIG'] = pd.to_numeric(air_temp_df['LUFTTEMPERATUR_RICHTIG'], errors='coerce')
air_temp_df['REL_FEUCHTE'] = pd.to_numeric(air_temp_df['REL_FEUCHTE'], errors='coerce')
air_temp_df = air_temp_df[(air_temp_df['LUFTTEMPERATUR_RICHTIG'] >= -25) & (air_temp_df['LUFTTEMPERATUR_RICHTIG'] <= 45) & (air_temp_df['REL_FEUCHTE'] >= 0) & (air_temp_df['REL_FEUCHTE'] <= 99)]

radverkehr_df = pd.read_csv("radverkehr_final.csv", sep=";", index_col=1, parse_dates=True, date_parser=parse_date).drop(['datum_rad'], axis=1).assign(RAD_gesamt=lambda df: df['NORD'] + df['SUED'])

df_cleaned = pd.concat([wind_df, sun_df, precipation_df, airpressure_df, air_temp_df, radverkehr_df], axis=1).dropna()
