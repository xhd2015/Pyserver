
import json
def generate_html(s):
	data=json.loads(s.sf.getPostData(s).decode("u8"));
	
	#正常处理数据
	rtnData="error"
	if "id" in data and data["id"]:
		data=data["id"]
		sqldata=data[:data.rindex(",")];
		with s.sq.connect(s.dbs) as conn:
			cur=conn.cursor()
			#cur.execute("Select id From Plan_P1 Where id in ({sqldata})".format(sqldata=sqldata))
			#print(cur.fetchall())
			cur.execute("Delete From Plan_P1 Where id in ({sqldata})".format(sqldata=sqldata))
			conn.commit()
			rtnData="success"
	return [0,rtnData]
