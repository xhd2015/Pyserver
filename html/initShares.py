#!/bin/python3
__doc__='''此处用于存放一个在服务器初始化完毕以后第一个调用的脚本，你可以在其中初始化服务器变量，用于其他页面共享'''

def init(**svr_args):
	handler=svr_args.get('handler',None)
	if handler:
		#这些变量在后面用在s.的后面共享
		handler.content_fmt='''<pre>{content}
<i>[{date}]</i><button onclick="postDeleteData(this);" content_id="{id}">删除</button></pre>'''

		#下面这些与系统相关
		handler.argv=svr_args['leftargs']
		handler.setups=svr_args['setups']
		
		#设置编程的变量
		handler.dbs=handler.setups.get('database','')
		handler.html_dir=handler.setups['htmlpath']
		handler.homepage=handler.setups.get('homepage','/index.html');
		
		#下面这些是示例常量
		#['head']['meta']==list(dict)
		handler.examples=dict()
		metas=[]
		metas.append({'name':'viewport','content':'initial-scale=1.0, minimum-scale=1.0'})
		metas.append({'charset':'utf-8'})
		metas.append({'httpequiv':'content-type' , 'content' : 'text/html; charset=utf-8'})
		
		
		headers=[]
		headers.append({'location':'/index.html','method':'get','response':302})
		headers.append({'host':'localhost:5533'})
		headers.append({'if-modified-since':'2016-02-28 14:02:03GMT'})
		
		handler.examples['metas']=metas
		handler.examples['headers']=headers

