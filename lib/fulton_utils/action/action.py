

	

#AttributeError
#__getattribute__
#__setattr__
import fulton_utils.lib_database.database_manipulate as dbman
import io
import json
import traceback

class NoSuchActoinException(Exception):
	def __init__(self,message):
		self.message=message
class DataGetException(Exception):
	def __init__(self,message):
		self.message=message
class Handler:
	__help__=r'''Input stream data is invalid for JSON parsing.Request with {'action':'help'} for help'''
	__doc__=r'''
	input: {action,
		data
		}
	output: {
		status: success|failed
		reason:
		data:
	}'''
	def __init__(self,s):
		self.rtnData={
			"status":"failed",
			"reason":"",
			"data":{}
		}
		self.__s=s
		self.serverdebug=False
		
	def serve(self):
		try:
			self.getData()
			self.log("after getData")
			doAction=self.getAction()
			self.log("after getAction")
		except DataGetException as e:
			self.onDataGetException(e)
		except NoSuchActoinException as e:
			self.onNoAction(e.message)
		except Exception as e:
			self.onPrepareException(e)
		else:
			try:
				self.log("before doAction")
				doAction()
				self.log("after doAction")
			except Exception as e:
				self.onServeException(e)
		finally:
			return self
				
	def getData(self):
		s=self.__s
		self.log("in getData")
		try:
			self.originalData=s.sf.getPostData(s).decode("u8")
			self.data=json.loads(self.originalData)
		except Exception as e:
			raise DataGetException(str(e))

	def getAction(self):
		try:
			name=self.data["action"] #不区分大小写
			self.log("in getAction : name = "+name)
		except:
			raise NoSuchActoinException("Not key 'action' is present in data.")
		#standard name
		sname=name.lower()
		#获取name的index
		oriattrs=self.__dir__()
		sattrs=[i.lower() for i in oriattrs]
		try:
			index=sattrs.index("action"+sname)
		except ValueError as e:#actionxxxx  not in list
			raise NoSuchActoinException(name)
		else:
			action=self.__getattribute__(oriattrs[index])
			if type(action) != type(self.__init__):#如果不是函数
				raise NoSuchActoinException(name)
			else:
				return action
	def setDebug(self,flag):
		self.serverdebug=flag
		return self
	def log(self,m):
		if self.serverdebug:
			print(m)
		return self
		
	def onPrepareException(self,e):
		self.log("In preparing data and action,an internal error happended:")
		self.log("\t[onPrepateException]"+str(type(e))+":"+str(e))
		self.setRtndata(reason="[Exception "+str(type(e))+"]"+str(e))
	def onNoAction(self,actionname):
		self.log("[onNoActionException]"+actionname)
		self.setRtndata(status="failed",reason="no such action :"+actionname+"\nSent data is:"+self.originalData)
	def onServeException(self,e):
		self.log("[ onServeException ]===START===")
		self.log("".join(Handler.formatException(e)))
		self.log("[ onServeException ]===END====")
		self.setRtndata(status="failed",reason="[Exception "+str(type(e))+"]"+str(e))
	def onDataGetException(self,e):
		self.setRtndata(status="failed",reason=Handler.__help__)
	@staticmethod
	def formatException(e):
		return traceback.format_exception(type(e), e, e.__traceback__)
	def finishServe(self):
		data=json.dumps(self.rtnData)
		self.log("[Finish Service] data:"+data)
		return [0,data]
		
	def setRtndata(self,**args):
		for key in args:
			if key in self.rtnData:
				self.rtnData[key]=args[key]
		self.log("[Set Rtndata] data:"+json.dumps(self.rtnData))
	
	def actionEcho(self):
		self.setRtndata(status="success",data=self.originalData)
	def actionHelp(self):
		self.setRtndata(status="success",data=Handler.__doc__)
	def actionExecPython(self):
		'''希望数据中包含pycode'''
		__res=io.StringIO()
		#设置新的环境变量, 重定向输出
		try:
			data=self.data["data"]["pycode"]
		except Exception as e:
			raise e
		exec_globals={'__res':__res,'s':self.__s,"dbman":dbman}
		exec(r'''import sys;s1,s2=sys.stdout,sys.stderr;sys.stdout=__res;sys.stderr=__res''',exec_globals)
		try:
			exec(data,exec_globals)
		except Exception as e:
			__res.write(str(type(e)).replace('class','Exception')+' : '+str(e))
			__res.flush()
		#还原输出
		exec(r'''sys.stdout,sys.stderr=s1,s2''',exec_globals)
		self.setRtndata(status="success",data=__res.getvalue())
		
	def actionLs(self):
		self.log("ls")
		i=list(map(lambda x:x[6:],filter(lambda x:x.startswith("action"),dir(self))))
		self.setRtndata(
			status="success",
			data=i
			)
