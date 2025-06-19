import json
import sqlite3

# Sample JSON data (replace this with your actual JSON data)
with open(r'F:\School\Computer Science\Senior Project\medical-codex-backend\blond_maggots\codex_cleaned.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# Create or connect to the SQLite database
conn = sqlite3.connect('medicines.db')
cursor = conn.cursor()

# Create a table to store medicine data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS medicines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        label_uk TEXT,
        label_ru TEXT,
        label_gr TEXT,
        label_en TEXT,
        alias_list_uk TEXT,
        alias_list_ru TEXT,
        alias_list_gr TEXT,
        alias_list_en TEXT
    )
''')

# Insert data into the table
for item in json_data:
    cursor.execute('''
        INSERT INTO medicines (label_uk, label_ru, label_gr, label_en, alias_list_uk, alias_list_ru, alias_list_gr, alias_list_en)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        item['label_uk'],
        item['label_ru'],
        item['label_gr'],
        item['label_en'],
        ', '.join(item['alias_list_uk']),
        ', '.join(item['alias_list_ru']),
        ', '.join(item['alias_list_gr']),
        ', '.join(item['alias_list_en']),
    ))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Data has been successfully dumped into the SQLite database.")
