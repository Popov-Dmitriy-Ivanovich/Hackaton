import pandas as pd
import pymorphy2
from sklearn.preprocessing import LabelEncoder 


#Даем уникальные значения каждому слову 
filename = '/content/drive/MyDrive/hackaton2/Full_keys.csv'
df = pd.read_csv(filename)  
print(df)

df['0'] = df['0'].str.lower()

morph = pymorphy2.MorphAnalyzer() #Приводит слово в нормальный вид (мыла -- мыть итд)

df['lemmas'] = df['0'].apply(lambda x: morph.parse(x)[0].normal_form)

label_encoder = LabelEncoder()
df['cipher'] = label_encoder.fit_transform(df['lemmas']) # Придает каждому слову уникальный идентификатор 

df.drop('lemmas', axis=1, inplace=True)

print(df[['0', 'cipher', 'prof']])
df.to_csv('Full_keys.csv',  index=False)

# Зачем мы приводили слово в нормальный вид? Чтобы дизайн/дизайна/Дизайном -- имели одинаковый код (для точности модели)