import linecache
import argparse

from fluent import sender
import time
import json
from datetime import datetime as dt

## setting of arguments
parser = argparse.ArgumentParser()
parser.add_argument("-f","--file", action='append', default=[],help="set the filepath to be loaded")
parser.add_argument("-t","--timezone", default="+09:00", help="set the timezone of your environment")
parser.add_argument("--host", help="set the host address where fluentd is working")
parser.add_argument("--port", help="set the port number where fluentd is working")
args = parser.parse_args()
print(args)
files = args.file
host = args.host if args.host else 'localhost'
port = args.port if args.port else 24224
t = args.timezone
candidates = []
counters = [1 for i in range(len(files))]

def update(i):
    counters[i] += 1 # counterを更新
    if linecache.getline(files[i], counters[i]) != '':
        line_json = json.loads(linecache.getline(files[i], counters[i])) # i行目を取得してjsonに変換
        candidates[i] = line_json # candidatesを更新
        timestamps[i] = dt.strptime(line_json['time'], "%Y-%m-%dT%H:%M:%S"+t)
        # print("updated! candidates["+str(i)+"] is now",candidates[i])
        return True
    else:
        candidates[i] = ''
        timestamps[i] = dt.max
        # reached to the end of the files
        return False


def get_min_timestamp_indices(timestamps):
    # print(timestamps)
    min_timestamp = min(timestamps)
    # print("next emittion is of", min_timestamp)
    indices = [i for i, x in enumerate(timestamps) if x == min_timestamp]
    return indices

def check():
    flag = False
    for item in candidates:
        if bool(item) == True:
            flag = True
    # print("check() returned", flag)
    return flag

# only for first lines of the files
lines = []
for i in range(len(files)):
    lines.append(linecache.getline(files[i], counters[i]))


timestamps = []
for line in lines:
    line_json = json.loads(line)
    candidates.append(line_json)
    tag = line_json['tag']
    timestamps.append(dt.strptime(line_json['time'], "%Y-%m-%dT%H:%M:%S"+t))
c_time = timestamps[get_min_timestamp_indices(timestamps)[0]] # list -> int

# ここで，取り出す要素が決まったので，それを取り出す
# 流すための要素が作られる
is_first = True
is_last = False
while(check()):
    # print("min_indices are", get_min_timestamp_indices(timestamps))
    for index in get_min_timestamp_indices(timestamps):
        # print("subject:",candidates[index])
        tag = candidates[index]['tag']
        c_time = dt.strptime(candidates[index]['time'], "%Y-%m-%dT%H:%M:%S"+t)
        del candidates[index]['tag']
        del candidates[index]['time']
        # print("candidates["+str(index)+"]","after deleted")
        record = candidates[index]
        if is_first:
            logger = sender.FluentSender(tag, host=host, port=port)
            logger.emit_with_time('', int(time.time()), record)
            print(str(c_time), record)
            is_first = False
            p_time = c_time
            update(index) # update candidates, timestamps of the ndex
        else:
            # calculate timegap
            timegap = (c_time - p_time).total_seconds()
            # print("timegap is",timegap)

            # watch elapsed time
            time_counter = 0
            start = int(time.time())
            while timegap > time_counter:
                time_counter = int(time.time()) - start
                time.sleep(0.1)

            # create a fluent-logger object
            logger = sender.FluentSender(tag, host=host, port=port)
            logger.emit_with_time('', int(time.time()), record)
            print(str(c_time),record)
            p_time = c_time
            update(index)
