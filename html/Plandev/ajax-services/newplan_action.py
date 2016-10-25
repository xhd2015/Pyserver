
import fulton_utils.action.action as gaction
import fulton_utils.lib_system.util_fulton as uf
import fulton_utils.lib_database.database_manipulate as dbman

__sqlSchema__=r"""
	create table Plan_V3(id integer primary key autoincrement,
							title text,
							description text,
							universal text,
							plansid,
							status,
							remark
						)
	create table Plan_V3_plans(id integer primary key autoincrement,
								content text,
								status text,
								remark text
							)
"""

#just a demo,an idea
class SqlEntity:
	def __init__(self):
		pass
	def makeSqlQuery(self):
		pass
	def makeSqlDelete(self):
		pass
#Here we proclaim a database designing standard
#has id auto increment primary key
#unfixed number of columns,use a nother table,but use sorted list to record id in the new table.
#	such as Plan_V3(id,title,d..,plansid='1 3 56 9',status,remark)
#			Subplans_V3(id,content,status,remark) ;subplans do not need title,description
class Handler(gaction.Handler):
	def __init__(self,s):
		super().__init__(s)
		self.table="Plan_V3"
		self.plansTable="Plan_V3_Plans"
		self.dbm=dbman.DBOperation(self.__s.dbs)
		self.dbm.use(self.table)
	#requires data to be executed
	#data:id=
	def actionAddPlan(self):
		self.dbm.insert(col0="title",condata0="")
		id=self.dbm.select(col0="max(id)")[0][0]
		self.setRtndata(status="success",reason="id is sent",data=str(id))
	def actionQuery(self):
		pass
	def actionQueryAll(self):
		pass
	
	#不能使用actionHdata,而应当actionHdataNull
	#input:data-->title,description, 
	#[subplan,substatus,subremark]//subplan,substatus,subremark
	def actionUpdate(self):
		
		pass
	#return : id
	def actionDeletePlan(self):
		pass
	def getData(self):
		super().getData()
		self.action=self.data["action"]
		self.pdata=self.data
	def finishServe(self):
		rs=super().finishServe()
		self.dbm.commit()
		self.dbm.close()
		return rs	
		
def generate_html(s):
	return Handler(s).setDebug(True).serve().finishServe();
