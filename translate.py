#!/usr/bin/python3
import re
#transfer curl command to dictionary
import getopt
#getopt通常认为数据是放在最后的
import urllib.parse 
__doc__=r'''
getopt相关信息：getopt.getopt(argv,short_opt,long_opt)
		argv是数组，必须满足如下要求：数据最后出现 
		short_opt 是短字符串，如果需要一个参数，使用:
		long_opt是数组，形如 ['long=','help']
		返回值是[二元组,数据]
	
httplib2.Http.request(uri,method,body,headers)

json
	dumps(pyobj)------>json
	loads(jsonstr)---------->python object
	
urllib.parse.quote(string,safe='/',encoding)
'''

__help__=r'''翻译英文'''
def transeFromCurl(s):
	argvData=transeToArgv(s)
	sdata=getopt.getopt(argvData,'H:',['data='])
	return sdata[0]
	
def transeToArgv(s):
	res=[]
	itemRegex=re.compile(r'''('[^']+'\s+|\S+)''')
	s=s.lstrip()
	fres=re.findall(itemRegex,s)
	for i,res in enumerate(fres):
		if res[0]=="'":
			fres[i]=res[1:res.rfind("'")]
	return fres
		
		
#-----start 
import sys
#myquery='do you have any thing like 小明'
myquery=sys.argv[1]
if myquery=='help':
	print(__help__)
	exit()
qMyquery=urllib.parse.quote(myquery,encoding='u8')
mydata=transeFromCurl(r"""-H 'Accept: */*' -H 'Accept-Language: zh-CN,en-US;q=0.7,en;q=0.3' -H 'Connection: keep-alive' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'DNT: 1' -H 'Host: fanyi.baidu.com' -H 'Referer: http://fanyi.baidu.com/' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0' -H 'X-Requested-With: XMLHttpRequest' --data 'from=en&to=zh&query="""+qMyquery+"""&transtype=translang&simple_means_flag=3' """)

import httplib2
hr=httplib2.Http()
headers={}
data=b''
for i in mydata:
	if i[0]=='-H':
		sIndex=i[1].find(':')
		headers[i[1][:sIndex]]=i[1][sIndex+1:]
	elif i[0]=='--data':
		data=i[1].encode('u8')
		

resp,content=hr.request('http://fanyi.baidu.com/v2transapi','POST',headers=headers,body=data)

import json
jsondata=json.loads(content.decode('u8'))
print(jsondata['trans_result']['data'][0]['dst'])
