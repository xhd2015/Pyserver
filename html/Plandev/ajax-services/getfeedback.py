
import json
def generate_html(s):
	#text
	data=json.loads(s.sf.getPostData(s).decode("u8"))
	rtnData=[]
	if data["id"]:
		if data["id"]=="[all]":
				with s.sq.connect(s.dbs) as conn:
					cur=conn.cursor()
					cur.execute("Select id,content From Plan_Feedback Where 1;")
					res=cur.fetchall()
					for i in res:
						rtnData.append({"id":i[0],"content":i[1]})
	
	return [0,json.dumps(rtnData)]
