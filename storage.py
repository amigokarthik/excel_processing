import urllib2
import zipfile
import os
import io
import csv, redis, json
import sys
import sched, time
from collections import OrderedDict
import datetime
from datetime import date, timedelta

s = sched.scheduler(time.time, time.sleep)

r = redis.StrictRedis(host="localhost", port=6379, db=0)

# method to parse csv file and store its data in list
def read_csv_data(csv_file):
    with io.open(csv_file, encoding='utf-8') as csvf:
        csv_data = csv.reader(csvf)
        temp_tuple = ()
        temp_list= []
        for r in csv_data:
            for i in range(0,len(r)):
                temp_tuple = temp_tuple + (r[i],)
            temp_list.append(temp_tuple)
            temp_tuple = ()
        return temp_list

# method to store csv data in redis db
def store_data(r, data):
    begin_tuple = data[0]
    for i in range(1,len(data)):
        key = str(i-1) + "- " + data[i][1]
        temp_dictionary = {}
        j = 0
        while(j<len(data[i])):
            temp_dictionary[begin_tuple[j]] = data[i][j]
            j = j+1
        r.hmset(key, temp_dictionary)

# method to extract zip file
def extract_zip():
    zip_ref = zipfile.ZipFile('equity.zip', 'r')
    zip_ref.extractall(os.getcwd())
    zip_ref.close()

# method to pass data to various files and clear files after storing their data in redis
def process(csv):
    # read csv and store in redis as key value pairs
    data = read_csv_data(csv)
    store_data(r, data)
    cwd = os.getcwd()
    files = os.listdir(cwd)
    for item in files:
        if (item.endswith(".zip")) or (item.endswith(".CSV")):
            os.remove(os.path.join(cwd, item))

# scheduler function runs every 24 hours and updates redis data
def scheduler(sc):
    r.flushall()
    e_date = date.today() - timedelta(1)
    u_date = e_date.strftime('%y%m%d')
    dd = datetime.datetime.strptime(u_date,'%y%m%d')
    year = str(dd.year)[2:]
    str_month = str(dd.month)
    if len(str_month) < 2:
        str_month = '0' + str_month
    str_day = str(dd.day)
    if len(str_day) < 2:
        str_day = '0' + str_day
    zip_url = 'https://www.bseindia.com/download/BhavCopy/Equity/EQ' + str_day + str_month + year + '_CSV.ZIP'
    response = urllib2.urlopen(zip_url)
    html = response.read()
    output = open("equity.zip", "w")
    output.write(html)
    output.close()
    extract_zip()
    csv = 'EQ' + str_day + str_month + year + '.CSV'
    process(csv)
    s.enter(86400, 1, scheduler, (sc,))

if __name__ == '__main__':
    s.enter(2, 1, scheduler, (s,))
    s.run()
