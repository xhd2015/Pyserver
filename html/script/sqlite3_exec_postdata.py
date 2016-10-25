
def generate_html(s):
	dbsTest=s.html_dir+'/__temp.db'
	data=s.sf.getPostData(s)
	exec_str=data.decode('u8')
	res=[]
	with s.sq.connect(dbsTest) as conn:
		c=conn.cursor()
		try:
			c.execute(exec_str)
			res=c.fetchall()
			conn.commit()
		except Exception as e:
			res.append(e)
	return [0,str(res)]


