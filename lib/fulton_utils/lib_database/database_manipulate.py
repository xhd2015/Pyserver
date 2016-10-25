
#sql functions useful
import sqlite3
import functools
import itertools
#itertools object用一次就完毕


class DBOperation:
	__doc__=r'''
	very simple APIs for database mainpulation
	select, delete : 如果条件中包含问号,就要提供内容
	'''
	#这些是最常用的sql命令
	sqlPatterns={
		"create":"Create Table {table}({keys});",
		"drop"	:"Drop Table {table};",
		"delete":"Delete From {table} Where {conditions};",#第一个condition不能有逻辑符号
		"update":"Update {table} Set {values} Where {conditions};",
		"insert":"Insert Into {table}({cols}) Values({values});",
		"select":"Select {cols} From {table} Where {conditions};"
	}
	NOTNULL="Not Null"
	AUTO="Autoincrement"
	INT="Integer"
	JSONTEXT="JSONText"
	DOUBLE="Double"
	PK="Primary Key"
	FK="Foreign Key"
	APK="Primary Key Autoincrement"
	
	@staticmethod
	def get(key):
		return DBOperation.sqlPatterns.get(key)
	@staticmethod
	def formatAsStr(cols,joiner=","):
		return cols if type(cols) in (str,) else joiner.join(cols)
	#判定是基本类型还是聚合类型,从而获取长度
	@staticmethod
	def isPackaged(someValue):#[], [ [] [] ]
		if DBOperation.isBasicType(someValue):
			return False
		else:
			return True
	@staticmethod
	def isBasicType(value):
		return type(value) in (str,int,float,bool)
	@staticmethod
	def isCollection(value):
		return type(value) in (list,tuple)
	@staticmethod
	def packagedData(data):
		return data if DBOperation.isPackaged(data) else [data]
	@staticmethod
	def asList(likeList):
		if DBOperation.isCollection(likeList):
			return likeList
		else:
			return [i for i in likeList]
	@staticmethod
	def example():
		drop="0"
		db=DBOperation("/home/x/installed/pyserver/AQzLike.db")
		table="kk"
		db.use(table)
		if drop=="-1":
			db.create(key1=[("id",["integer","primary key","autoincrement"]),("test",["text"])])
		#print(db.select(table0="sqlite_master"))
		#db.insert(col0="test",condata0="w") 
		#Delete From kk Where test=w;
		#sqlite3.OperationalError: no such column: w
		#在sqlite3中标识符就是列
		db.update(col0="test",condata0="yy",cond1=["id=11"])
		#db.delete(cond0="test=?",condata0="w")
		print(db.select())
		 
		if drop=="1":
			db.drop()
		db.commit()
		db.close()
	#return be none if both are None, else is list
	def standlizeArgs2(arg1,arg2):
		if arg1!=None:
			if arg2==None:
				arg2=[]
			else:
				arg2=DBOperation.asList(arg2)
			arg2.append(arg1)
		#now arg1==None and arg=[any] || arg=list	
		
		if arg2!=None:#list like
			arg2=DBOperation.asList(arg2)
			
		return arg2
	def noneAsDefault(x,defunc):
		if x==None:
			x=defunc()
		return x
	
	def __init__(self,dbs):
		self.dbs=dbs
		self.conn=sqlite3.connect(self.dbs)
		self.cursor=self.conn.cursor()
		self.curtable=None
	def use(self,table):
		self.curtable=table
	def getCurtable(self):
		return self.curtable
	#with
	#href=https://docs.python.org/3.5/library/stdtypes.html?highlight=__enter__#contextmanager.__enter__
	def __enter__(self):
		#raise Exception("x")
		return self
	def __exit__(self,exc_type, exc_val, exc_tb):
		print(exc_type, exc_val, exc_tb)
		return False #complete handling exceptions
		
	def hasJSON(self,table):
		pass
		
	#这里介绍了一种新的函数编写格式
	#1.None作为默认参数,通过内部调用noneAsDefault()来设置参数默认值
	
	#keys=[("id",[integer,primary key,autoincrement]),...]
	#为了使keys保持固定的顺序
	#只提供一个table0级别,只能创建一个表
	#key0:("id",[integer,primary key,autoincrement]), key1:[key0]
	#table0:"sqltable"
	def create(self,col0=None,col1=None,table0=None):
		findkey="create"
		#key
		col1=DBOperation.standlizeArgs2(col0,col1)
		col1=DBOperation.noneAsDefault(col1,list)
		#table
		table=DBOperation.noneAsDefault(table0,self.getCurtable)

		sqlkeys=[]
		for i in col1:
			sqlkeys.append(" ".join(itertools.chain([i[0]],i[1])))
		sqlCreate=DBOperation.get(findkey).format(
			table=table,
			keys=",".join(sqlkeys)
		)
		self.executeUpdate(sqlCreate)
	#仅执行一个insert,values= listlike | ["x","y"] 
	#condata0:"x" condata1:[condata0] condata2:[ [condata0] ]
	#table0:"x"
	#col0:"id"
	def insert(self,col0=None,col1=None,condata0=None,condata1=None,condata2=None,table0=None):
		findkey="insert"
		#col
		col1=DBOperation.standlizeArgs2(col0,col1)
		col1=DBOperation.noneAsDefault(col1,list)
		#condata
		condata1=DBOperation.standlizeArgs2(condata0,condata1)
		condata2=DBOperation.standlizeArgs2(condata1,condata2)
		condata2=DBOperation.noneAsDefault(condata2,list)
		#table
		table0=DBOperation.noneAsDefault(table0,self.getCurtable)
		
		#构造sql语句
		sqlInsert=DBOperation.get(findkey).format(
			table=table0,
			cols=",".join(col1),
			values=",".join(["?"]*len(col1))
		)
		self.executeUpdate(sqlInsert,condata2)

		
	#condata--> ["x"] list
	#con0:
	def delete(self,cond0=None,cond1=None,condata0=None,condata1=None,condata2=None,table0=None):
		findkey="delete"
		#cond
		cond1=DBOperation.standlizeArgs2(cond0,cond1)
		cond1=DBOperation.noneAsDefault(cond1,lambda:["0"]) #still None,set to default
		#condata
		#return must be list
		condata1=DBOperation.standlizeArgs2(condata0,condata1)
		condata2=DBOperation.standlizeArgs2(condata1,condata2)
		condata2=DBOperation.noneAsDefault(condata2,list)
		#table
		table0=DBOperation.noneAsDefault(table0,self.getCurtable)

		
		sqlDelete=DBOperation.get(findkey).format(
			table=table0,
			conditions=" ".join(DBOperation.packagedData(cond1))
		)
		self.executeUpdate(sqlDelete,condata2)
		
	#conditions 作为标准的[],而不能是基本对象
	#凡是作为?插入的数据,都是condata
	def update(self,col0=None,col1=None,cond0=None,cond1=None,condata0=None,condata1=None,condata2=None,table0=None):
		findkey="update"
		#col
		col1=DBOperation.standlizeArgs2(col0,col1)
		col1=DBOperation.noneAsDefault(col1,list)
		#cond
		cond1=DBOperation.standlizeArgs2(cond0,cond1)
		cond1=DBOperation.noneAsDefault(cond1,lambda:["0"])
		#condata
		condata1=DBOperation.standlizeArgs2(condata0,condata1)
		condata2=DBOperation.standlizeArgs2(condata1,condata2)
		condata2=DBOperation.noneAsDefault(condata2,list)
		#table
		table0=DBOperation.noneAsDefault(table0,self.getCurtable)
		
		sqlUpdate=DBOperation.get(findkey).format(
			table=table0,
			values=",".join([i+" = ?" for i in col1]),
			conditions=" ".join(cond1)
		)
		self.executeUpdate(sqlUpdate,condata2)
		
	#必须是标准的list,tuple
	#condata=[ [] [] [] ]
	#condata必须作为2级传入
	#参数名规则:默认1,2则要求传入包装
	def select(self,col0=None,col1=None,cond0=None,cond1=None,condata0=None,condata1=None,condata2=None,table0=None,table1=None):
		findkey="select"
		#col
		col1=DBOperation.standlizeArgs2(col0,col1)
		col1=DBOperation.noneAsDefault(col1,lambda:["*"])
		#cond
		cond1=DBOperation.standlizeArgs2(cond0,cond1)
		cond1=DBOperation.noneAsDefault(cond1,lambda:["1"])
		#condata
		condata1=DBOperation.standlizeArgs2(condata0,condata1)
		condata2=DBOperation.standlizeArgs2(condata1,condata2)
		condata2=DBOperation.noneAsDefault(condata2,list)
		#table
		table1=DBOperation.standlizeArgs2(table0,table1)
		table1=DBOperation.noneAsDefault(table1,lambda:[self.getCurtable()])
		
		
		sqlSelect=DBOperation.get(findkey).format(
			table=",".join(table1),
			cols=",".join(col1),
			conditions=" ".join(cond1)
		)
		return self.executeQuery(sqlSelect,condata2)
	
		
	def drop(self,table0=None):
		findkey="drop"
		#table
		table0=DBOperation.noneAsDefault(table0,self.getCurtable)
		sqlDrop=DBOperation.get(findkey).format(table=table0)
		self.executeUpdate(sqlDrop)
		
	#sqlData must be packaged to be [ [] [] [] ]或者[None]
	def execute(self,sqlStatement,sqlData=[]):
		slen=len(sqlData)
		print(sqlStatement,sqlData)
		if slen == 0:
			self.cursor.execute(sqlStatement)
		elif slen ==1 :
			self.cursor.execute(sqlStatement,sqlData[0])
		elif slen > 1:
			self.cursor.executemany(sqlStatement,sqlData)
		return self.cursor.fetchall()
	
	def executeQuery(self,sqlStatement,sqlData=[]):
		return self.execute(sqlStatement,sqlData)
	def executeUpdate(self,sqlStatement,sqlData=[]):
		self.execute(sqlStatement,sqlData)
	def commit(self):
		self.conn.commit()
	def close(self):
		self.conn.close()

if __name__=="__main__":
	DBOperation.example()
