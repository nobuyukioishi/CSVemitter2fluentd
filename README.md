# log-emitter2fluentd

I'm developing this to help you take your hassle out of the process of testing and debugging fluentd. Once you created a sample log file as shown below, you can recycle the data in your log file again and again with just one command-line execution!

## For your quick try

```
python emitter2fluentd-json.py -f sample.log
```
*fluentd must be running on your local environment

## How to create a sample log file

Add this to your fluentd configuration file and you'll see your log file at your ./log/json. The filename will be like ```buffer.**.log```

```
<match tag.to_log>
  @type file
  path ./log/json/
  format json
  include_time_key true
  include_tag_key true
</match>
```

## How to use emitter2fluentd-json.py

After creating your sample log file, you'll be able to emit fluentd events as many times as you need with the command following:

```
python emitter2fluentd-json.py -f path2yourlogfile --host 9199 --port localhost
```

Tag emission interval will be calculated from the log file to reproduce the same condition as you created the log file.


### help message
```
-h, --help            show this help message and exit
-f FILE, --file FILE  set the filepath to be loaded
--host HOST           set the host address where fluentd is working
--port PORT           set the port number where fluentd is working
```
