
import linecache
print(bool(linecache.getline('sample.log', 1)))
print(linecache.getline('sample.log', 100))
