
def get_content(f):
	data=""
	with open(f,encoding="u8") as cf:
		data=cf.read()
	return data


#对任何具有 key:value的数据进行解析,返回键:值列表
import re
def parse_data(data,pattern):

	#编译正则表达式
	pattern_setting=re.M|re.VERBOSE
	ptrn=re.compile(pattern,pattern_setting)
	rdata=re.findall(ptrn,data)
	
	#生成列表,对应于数据库的顺序,网页端也必须保持同样的顺序
	#必须保持顺序
	return rdata

def parse_keyvalue(data):
	pattern=r'''
		\{?\s? #match empty start
		([^:]*):([^,]*)  #key:value
		(?:,|\})  #match empty end
	'''
	return parse_data(data,pattern)
	

def generate_html(s):
	return [0,""]
