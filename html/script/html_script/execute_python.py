def generate_html(s):
	data=s.sf.getPostData(s)
	data=data.decode('u8')
	
	
	import io
	__res=io.StringIO()
	#设置新的环境变量, 重定向输出
	exec_globals={'__res':__res,'s':s}
	exec(r'''import sys;s1,s2=sys.stdout,sys.stderr;sys.stdout=__res;sys.stderr=__res''',exec_globals)
	try:
		exec(data,exec_globals)
	except Exception as e:
		__res.write(str(type(e)).replace('class','Exception')+' : '+str(e))
		__res.flush()
	#还原输出
	exec(r'''sys.stdout,sys.stderr=s1,s2''',exec_globals)
		
	return [0,__res.getvalue()]
