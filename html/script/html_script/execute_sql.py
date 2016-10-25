#slave 页面是 无,所有页面均可向这个页面发起一个请求
__doc__=r'''
input:
	sql:Select * From Plan_P1 -- a complete sql statement
	dbs:-->s.dbs						-- db name to operate,default to be s.dbs
	--help:						-- get help message
output:
	status:failed | success -- if sql is an operation statement
	data: <fetched data from database> -- if sql is query statement
	default:<message wrote for status or others>
'''
def hasAllKey(datadict,keys):
	for i in keys:
		if not i in datadict:
			return False,i
	return True
	
#取字典的一个子集,值copy; subCopyFrom()
def subCopyFrom(dict_from,keys):
	rtndict={}
	for i in keys:
		if i in dict_from:
			rtndict[i]=dict_from[i]
	return rtndict
	
import json,sqlite3
import sys
def generate_html(s):
	#有些键具有默认值
	#allKeys=["sql","dbs"-->s.dbs]
	requiredKeys=["sql"]
	rtnData={"status":"failed","data":None,"default":None}
	try:
		data=json.loads(s.sf.getPostData(s).decode("u8"))
		if type(data)!=dict:
			raise Exception("Not dict")
		if "--help" in data:
			rtnData["status"]="success"
			rtnData["default"]=__doc__
		elif not hasAllKey(data,requiredKeys):
			rtnData["default"]="Missing key(s) from data,required keys are '"+",".join(requiredKeys)+"'."
		else:
			validData=subCopyFrom(data,requiredKeys)
			if not "dbs" in validData:
				validData["dbs"]=s.dbs
			try:
				with s.sq.connect(validData["dbs"]) as conn:
					cur=conn.cursor()
					cur.execute(validData["sql"])
					rtnData["data"]=cur.fetchall()
					conn.commit()
					rtnData["status"]="success"
			except Exception as e:
				rtnData["default"]="Error happened when operate on database.Exception:"+str(e)+"."
	except:
		rtnData["default"]="Wrong parsing data."
	
	return [0,json.dumps(rtnData)]
	
