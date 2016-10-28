
import fulton_utils.action.action as gaction
import fulton_utils.lib_system.util_fulton as uf
import fulton_utils.lib_database.database_manipulate as dbman
from attr.validators import instance_of
import itertools
import sqlite3

__sqlSchema__=r"""
	create table Plan_V3(id integer primary key autoincrement,
							title text,
							description text,
							universal text,
							status text,
							weight double,
							visiable text,
							remark text
						)
	create table Plan_V3_Plans(id integer primary key autoincrement,
								mainid integer,
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
		id=self.dbm.executeQuery("select max(id) from Plan_V3")
		try:
			id=id[0][0]+1
		except:
			id=1
		self.dbm.insert(col1=["id","visiable","plansid"],condata1=[id,"shown",""])
		self.setRtndata(status="success",reason="id is sent",data=str(id))
	#input {
	#	word:""
	#	type:[word1] || no type
	#	typeall:all -->if have
	#	limit:""
	#}
	#sql is : select id,title,description,universal,plansid
	#	status,weight,visiable,remark from Plan_V3 where visable=?
	# and (title like .. or description like or un.. )
	#
	# order by (weight,id)
	# Example:
	#	type=["plan" "title" "description"]
	#	if(search plan)
	#	no type
	
	#先部分实现,因为搜索功能并不是必须用到;实现description,visiable
	#title,universal,以及all的实现
	
	#bug report:
	#可能搜索%,_有问题,考虑使用quote函数
	def actionQuery(self):
		word=self.pdata["word"]
		maintypes=self.pdata.get("type",None)
		alltype=self.pdata.get("typeall",None)
		visiable=self.pdata.get("visiable","shown")
		limit=self.pdata["limit"]
		if not maintypes:
			maintypes=[]
		if alltype:
			maintypes=["title","universal","description"]
		#使用printf
		mylen=len(maintypes)
		funcfmt=""
		if mylen!=0:
			firstfmt="%s"*mylen
			args=",".join(maintypes)
		
			funcfmt="printf(\""+firstfmt+"\","+args+") like ? "
		sqlQuery = r'''
		Select id,title,description,universal,plansid,status,weight,visiable,remark 
		from Plan_V3
		where visiable = ?
		'''
		sqlData=[visiable]
		if funcfmt:
			sqlQuery+=" and "+funcfmt
			sqlData.append("%"+word+"%")
		try:
			limit=str(int(limit))
			#空字符串会失败
		except ValueError as e:
			sqlLimit=""
		else:
			sqlLimit=" limit "+limit
		sqlQuery+=sqlLimit+" order by id desc"
		
		self.dbm.cursor.execute(sqlQuery,sqlData)
		res=self.dbm.cursor.fetchall()
		rtnData=[]
		if res:
			#还原id
			for ir in res:
				thisdict=dict()
				thisdict["id"]=ir[0]
				thisdict["title"]=ir[1]
				thisdict["description"]=ir[2]
				thisdict["universal"]=ir[3]
				thisdict["status"]=ir[5]
				thisdict["weight"]=ir[6]
				thisdict["visiable"]=ir[7]
				thisdict["remark"]=ir[8]
				thisdict["plans"]=[]
				if ir[4]:
					plansid=[ [int(i)] for i in ir[4].split(" ")]
					subres=[]
					for i in plansid:
						self.dbm.cursor.execute("Select id,content,status,remark from Plan_V3_Plans where id=?",i)
						subres.append(self.dbm.cursor.fetchone())
					for isub in subres:
						thisdict["plans"].append({
							"id":isub[0],
							"content":isub[1],
							"status":isub[2],
							"remark":isub[3]
							})
				rtnData.append(thisdict)
		self.setRtndata(status="success",reason=str(len(rtnData))+" items set.",
				data=rtnData
				)
	#不能使用actionHdata,而应当actionHdataNull
	#input:data-->title,description, 
	#[subplan,substatus,subremark]//subplan,substatus,subremark
	'''
	{"action":"update","data":
	{"title":"","description":"","universal":"","id":
	"planid":["",""],  #如果先把plan与旧的相比,1.包含newplan的新建,2.不在planid中的,删除
	"subplan":["",""], #这些数据或者是None,或者是数组,一个元素的数组也是这样的
	"substatus":["",""],
	"subremark":["",""],
	"status":"All status",
	"remark":"",
	"weight":"weight",
	"visiable":"shown"}}
	'''
	#bug report:
	#	数据库Plan_V3_Plans可能插入完全相同的数据content,status,remark ; 这对正确性没有影响,但是有可能
	#造成数据冗余;  最好使用unique约束
	def actionUpdate(self):
		id=self.pdata["id"]
		try:
			id=str(int(id))
		except ValueError as e:
			self.setRtndata(status="failed",reason="id is not vaild integer.")
		else:
			sqlQueryPlans="Select plansid From Plan_V3 Where id="+id+";"
			oriPlansid=self.dbm.executeQuery(sqlQueryPlans)[0][0]
			if oriPlansid:
				oriPlansid=oriPlansid.split(" ")
			else:
				oriPlansid=[]
			givePlansid=self.pdata.get("planid",[])
			#<start> plan更新
			delPlanId=[]
			updatePlanId=[]
			for index,oriId in enumerate(oriPlansid):
				if not oriId in givePlansid:
					delPlanId.append([oriId])
				else:
					updatePlanId.append([ 
							self.pdata["subplan"][index],
							self.pdata["substatus"][index],
							self.pdata["subremark"][index],
							int(oriId)
						])
			insertPlans=[]
			for index,giveId in enumerate(givePlansid):
				if giveId=="newplanid" or giveId=="":
					insertPlans.append([
						self.pdata["subplan"][index],
						self.pdata["substatus"][index],
						self.pdata["subremark"][index]
						])
			if delPlanId:
				sqlDeletePlans="Delete From Plan_V3_Plans"
				self.dbm.executeUpdate(sqlDeletePlans,[delPlanId])
			
			if updatePlanId:
				sqlUpdatePlans="Update Plan_V3_Plans Set content=? , status=? , remark=?  Where id=?"
				self.dbm.executeUpdate(sqlUpdatePlans,updatePlanId)
			
			insertedIds=[]
			if insertPlans:
				sqlInsertPlans="Insert Into Plan_V3_Plans(content,status,remark) Values(?,?,?)";
				self.dbm.executeUpdate(sqlInsertPlans,insertPlans)
				sqlQueryNewIds="Select id From Plan_V3_Plans Where content=? and status=? and remark=?"
				for insert in insertPlans:
					self.dbm.cursor.execute(sqlQueryNewIds,insert)
					insertedIds.append(self.dbm.cursor.fetchone()[0])
				
			#这里必须为字符串表示的整数才能正常
			#将id排序之后才插入
			updatedIds=" ".join(sorted(itertools.chain(
				map(lambda x:str(x),insertedIds),
				map(lambda x:str(x[3]), updatePlanId)
				)))
			#</end> 完成了plan的更新
			sqlUpdateMain=r'''Update Plan_V3 Set title=?,description=?,universal=?,plansid=?,status=?,remark=?,weight=?,visiable=?'''
			sqlUpdateMainData=(
					self.pdata["title"],
					self.pdata["description"],
					self.pdata["universal"],
					updatedIds,
					self.pdata["status"],
					self.pdata["remark"],
					float(self.pdata["weight"]),
					self.pdata["visiable"]
				)
			sqlUpdateMain+=" Where id="+id+";"
			self.dbm.cursor.execute(sqlUpdateMain, sqlUpdateMainData)
			self.setRtndata(status="success",reason="data updated.id is sent.",data=id)
			
	#return : id
	def actionDeletePlan(self):
		pass
	#@override
	def getData(self):
		super().getData()
		self.action=self.data["action"]
		self.pdata=self.data["data"]
	#@override
	def finishServe(self):
		self.dbm.commit()
		self.dbm.close()
		return super().finishServe()
	
	def addNewMainDefault(self):
		sqlInsert="Insert Into Plan_V3(visiable,weight) Values(?,?);"
		sqlData=[["shown",100]] 
		self.myexec(sqlInsert, sqlData)
		sqlQuery="Select max(id) From Plan_V3;"
		id=self.myexec(sqlQuery)[0][0]
		return id
	def addNewPlanDefault(self,mainids):
		sqlInsert="Insert Into Plan_V3_Plans(mainid) Values(?);"
		sqlData=[ [id] for id in mainids ]
		self.myexec(sqlInsert, sqlData)
		sqlQuery="Select id From Plan_V3_Plans Order By id Desc Limit "+len(sqlData)+";"
		newids=[ i[0] for i in self.myexec(sqlQuery) ]
		return newids
	
	def updateOneMain(self):
		pass
	def updatePlanWithOneMain(self,mainid):
		pass
	def queryPlans(self,content,mainids=None):
		sqlQuery="Select id,mainid,content,status,remark from Plan_V3_Plans"
		sqlQuery+="  Where mainid in ("+",".join(map(lambda x:str(x)))+");"
		return self.myexec(sqlQuery)
		
	def myexec(self,sql,data=[]):
		self.log(sql+" "+str(data))
		try:
			self.dbm.cursor.executemany(sql,data)
		except sqlite3.ProgrammingError as e:
			if e.args[0]=="You cannot execute SELECT statements in executemany().":
				self.dbm.cursor.execute(sql,data)
		return self.dbm.cursor.fetchall()
		
		
def generate_html(s):
	return Handler(s).setDebug(True).serve().finishServe();
