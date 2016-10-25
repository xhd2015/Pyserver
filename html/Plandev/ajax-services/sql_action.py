

	

#AttributeError
#__getattribute__
#__setattr__
import fulton_utils.lib_database.database_manipulate as dbman
import io
import json
import fulton_utils.action.action as gaction
import itertools
	
class Handler(gaction.Handler):
	def __init__(self,s):
		super().__init__(s)

	#database,table
	def actionCreateTable(self):
		dbm,data=self.prepare()
		col1=zip(data["col"],[i.split(" ") for i in data["colarg"]])
		dbm.create(col1=col1)
		dbm.commit()
		dbm.close()
		self.setRtndata(status="success",reason="table "+data["table"]+" created")
	def actionDelete(self):
		try:
			data=self.data["data"] #应当能够保存用户信息,然后获取默认使用的dbase,table
			id=data.get("id",None)
			table=data.get("table",None)
			if not id or not table:
				raise Exception("id or table not given")
			dbase=data.get("dbase",self.__s.dbs)
			dbm=dbman.DBOperation(dbase)
			dbm.use(table)
			dbm.delete(cond0="id=?",condata0=id)
			dbm.commit()
			dbm.close()
		except Exception as e:
			self.setRtndata(status="failed",reason=str(e))
			raise e
		else:
			self.setRtndata(status="success",reason=id+" deleted from "+dbase+"-->"+table)
	def actionDropTable(self):
		dbm,data=self.prepare()
		dbm.drop()
		dbm.commit()
		dbm.close()
		self.setRtndata(status="success",reason=dbm.getCurtable()+" dropped")
	def actionQueryAll(self):
		dbm,data=self.prepare()
		qdata=dbm.select()
		dbm.commit()
		dbm.close()
		self.setRtndata(status="success",reason="data is sent." ,data=qdata);
	def actionInsert(self):
		dbm,data=self.prepare()
		expectedCols=["content"]
		dbm.insert(
			col1=expectedCols,
			condata1=(data.get(key,None) for key in expectedCols)
			)
		qid=dbm.select(col0="id",cond0="content=?",condata0=data["content"])[0][0]
		dbm.commit()
		dbm.close()
		self.setRtndata(status="success",reason="id is sent." ,data=qid);
	def actionUpdate(self):
		dbm,data=self.prepare()
		expectedCols=["content"]
		
		dbm.update(
			col1=expectedCols,
			cond0="id="+data["id"],
			condata1=(data.get(Key,None) for key in expectedCols) 
		)
		dbm.commit()
		dbm.close()
		
		
	def prepare(self):
		data=self.data["data"]
		table=data.get("table",None)
		if not table:
			raise Exception("no given table")
		dbase=data.get("dbase",self.__s.dbs)
		dbm=dbman.DBOperation(dbase)
		dbm.use(table)
		return dbm,data
			
	
		
def generate_html(s):
	return Handler(s).setDebug(True).serve().finishServe();
