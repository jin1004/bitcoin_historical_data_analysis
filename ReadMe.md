## Project Overview
This repository contains different database operations and analysis using bitcoin historical data by Kaggle

## Main requirements
Python3
Anaconda, Jupyter
PostgreSQL

## Loading the files to database
The files are loaded to the database using load_to_db.py
We can then check if everything was loaded properly to the db using Postico or other PostgreSQL Client
![Alt text](https://github.com/jin1004/bitcoin_historical_data_analysis/blob/master/images/raw_db1.png)
![Alt text](https://github.com/jin1004/bitcoin_historical_data_analysis/blob/master/images/raw_db2.png)

## Extract, Transform and Load
For this project, I have created a separate database on PostgreSQL to be the data warehouse. 
From the raw data, only valid transactions are kept and the timestamps are transformed to regular date and time format so that it becomes easier to query the data for any future task.

Snapshot of a transformed table in the warehouse db:
![Alt text](https://github.com/jin1004/bitcoin_historical_data_analysis/blob/master/images/warehouse_db1.png)

The ETL functions are in the etl.py file.

In order to schedule the script to run at intervals, the easiest way is to use cron for linux/mac and task manager for windows.
> ##To-Do
> Set up Apache Airflow and use it to schedule and monitor the ETL functions being performed on incoming new data since that would be much better than  having platform-dependent task schedulers and managers.

## Analysis on the data

The "bitcoin_data_analysis.ipynb" notebook consists of all the visualizations and analysis.

>##To-Do
> Do a time-series analysis (ARIMA model) for price forecasting
> Do some more experimentations with the data to see if any interesting insights can be found

## Real time suspicious pricing alerts.

>##To-Do
>Prepare anomaly detection function by modelling regular price patterns to figure out when the price seems like an anomaly
>Run anomaly detection function on incoming new data using the task manager pipeline

## BI Architecture

![Alt text](https://github.com/jin1004/bitcoin_historical_data_analysis/blob/master/images/bi_pipeline.png)

In order to plan a detailed architecture and decide exactly which tools to use, I feel like it's important to know way more details about the business and the current state of things such as what the incoming data sources are, which areas primarily need optimization, resources available etc.