#!/usr/bin/env python
### you have to send the header to do an auth on services that dont return a 401 on login.... why? 
import urllib2, base64
import json
import sys


username = sys.argv[1]
password = sys.argv[2]
host = sys.argv[3]

bucket_url = "/pools/default/buckets"
url = 'http://' + host + ':8091' + bucket_url

request = urllib2.Request(url)
# You need the replace to handle encodestring adding a trailing newline 
# (https://docs.python.org/2/library/base64.html#base64.encodestring)
base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
request.add_header("Authorization", "Basic %s" % base64string)   
result = urllib2.urlopen(request)


data = json.load(result)
#print json.dumps(data)
#print(data)

print len(data), "buckets"

print '||Cluster||Bucket Name||Bucket Password||Bucket Type||Bucket Size||Bucket % used ||'
for buckets in data:
    print  ' | ' + host + ' | ' + buckets['name'] + ' | ' +  buckets['saslPassword'] + ' | ' + buckets['bucketType'] + ' | ' + str(buckets['quota']['ram']/1024/1024) + ' MB' + ' | '  + str(buckets['basicStats']['quotaPercentUsed']) + '%' + ' | '


