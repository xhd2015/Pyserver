__doc__=r'''
#input	:data/dict containing keys ["title","description","universal","px"],if "--help" is present,help info of this is sent
#process:insert data into database,failed when there exists exactly such one
#table_schema: Plan_P1--->id(pkey),title,description,universal,plans,extrasid(fkey)
#table_shcema: Plan_P1_Extras--> id(fkey),contents{},remarks{main:,px:},status{main:,px:}
#output	:{"id":-1|any integer,"datetime":"xxxx-xx-xx dd:dd:dd","status":"failed"|"success","default":help-info|other-request}
'''
import database_manipulate
import json
import itertools

schemas=[
	["Plan_P1",[
		("id",["Integer","Primary Key","Autoincrement"]),
		("title",["Text","Not Null"]),
		("description",["Text"]),
		("universal",["Text"]),
		("plans",["Text"]),#先将plans序列化成多个px,[p1,p2,p3,...]
		("extrasid",["Integer"])
	]],
	["Plan_P1_Extras",[
		("id",["Integer","Primary Key","Autoincrement"]),
		("contents",["JSONText"]),
		("remarks",["JSONText"]),
		("datetime",["Double","Not Null"]),
		("flags",["JSONText"])
	]]
]
#不管输入与否
#一个Handler将网页输入-->数据库表对应起来,然后定义各种插入,删除的操作-->返回输出
class BaseHandler:
	def __init__(self,s,schemas):
		self.s=s
		self.schemas=schemas
		self.dbm=database_manipulate.DBOperator(s.dbs)
		self.rtnData={}
	def init_schemas(self):
		for sch in LocalHandler.schemas:
			self.dbm.create(keys=sch[1],table=sch[0])
	def delete_schemas(self):
		for sch in LocalHandler.schemas:
			self.dbm.drop(table=sch[0])
	def get_data(self):
		data=self.s.sf.getPostData(self.s).decode('u8')
	def onGetInput(self):
		pass
		
	#Erros
	def onInputError(self):
		pass
	def onDatabaseError(self):
		pass
	__htmlinfo__=r'''
	
	
	'''
class InputHandler(BaseHandler):
	def __init__(self,s,schemas):
		super().__init__(s,schemas)
		self.data=self.s.sf.getPostData(self.s).decode('u8')

#JsonDataHandler
#获取json输入的脚本处理
class JSONHandler(InputHandler):
	def __init__(self,s,schemas):
		super().__init__(s,schemas)
		self.data=json.loads(self.data)

import urllib.parse
def processed_data(data):
	return urllib.parse.unquote(data)

import re
import sqlite3
import datetime
import json
#can't work now
def generate_html(s):
	#****onInit
	rtnData={"id":-1,"datetime":"","status":"failed"}
	
	#****getData
	#标准的数据获取语句
	try:
		data=json.loads(s.sf.getPostData(s).decode("u8")) 
	except:
	#****onGetDataError
		rtnData["default"]=r'''Input stream data is invalid for JSON parsing.Request with {'--help':''} for help.'''
	
	#定义完整的返回数据 id,datetime添加的日期,精确到秒xxxx-xx-xx xx:xx:xx
	else:
	#*****onGetHelp
		if "--help" in data:
			rtnData["status"]="success"
			rtnData["default"]=__doc__
	#****onAction---user defined
		else:
			plankeyvalue=[i for i in
				filter(
					lambda keyval:re.match(r'p\d',keyval[0]),
					data.items()
				)
			]
			#sort by px
			plankeyvalue.sort(key=lambda p:p[0])
			flags={"status":"undone"}
			
			#get json
			dataplanvalue=json.dumps(plankeyvalue)
			dataflags=json.dumps(flags)
			
			timenow=datetime.datetime.now()
			dnow=timenow.timestamp()
			try:
				dbm=database_manipulate.DBOperation(s.dbs)
				#数据没有重复,但是我觉得根本没有必要确定数据是否重复,这太麻烦了.
				
				#insert into Plan_P1_Extras
				table="Plan_P1_Extras"
				dbm.insert(
					table0=table,
					col1=["contents","flags","datetime"],
					condata1=[dataplanvalue,dataflags,dnow]
				)
				#时间戳是唯一的
				extrasid=dbm.select(
					table0=table,
					col0="id",
					cond0="datetime = ?",
					condata0=dnow
				)[0][0]
				print(extrasid)
				
				#insert into Plan_P1
				table="Plan_P1"
				colsInsert1=["title","description","universal"] #must find those keys
				colsInsert2=["plans","extrasid"]
				dbm.insert(
					table0=table,
					col1=itertools.chain(colsInsert1,colsInsert2),
					condata1=itertools.chain(
						[data[i] if i in data else None for i in colsInsert1 ],
						[ json.dumps([i[0] for i in plankeyvalue]),extrasid]
					)
				)

				mainid=dbm.select(
					table0=table,
					col0="id",
					cond0="extrasid=?",
					condata0=extrasid
				)[0][0]

				rtnData["status"]="success"
				rtnData["id"]=mainid
				rtnData["datetime"]=timenow.strftime("%Y-%m-%d %H:%M:%S")
			except sqlite3.OperationalError as e:
				stre=str(e)
				rtnData["default"]="Exception : "+str(type(e))+" , "+stre+"\n"
				if stre.startswith("no such table:"):
					#create table
					rtnData["default"]+="Please POST again after a new table created.\n"
				else:
					rtnData["default"]+=""
				raise e
			except Exception as e:
				rtnData["default"]=str(type(e))+" , "+str(e)+"\n"
				raise e
			finally:
				dbm.commit()
				dbm.close()
	#****onReturn
	return [0,json.dumps(rtnData)]
