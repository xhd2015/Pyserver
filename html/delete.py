#!/bin/python3 
def generate_html(s):
	i=s.path.find('?')
	if i==-1:
		id=-1
	else:
		try:
			id=int(s.path[i+1+len('id='):])
		except:
			id=-1
	if id!=-1:
		with s.sq.connect(s.dbs) as conn:
			c=conn.cursor()
			c.execute('DELETE FROM alldata WHERE id=?',(id,))
			conn.commit()
	#此处必须返回字符串类型,否则出错
	return [0,str(id)]
