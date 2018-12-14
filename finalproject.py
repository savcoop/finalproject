import requests 
import json 
import sqlite3
from darksky import forecast
import matplotlib.pyplot as plt

url = 'https://api.darksky.net/forecast'
secret_key = '908f42d521e235766df615ee6da7fb3f'

def temperatureDatabase():
        """
        This function creates a SQLite table of “Actual Temperature High,” “Apparent Temperature High,” and the average of the two. 
        It uses the Dark Sky API to pull the two data points from a dictioanary. Dark Sky uses UNIX time, so in order to get 100 data 
        points I calculated August 29th using a UNIX calculator. 
        """
    conn = sqlite3.connect('final.sqlite')
    cur=conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS Temperature (apparentHigh NUMERIC, actualHigh NUMERIC, Average NUMERIC)')
    cur.execute('SELECT * FROM Temperature')
    data = cur.fetchall()
    if len(data) == 100:
        pass
    else: 
        #UNIX time is 100 dats ago since December 7th. Date would be August 29th, 2018
        time = 1535571637
        for x in range(100):
            r = requests.get('https://api.darksky.net/forecast/908f42d521e235766df615ee6da7fb3f/40.742846,-74.0060,{}?exclude=currently,minutely,hourly,alerts,flags'.format(time))
            time += 86400
            app_temp_high = r.json()['daily']['data'][0]['apparentTemperatureHigh']
            temp_high = r.json()['daily']['data'][0]['temperatureHigh']
            avg = (app_temp_high + temp_high) / 2 
            cur.execute('INSERT INTO Temperature (apparentHigh, actualHigh, Average) VALUES (?, ?, ?)',(app_temp_high,temp_high,avg))
        conn.commit()
        cur.execute('SELECT * FROM Temperature')
        data = cur.fetchall()    
    return(data)

def extraDatabase():
    '''
    This function creates a SQLite table of “Actual Temperature Low,” “Apparent Temperature Low,” and the average of the two. 
    It uses the Dark Sky API to pull the two data points from a dictioanary. Dark Sky uses UNIX time, so in order to get 100 data 
    points I calculated August 29th using a UNIX calculator. 
    '''
    conn = sqlite3.connect('final2.sqlite')
    cur=conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS Temperature_Low (apparentLow NUMERIC, actualLow NUMERIC, AverageLow NUMERIC)')
    cur.execute('SELECT * FROM Temperature_Low')
    data_e = cur.fetchall()
    if len(data_e) == 100:
        pass
    else: 
        #UNIX time is 100 dats ago since December 7th. Date would be August 29th, 2018
        time = 1535571637
        for x in range(100):
            r = requests.get('https://api.darksky.net/forecast/908f42d521e235766df615ee6da7fb3f/40.742846,-74.0060,{}?exclude=currently,minutely,hourly,alerts,flags'.format(time))
            time += 86400
            app_temp_low = r.json()['daily']['data'][0]['apparentTemperatureLow']
            temp_low = r.json()['daily']['data'][0]['temperatureLow']
            avg_low = (app_temp_low + temp_low) / 2 
            cur.execute('INSERT INTO Temperature_Low (apparentLow, actualLow, AverageLow) VALUES (?, ?, ?)',(app_temp_low,temp_low,avg_low))
        conn.commit()
        cur.execute('SELECT * FROM Temperature_Low')
        data_e = cur.fetchall()    
    return(data_e)

def extraDatabase2():
    '''
    This function creates a SQLite table of “Temperature High,” Temperature Low,” and the average of the two. 
    It uses the Dark Sky API to pull the two data points from a dictioanary. Dark Sky uses UNIX time, so in order to get 100 data 
    points I calculated August 29th using a UNIX calculator. 
    '''
    conn = sqlite3.connect('final3.sqlite')
    cur=conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS Temperature_Average (actualLow NUMERIC, actualHigh NUMERIC, actualAverage NUMERIC)')
    cur.execute('SELECT * FROM Temperature_Average')
    data_e2 = cur.fetchall()
    if len(data_e2) == 100:
        pass
    else: 
        #UNIX time is 100 dats ago since December 7th. Date would be August 29th, 2018
        time = 1535571637
        for x in range(100):
            r = requests.get('https://api.darksky.net/forecast/908f42d521e235766df615ee6da7fb3f/40.742846,-74.0060,{}?exclude=currently,minutely,hourly,alerts,flags'.format(time))
            time += 86400
            temp_low = r.json()['daily']['data'][0]['temperatureLow']
            temp_high = r.json()['daily']['data'][0]['temperatureHigh']
            avg_temp = (temp_low + temp_high) / 2 
            cur.execute('INSERT INTO Temperature_Average (actualLow, actualHigh, actualAverage) VALUES (?, ?, ?)',(temp_low,temp_high,avg_temp))
        conn.commit()
        cur.execute('SELECT * FROM Temperature_Average')
        data_e2 = cur.fetchall()    
    return(data_e2)

data_1 = temperatureDatabase()
data_2 = extraDatabase()
data_3 = extraDatabase2() 


#visualizations  
plt.plot(data_1)
plt.title("Temperature High from August 29th-Decemer 7th")
plt.legend(['Apparent Temperature High', 'Actual Temperature High', 'Average Temperature High'])
plt.xlabel('Time in Days')
plt.ylabel('Temperature')
plt.show()

plt.plot(data_2)
plt.title("Temperature Low from August 29th-Decemer 7th")
plt.legend(['Apparent Temperature Low', 'Actual Temperature Low', 'Average Temperature Low'])
plt.xlabel('Time in Days')
plt.ylabel('Temperature')
plt.show()

plt.plot(data_3)
plt.title("Temperature Low vs. Temperature High from August 29th-Decemer 7th")
plt.legend(['Actual Temperature Low', 'Actual Temperature High', 'Average Temperature'])
plt.xlabel('Time in Days')
plt.ylabel('Temperature')
plt.show()








