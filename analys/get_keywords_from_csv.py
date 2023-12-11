import os
import pandas as pd

directory_path = '/content/drive/MyDrive/hackaton/'

csv_files = [file for file in os.listdir(directory_path) if file.endswith('.csv')] # Считываем все css которые есть в папке

for csv_file in csv_files:
    file_path = os.path.join(directory_path, csv_file)
    df = pd.read_csv(file_path, header=None)

    books_keys = [] # Проходимся по всем столбцам (бесконтрольно, потом просто очистим эти данные от выбросов: цифр, букв, и проч)
    for column in df.columns:
        for value in df[column]:
            if pd.notna(value):
                for word in str(value).split():
                    books_keys.append(word)

    keys_df = pd.DataFrame(books_keys)
    keys_file_path = os.path.join(directory_path, f'{csv_file.split(".")[0]}_keys.csv') # Сохраняем в формате "имя_файла"+keys
    keys_df.to_csv(keys_file_path, mode='w', header=False, index=False)