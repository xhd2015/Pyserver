import json

def generate_html(s):
	data=s.sf.getPostData(s);
	try:
		data=json.loads(data.decode('u8'))
	except:#not valid data
		return [0,"-1"]
	#id content
	try:
		id=int(data['id'])
		content=data['content']
		with s.sq.connect(s.dbs) as conn:
			c=conn.cursor()
			c.execute('UPDATE alldata SET content=? WHERE id=?',[content,id])
			conn.commit()
	except:
		id=-1
	
	return [0,str(id)]
