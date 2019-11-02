import psycopg2
import math
from datetime import datetime

#connection params
host='localhost'
user='naziba'
password='postgres'
raw_db='bitcoin_historical_data'
warehouse_db='data_warehouse'

#extract all the data from the table in db
def extract(table_name):
    conn = psycopg2.connect(host=host, dbname=raw_db, user=user, password=password)
    cur=conn.cursor()
    select_query="select * from "+table_name
    cur.execute(select_query)
    raw_data=cur.fetchall()
    cur.close()
    conn.close()
    return raw_data

#remove the entries with all null fields as that depicts no transactions took place
#also convert unix timestamps into separate date and time fields to make querying easier
def transform(raw_data):
    updated_data=[]
    ind=0
    for row in raw_data:
        #when the field is nan, field value!=field value
        if all(field==field for field in row[1:]):
            date_time=datetime.utcfromtimestamp(row[0]).strftime('%Y-%m-%d %H:%M:%S').split(' ')
            date=date_time[0]
            time=date_time[1].split(':')
            updated_data.append((ind,date_time[0],date_time[1])+row[1:])
            ind+=1
    return updated_data

#load the data to warehouse db
def load(updated_data,table_name):
    conn = psycopg2.connect(host=host, dbname=warehouse_db, user=user, password=password)
    cur=conn.cursor()
    #create the table
    cur.execute("""
    CREATE TABLE """+table_name+"""(
    id int PRIMARY KEY,
    Date date,
    Time time,
    Open float,
    High float,
    Low float,
    Close float,
    Volume_BTC float,
    Volume_Currency float,
    Weighted_Price float)""")
    conn.commit()
    insert_query=""" INSERT INTO """+table_name+""" 
    (id, Date, Time, Open, High, Low, Close, Volume_BTC, Volume_Currency, Weighted_Price) 
    Values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    for row in updated_data:
        cur.execute(insert_query,row)
        conn.commit()
    cur.close()
    conn.close()   

def etl():
    for table_name in ['bitstampusd','coinbaseusd']:
        raw_data=extract(table_name)
        updated_data=transform(raw_data)
        load(updated_data,table_name)

if __name__=='__main__':
    etl()