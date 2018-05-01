import argparse
from fluent import sender
import time
import json
from datetime import datetime as dt

## setting of arguments
parser = argparse.ArgumentParser()
parser.add_argument("-f","--file", help="set the filepath to be loaded")
parser.add_argument("--host", help="set the host address where fluentd is working")
parser.add_argument("--port", help="set the port number where fluentd is working")
args = parser.parse_args()
# print(args)
host = args.host if args.host else 'localhost'
port = args.port if args.port else 24224


# only when a log-file is specified
if args.file:
    f = open(args.file, 'r')
    lines = f.readlines() # 1行毎にファイル終端まで全て読む(改行文字も含まれる)
    n_lines = len(lines)
    f.close()
    is_first = True
    for line in lines:
        line_json = json.loads(line)
        tag = line_json['tag']
        c_time = dt.strptime(line_json['time'], "%Y-%m-%dT%H:%M:%S+09:00")
        del line_json['tag']
        del line_json['time']
        record = line_json
        if is_first:
            logger = sender.FluentSender(tag, host=host, port=port)
            logger.emit_with_time('', int(time.time()), record)
            is_first = False
            p_time = c_time # 次のために取っておく
        else:
            # calc time_d
            timegap = (c_time - p_time).total_seconds()
            # print("timegap is",timegap)

            # start と counter でtimegapを監視する
            start = int(time.time())
            counter = 0
            while timegap > counter:
                counter = int(time.time()) - start
                # print(counter)
                time.sleep(0.1)
            # create a fluent-logger object
            logger = sender.FluentSender(tag, host=host, port=port)
            logger.emit_with_time('', int(time.time()), record)
            p_time = c_time
else:
    print("specify a path of your json-type logfile.")
