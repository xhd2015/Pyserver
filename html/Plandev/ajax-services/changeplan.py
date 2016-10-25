
import json
def generate_html(s):
	data=json.loads(s.sf.getPostData(s).decode("u8"));
	#正常处理数据
	rtnData="error"
	if "id" in data and data["id"]:
		id=data["id"]
		title=data["title"]
		description=data["description"]
		universal=data["universal"]
		p1=data["p1"]
		p2=data["p2"]
		p3=data["p3"]
		p4=data["p4"]
		p5=data["p5"]

		with s.sq.connect(s.dbs) as conn:
			cur=conn.cursor()
			cur.execute("Select id From Plan_P1 Where id = ?",[id]);
			res=cur.fetchone()
			if res:#查询到这个结果
				sqlUpdate="Update Plan_P1 Set title=?,description=?,universal=?,p1=?,p2=?,p3=?,p4=?,p5=? Where id=?";
				sqlData=[title,description,universal,p1,p2,p3,p4,p5,id]
				cur.execute(sqlUpdate,sqlData)
				conn.commit()
				rtnData="success"
	return [0,rtnData]
