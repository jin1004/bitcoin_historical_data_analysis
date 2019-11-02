import psycopg2
import os
import csv

#create connection
host='localhost'
dbname='bitcoin_historical_data'
user='naziba'
password='postgres'
conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
cur=conn.cursor()

dataset_dir=os.getcwd()+('/bitcoin-historical-data/')
for file in os.listdir(dataset_dir):
    #create the table
    table_name=file.split('_')[0]
    cur.execute("""
    CREATE TABLE """+table_name+"""(
    Timestamp bigint PRIMARY KEY,
    Open float,
    High float,
    Low float,
    Close float,
    Volume_BTC float,
    Volume_Currency float,
    Weighted_Price float)""")
    conn.commit()
    #remove brackets from the headers in the csv files
    with open(dataset_dir+file,'r') as f,open(dataset_dir+file+'_updated','w') as out:
        reader=csv.reader(f)
        writer=csv.writer(out)
        header=next(reader)
        header_updated=[]
        for col_name in header: 
            header_updated.append(col_name.replace('(','').replace(')',''))
        writer.writerow(header_updated)
        for line in reader:
            writer.writerow(line)
    #load the file to db
    with open(dataset_dir+file+'_updated','r') as f:
        next(f) #skip the header row
        cur.copy_from(f,table_name,sep=',')
        conn.commit() 