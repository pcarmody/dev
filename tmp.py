#
import json
from pprint import pprint

json_file='/home/paul/bin/data/sunmoon_201803'

json_data=open(json_file)#.read()
data = json.load(json_data)
#pprint(data)
json_data.close()

print data[6]
json_file='/home/paul/bin/data/tides_201803'
json_data=open(json_file)#.read()
data = json.load(json_data)
json_data.close()

print data[6]
