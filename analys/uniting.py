import pandas as pd
import pymorphy2
from sklearn.preprocessing import LabelEncoder


file_mapping = {
    'Транспорт_keys.csv': 'Водитель',
    'Машиностроние_keys.csv': 'Инженер по машиностроению',
    'Топливо_keys.csv': 'Инженер-технолог',
    'Торговля_keys.csv': 'Торговец',
    'Финансы_keys.csv': 'Финансист',
    'Электроника_keys.csv': 'Инженер по электронике радиотехнике',
    'Agronom_keys.csv': 'Агроном',
    'Architect_keys.csv': 'Архитектор',
    'Biology_keys.csv': 'Биолог',
    'Books_keys.csv': 'Филолог',
    'Botanic_keys.csv': 'Ботаник',
    'Business_keys.csv': 'Бизнесмен',
    'Electronic_keys.csv': 'Инженер по электронике радиотехнике',
    'IT_keys.csv': 'IT-специалист',
    'Repair_car_keys.csv': 'Автомеханик',
    'Sheeve_keys.csv': 'Швея-кройщица',
    'WebDesign_keys.csv': 'Веб-дизайнер'
}

dfs = []

for file_name, profession in file_mapping.items():
    filename = '/content/drive/MyDrive/hackaton2/keys/' + file_name
    df = pd.read_csv(filename, header=None)
    df['prof'] = profession
    dfs.append(df)

result_df = pd.concat(dfs, ignore_index=True)

result_df.to_csv('/content/drive/MyDrive/hackaton2/Full_keys.csv', index=False)


    
