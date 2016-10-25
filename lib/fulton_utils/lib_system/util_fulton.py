import re
import sys
import importlib
import os

#just for .py modules
def local_import(path,name):
	#assume for existence
	#if not os.path.exists(os.path.join(path,name+'.py'):
		#return None
	sys.path.append(path)
	mlib=sys.modules.get(name,None)
	#print(mlib)
	#print('importing',name)
	if mlib:
		try:
			hlib=importlib.reload(mlib) #如果此处出现错误，是因为sys.path中没有包含相应的路径
			#print('reload',name,'successfully')
		except AttributeError:#没有reload属性，不支持reload
			hlib=mlib
	else:
		hlib=importlib.import_module(name)
	sys.path.pop()
	return hlib
	
def get(s,start=None,end=None,exreturn=None):
	try:
		if end:
			res=s[start:end]
		else:#end=None时表示取单个元素
			res=s[start]
	except:
		res=exreturn
	return res
def readSetupFile(setupfile):
	setups=dict()
	with open(setupfile,'r') as f:
		lineno=1
		for line in f.readlines():
			line=line.lstrip()
			if not line.startswith('#') and not re.match(r'^\s*$',line):
				pos=line.find('=')
				if pos!=-1:
					key=line[:pos].strip()
					value=None if pos+1==len(line) else line[pos+1:-1]
					setups[key]=value
				else:
					raise Exception("Not valid expression in line:"+str(lineno)+".\n\tServer not initialized.");
			lineno=lineno+1
	return setups
	
#获取所有的文件目录
def traversPath(direc,pendings=None):
	if pendings==None:
		pendings=[]
	#拼写错误花去大部分时间
	if os.path.isdir(direc):
		pendings.append(direc)
		for i in os.listdir(direc):
			if not i.startswith("_"):
				traversPath(os.path.join(direc,i),pendings)

	return pendings
import shutil
import os
def backupFile(fFrom,fBackname,dBasedir):
	dst=os.path.join(dBasedir,fBackname)
	if not os.path.exists(fFrom):
		return "file "+fFrom+" not exists"
	if os.path.exists(dst):
		return backupFile(fFrom,fBackname+" - copy",dBasedir)
	else:
		shutil.copyfile(fFrom,dst)
		return "file "+fFrom+" backuped as "+dst
def listBackupdir(dBasedir):
	return "\n".join(os.listdir(dBasedir))
import datetime

#add to self
def backupDB(self):
	now=datetime.datetime.now()
	s=now.strftime("%Y-%m-%d %H:%M:%S")
	backdir=os.path.join(os.path.dirname(self.html_dir),"backups")
	backname=os.path.basename(self.dbs)+" - "+s
	res=backupFile(self.dbs,backname,backdir)
	print(res)

def listBackups(self):
	backdir=os.path.join(os.path.dirname(self.html_dir),"backups")
	res=listBackupdir(backdir)
	print(res)
def mysystem(cmd):
	tempstdout='/home/x/temp/stdout'
	#cmd=cmd.replace("\n",";")
	ccmd='('+cmd+') 2> '+tempstdout+' 1> '+tempstdout
	os.system(ccmd)
	print('exec :',ccmd)
	f=open(tempstdout)
	data=f.read();
	f.close()
	f=open(tempstdout,"w")#清空文件
	f.flush()
	f.close()
	return data
