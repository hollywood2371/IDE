from flask import Flask, request, jsonify
import pickle
import numpy as np
import pandas as pd
import category_encoders as ce
import json

# Загрузка сохраненной модели из файла pickle
with open("data/best_model.pkl", "rb") as f:
    loaded_model = pickle.load(f)
# Загрузка нормализатора из файла pickle
with open("data/mm_scaler.csv", "rb") as f:
    mm_scaler = pickle.load(f)
# Загрузка кодировщика из файла pickle    
with open("data/encoder.csv", "rb") as f:
    encoder = pickle.load(f)

# создаём приложение
app = Flask(__name__)

@app.route('/')
def index():
    msg = "Тестовое сообщение. Сервер запущен!"
    return msg

@app.route('/predict', methods=['POST'])

def predict_func():
    df_out = request.json
    cols = ['Driver', 'LapNumber', 'Compound', 'Stint', 'TyreLife', 'Position', 'LapTime (s)', 'Race', 'Year', 'LapTime_Delta', 
            'Cumulative_Degradation', 'PitStop', 'PitNextLap', 'RaceProgress', 'Normalized_TyreLife', 'Position_Change', 'Prev_TyreLife']
    df_out = pd.DataFrame([df_out], columns=cols)
    
    df_out.fillna(0, inplace=True) 
    df_out = df_out.drop(['Prev_TyreLife'], axis=1)
    df_out = df_out.drop(['RaceProgress'], axis=1)
    df_out['Year'] = df_out['Year'].astype(object)
    race_length = df_out.groupby('Race')['LapNumber'].transform("max")
    df_out['RemainingLaps'] = race_length - df_out['LapNumber']
    df_out['TyreLifeRemainingRatio'] = df_out['TyreLife'] / (df_out['RemainingLaps']+1)
    df_out['PositionTyreLife'] = df_out['Position'] * df_out['TyreLife']
    df_out['LapDelta_TyreLife'] =  df_out['LapTime_Delta'] * df_out['TyreLife']
    df_out['Stint_TyreLife'] = df_out['Stint'] * df_out['TyreLife']

    cat_cols = df_out.select_dtypes(include=['object']).columns.tolist()

    type_bin = encoder.transform(df_out[cat_cols])
    df_out = pd.concat([df_out, type_bin], axis=1)
    df_out.drop(cat_cols, axis=1, inplace=True)

    col_names = list(df_out.columns)
    df_out = mm_scaler.transform(df_out)
    df_out = pd.DataFrame(df_out, columns=col_names)
    X_test = df_out.drop(['PitNextLap'], axis=1)
    y_predict = loaded_model.predict(X_test)
    return jsonify({'prediction': y_predict[0]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
