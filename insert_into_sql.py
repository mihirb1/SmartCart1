import pandas as pd
import mysql.connector

csv_file = "amazon_products1.csv"
data = pd.read_csv(csv_file)


data = data.fillna({

    'title': 'Unknown',
    'total price': 0.0,
    'price per unit': 0.0,
    'unit': 'Unknown',
    'link': 'Unknown',
    'availability': 'Unknown',
    'source': 'Unknown'
})
data['link'] = 'https://www.amazon.com' + data['link']
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="products"
)
cursor = conn.cursor()

for _, row in data.iterrows():

    sql = """
    INSERT INTO products (`title`, `total_price`, `price_per_unit`, `unit`, `link`, `availability`, `source`)
    VALUES (%s, %s, %s, %s, %s, %s, 'Amazon')
    """
    try:
        cursor.execute(sql, tuple(row))
    except Exception as e:
        print(e)

conn.commit()
cursor.close()
conn.close()

print("Data import successfully!")