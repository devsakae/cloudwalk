import csv, time, sys
import mysql.connector as mysql
from datetime import datetime
from flask import Flask, jsonify, request, after_this_request
from anomaly_rules import check_transactions

bold = '\033[1m'
cyan = '\033[96m'
end = '\033[0m'

app = Flask(__name__)
db = mysql.connect(user='root', password='password', host='localhost')
cursor = db.cursor(buffered=True)
cursor.execute("CREATE DATABASE IF NOT EXISTS cloudwalk")

def menu():
  print(f"""\n{cyan}Anomaly detector simple script for Cloudwalk (created by Rodrigo Sakae){end}\n
 Option [1]: Get your hands dirty
 Option [2]: Solve the problem
 
 Type any other char to cancel
 """)
  answer = input(">> Please type the option: ")
  if answer == "1":
    checkouts()
  elif answer == "2":
    transactions()
  else:
    print('Cancelling...')
    time.sleep(1)

def checkouts():
  print('Task 3.1 script: Get your hands dirty')
  cursor.execute('DROP TABLE IF EXISTS cloudwalk.checkouts')
  cursor.execute('''CREATE TABLE cloudwalk.checkouts (
    time VARCHAR(5) primary key,
    today INT,
    yesterday INT,
    same_day_last_week INT,
    avg_last_week FLOAT(5, 3),
    avg_last_month FLOAT(5, 3)
    )''')
  populate(input('>> Please type the CSV filename (without .csv): '))
  
def transactions():
  print('Task 3.2 script: Solve the problem')
  cursor.execute('DROP TABLE IF EXISTS cloudwalk.transactions')
  cursor.execute('''CREATE TABLE cloudwalk.transactions (
    time VARCHAR(10) PRIMARY KEY NOT NULL,
    approved FLOAT(7, 3),
    backend_reversed FLOAT(7, 3),
    denied FLOAT(7, 3),
    failed FLOAT(7, 3),
    processing FLOAT(7, 3),
    refunded FLOAT(7, 3),
    reversed FLOAT(7, 3)
    )''')
  populate_table = input(">> Populate table with data? (Y/n): ") or "Y"
  if populate == "Y" or "y":
    now = datetime.now()
    time_created = f'{now.strftime("%H")}h{now.strftime("%M")}m{now.strftime("%S")}s'
    cursor.execute('''INSERT INTO cloudwalk.transactions (
      time,
      approved,
      backend_reversed,
      denied,
      failed,
      processing,
      refunded,
      reversed
      )
      VALUES (%s, 182.927, 0.751, 21.346, 0.504, 0.386, 0.584, 6.729)''', [time_created])
  db.commit()
  app.run(host='0.0.0.0') 

def populate(filename):
  try:
    csv_file = open(f'data/{filename}.csv', mode='r')
  except:
    return print('File not found on folder "data"')
  csv_reader = csv.reader(csv_file)
  header = next(csv_reader)
  for row in csv_reader:
      sql = "INSERT INTO cloudwalk.checkouts (time, today, yesterday, same_day_last_week, avg_last_week, avg_last_month) VALUES (%s,%s,%s,%s,%s,%s)"
      cursor.execute(sql, tuple(row))
  print(f"Data from {filename}.csv inserted to database")
  db.commit()
  if input('>> Run anomaly detector? (Y/n) ') == 'n':
    print('** Terminating script **')
    return cursor.close()
  index = int(input('>> Choose anomaly index (default 2): ') or 2)
  anomaly(index)
  
def anomaly(index):
  query = f"SELECT time, TRUNCATE((today - ((same_day_last_week + avg_last_week + avg_last_month) / 3)),2) AS variation FROM cloudwalk.checkouts WHERE TRUNCATE((today - ((same_day_last_week + avg_last_week + avg_last_month) / 3)),2) < ({index} * -1)"
  cursor.execute(query)
  result = cursor.fetchall()
  if result:
    for x in result:
      print(x)
  else:
    print('No data found. Using default index (3)...')
    anomaly(3)

def get_transactions(mode):
  if (mode == "all"):
    query = "SELECT * FROM cloudwalk.transactions"
  elif (mode == "avg"):
    query = "SELECT AVG(failed) AS avg_failed, AVG(denied) AS avg_denied, AVG(reversed) AS avg_reversed FROM cloudwalk.transactions"
  try:
    to_dict_cursor = db.cursor(dictionary=True)
    to_dict_cursor.execute(query)
    result = to_dict_cursor.fetchall()
    if result:
      return check_transactions(result)
  except:
    return { "message": "Database error" }

def save_transactions():
  now = datetime.now()
  total = 0
  data_dict = {
      "time": f'{now.strftime("%H")}h{now.strftime("%M")}m{now.strftime("%S")}s',
      "approved": 0,
      "backend_reversed": 0,
      "denied": 0,
      "failed": 0,
      "processing": 0,
      "refunded": 0,
      "reversed": 0
    }
  try:
    for info in request.get_json():
      item = request.get_json()[info]
      data_dict[info] = item
      total += int(item)
    query = "INSERT INTO cloudwalk.transactions (time, approved, backend_reversed, denied, failed, processing, refunded, reversed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, list(data_dict.values()))
    db.commit()
    return { "message": "Data saved" }
  except:
    return { "message": "Something wrong with your payload, maybe?" }

@app.route('/', methods=['GET', 'POST'])
def index():
  if (request.method == 'POST'):
    return jsonify(save_transactions())

  if (request.method == 'GET'):
    @after_this_request
    def add_header(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    data = get_transactions('all')
    return jsonify(data)

if __name__ == '__main__':
  menu()