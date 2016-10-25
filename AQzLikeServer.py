#!/usr/bin/python3
#-*-coding:utf8;-*-
#qpy:3
#qpy:console

__version__="0.91"
__author__="Fulton Shaw"
__doc__='''
脚本启动：
	命令行参数被完整传递到initShares.py脚本中，存储在s.argv中
	定义函数模式如下:
	def generate_html(s):
		...<python coding here>...
		return [code,data,response]
		code分别取0,1,2,3代表regular,redirect,send-data,completed;基本而言，如果返回的数据是可编码（str）类型，都会使用regular选项，send-data通常是为二进制数据准备的。

服务器规则：
	依据s.path来定位资源
	s.path为'/'直接永久重定向到'/{homepage}'
	s.path为存在相应的${s.path}.py文件，执行这个py文件后返回 。因此服务器内部不允许存在非法的.py文件//replace .html or with .py
	s.path不存在.py文件，如果是html或者htm文件，直接返回这个html；否则返回资源文件
	如果找不到,即返回404 NOT FOUND

配置文件规则：
	配置文件内容  
			name=value
	其中name不允许含有空格,value可以含有空格
	配置文件的内容被传递到s.setups中（数据结构：字典）
	配置文件必须至少包含一项：htmlpath-->s.html_dir
	如果还使用了数据库，还应当包含:database-->s.dbs
	在lib中添加想要导入的库
'''

import socket as s
import sys#for stdin
import os,re
import time
import importlib
import filecmp #可以使用md5进行比较,hashlib.md5 或者md5包
from urllib.parse import unquote_to_bytes
#可以浏览日志，提交日志
#浏览临时根据模板构造网页

import http.server as hs
import sqlite3 as sq
import sys

#get current directory
#遍历sys.argv,第一个.py文件就是执行的文件

def getPyFile(argv):
	for i in argv:
		if i.endswith(".py") and os.path.isfile(i):
			return i

pydir=os.path.split(getPyFile(sys.argv))[0]
print("pydir:",pydir)


#将lib加入搜索路径
sys.path.append(os.path.join(pydir,"lib"))

#local librarys,from $html_dir/lib
import fulton_utils.lib_system.socketserver_fulton as sf
import fulton_utils.lib_system.htmlutil_fulton as hf
import fulton_utils.lib_system.util_fulton as util_fulton

#指定配置文件
#AQzLikeServer.ini 与 AQzLikeServer.py必须在同一个目录
print("sys.argv : ",sys.argv)
setupfile=pydir+"/AQzLikeServer.ini"
print("setupfile : ",setupfile)
setups=util_fulton.readSetupFile(setupfile)
print("setups : ",setups)


#调用初始化脚本
#htmlpath=util_fulton.get(sys.argv,1,None,'') #原来的类型是通过命令行指定，现在的命令行参数被传递到initShares.py
htmlpath=setups.get('htmlpath','./html')
print("htmlpath :",htmlpath)
leftargs=util_fulton.get(sys.argv,1,len(sys.argv),[])

#@depreciated use datetime.strftime("%Y-%m-%d
def formatTime(s,t):
	__doc__='''to format time return to client , showed in the HTML file'''
	a=time.localtime(t) #转化为time_struct
	subfmt='0>2d'
	datefmt='{1}.{2:{0}}.{3:{0}} {4:{0}}:{5:{0}}:{6:{0}}'
	b=datefmt.format(subfmt,a.tm_year,a.tm_mon,a.tm_mday,a.tm_hour,a.tm_min,a.tm_sec)
	
	return b


class LocalHandler(hs.BaseHTTPRequestHandler):
	#要求s的所有变量都为与模块无关的绝对变量，这是因为需要频繁地传递变量
	#下面这些变量被传递到init中进行
	#content_fmt='''<pre>{content}
	#<i>[{date}]</i><a href='/delete.html?id={id}'>删除</a></pre>'''
	#dbs=database_dir+'/AQzLike.db'


	def do_POST(s):
		return s.do_GET()
	def do_GET(s):
		if s.path=='/':
			hf.send_redirect(s,s.homepage,301)
		else:
			#已经排除s.path='/'的情况,所以s.path='/x+'
			#调用html下相应的.py文件
			#import不能是变量，所以通过import构造的方法不能实现服务器路径
			#通过生成html的方式来实现数据交换，缺点是：每一次都需要重新生成页面，而不是只在需要更新的部分生成。实际上所要求的仅仅是动态的部分而已
			#通过脚本的方式传递参数给.py，使之重新构造出一个s对象，然后再进行传输即可，譬如 ./index.py 192.168.199.1 20  
			#但是由于这个脚本所要做的仍然是仅仅发送一个html，响应头部分仍然得由此处发送，所以将其设计为一个本地函数，返回html即可



			#使用__import__函数或者importlib.import 函数即可
			#由于文件名中可能含有.，而lib中是不允许这样的，首先将所有的_换成__,再将.换成_即可。这个使用transPath函数实现

			#index.html.py也就是index_Pointhtml.py
			#htmlib=index_Pointhtml

			#解析s.path,首先s.path是规范化的，即形如'/','/dfas',不能以'/'结尾('/'除外)

			dataIndex=s.path.find('?')
			if dataIndex==-1:
				formattedPath=s.path
			else:
				formattedPath=s.path[:dataIndex]

			splitIndex=formattedPath.rindex('/')
			htmlpath=util_fulton.get(formattedPath,0,splitIndex,'')
			htmlname=util_fulton.get(formattedPath,splitIndex+1,len(formattedPath),'')

			import os.path
			#如果有py文件，优先返回其py文件的执行结果，否则直接返回该文件
			copath=s.html_dir+formattedPath
			if copath.endswith('.html') and os.path.exists(copath.replace('.html','.py')):
				libname=htmlname.replace('.html','')
				htmlib=util_fulton.local_import(s.html_dir+htmlpath,libname)#导入函数
				res=htmlib.generate_html(s)  #返回页面或者重定向信息,这些
				#返回值重新定义：code={0,1,2},data={},response={},尽在code=redirect的时候response可选
				rtnCode=util_fulton.get(res,0,None,-1)
				rtnData=util_fulton.get(res,1,None,'')
				rtnResponse=util_fulton.get(res,2,None,302)
				#使用脚本的返回类型包括：页面{重定向，目标页面}，数据
				#print(html)
				#input('按任意键继续...')
				if s.rtnCode[rtnCode]=='regular':
					hf.send_html(s,rtnData)
				elif s.rtnCode[rtnCode]=='redirect':
					hf.send_redirect(s,rtnData,rtnResponse)
				elif s.rtnCode[rtnCode]=='send-data':
					hf.send_data(s,rtnData)#without encoding
				elif s.rtnCode[rtnCode]=='completed':#自定义
					pass
				else:
					hf.send_internerror(s)
			elif os.path.exists(copath) and os.path.isfile(copath):
				with open(copath,'rb') as f:
					if copath.endswith('.html') or copath.endswith('.htm'): #判断请求的资源类型
						hf.send_html(s,f.read())
					else:
						hf.send_data(s,f.read())

			else:
				hf.send_notfound(s)

#此处赋予LocalHandler全局编程性质
LocalHandler.sf=sf
LocalHandler.hf=hf
LocalHandler.hs=hs
LocalHandler.sq=sq
LocalHandler.uf=util_fulton
LocalHandler.formatTime=formatTime
LocalHandler.helpinfo=__doc__
LocalHandler.rtnCode=['regular','redirect','send-data','completed']

sharelib=util_fulton.local_import(htmlpath,'initShares')
#传递一系列的参数初始化环境
sharelib.init(handler=LocalHandler,setups=setups,leftargs=leftargs)


svr=hs.HTTPServer(('',5533),LocalHandler)
__helpinfo__=r'''about
	server	:Fulton python server based on http.server.HTTPServer
	copyright: Copyright 2016 Douglas Fulton Shaw
	version : '''+__version__+r'''
'''
print(__helpinfo__)
try:
	print("Serving starting,now listening...")
	svr.serve_forever()
except:
	pass

print("Server ending...")
svr.server_close()
