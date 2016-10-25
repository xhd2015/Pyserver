
import __plandev_library as plandev
import json
def generate_html(s):
	data=s.sf.getPostData(s)
	data=data.decode("u8")

	dictdata=json.loads(data)
	
	rtnres="[]"
	with s.sq.connect(s.dbs) as conn:
		cur=conn.cursor()
		
		if dictdata["q"]=="[all]":
			#查询所有数据
			sqlQuery="Select * From Plan_P1;"
		
		cur.execute(sqlQuery)
		res=cur.fetchall()
		
		#将数据打包成键值对
		sqlkeys=["id","title","description","universal","p1","p2","p3","p4","p5"]
		dictres=[]
		for i in res:
			dictres.append({sqlkeys[index]:i[index] for index in range(len(sqlkeys))})
		rtnres=str(json.dumps(dictres))
		
	return [0,rtnres]
		
		
		
