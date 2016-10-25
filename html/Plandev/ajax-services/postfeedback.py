

import json
def generate_html(s):
	#text
	data=json.loads(s.sf.getPostData(s).decode("u8"))
	rtnData={"status":"failed","id":"-1"}
	with s.sq.connect(s.dbs) as conn:
		cur=conn.cursor()
		cur.execute("Select id From Plan_Feedback Where content=?;",(data["text"],) )
		res=cur.fetchone()
		if res:#已经存在同样的内容
			pass
		else:
			cur.execute("Insert Into Plan_Feedback(content) Values(?);",(data["text"],) )
			conn.commit()
			cur.execute("Select id From Plan_Feedback Where content=?;",(data["text"],) )
			res=cur.fetchone()
			rtnData["status"]="success"
			rtnData["id"]=res[0]
	print(rtnData)
	
	return [0,json.dumps(rtnData)]
