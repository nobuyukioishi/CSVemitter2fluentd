import pandas as pd
import argparse
from fluent import sender
import time

parser = argparse.ArgumentParser()
parser.add_argument("-f","--file", help="set the filepath to be loaded")
parser.add_argument("-t","--tag", help="set the tag name to be sent")
parser.add_argument("-hd","--header", help="specify headers if your file doesn't have headers")
parser.add_argument("-i","--index", help="set the index column")
parser.add_argument("-s","--sep", help="specify the separator; default: ','") # 未実装
parser.add_argument("--host", help="set the host address where fluentd is working")
parser.add_argument("--port", help="set the port number where fluentd is working")

## 処理1 CSVファイルにヘッダもあるし，タイムスタンプもついている
## 処理2 CSVファイルにヘッダはあるけど，タイムスタンプは付いていない (1秒間隔で動作する)
## 処理3 CSVファイルにヘッダはないが，タイムスタンプは付いている
## 処理4 CSVファイルにヘッダは付いていないし，タイムスタンプも付いていない

#def tag_

args = parser.parse_args()
print(args)

host = args.host if args.host else 'localhost'
port = args.port if args.port else 24224
tag = args.tag if args.tag else 'csv-emitter2fluentd'
logger = sender.FluentSender(tag, host=host, port=port)

if args.file:
    df = pd.read_csv(args.file)
    print(df.index)
    # print(df)
    print(df.columns)
    # for remote fluent
    i = 0
    while(i < len(df.index)):
        cur_time = int(time.time()) # when not specified
        logger.emit_with_time('', cur_time, df.loc[i].to_dict())
        time.sleep(1.0)
        i += 1
