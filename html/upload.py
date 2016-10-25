#!/bin/python3

from urllib.parse import unquote_to_bytes
import time

def generate_html(s):
	sf=s.sf
	sq=s.sq


	data=sf.getPostData(s).decode('u8')
	#posted data read as bytes

	#一时疏忽，把数据库clear了
	with sq.connect(s.dbs) as conn:
		c=conn.cursor()
		if len(data)>0:
			c.execute('SELECT MAX(id) FROM alldata')    
			last=c.fetchone()[0]
			if last:
				last=int(last)+1
			else:
				last=0
			#print(content)
			# input()
			#关于引号的问题
			# content=content.replace("'","%27")
			uptime=time.time()
			c.execute('''
			INSERT INTO alldata VALUES(?,?,?)
			''',(last,data,uptime)
			)
			rtnJSON=r'''{{"id":{id} , "date":"{date}"}}'''.format(id=last,date=s.formatTime(uptime))
			conn.commit()
		else:
			rtnJSON='{}'
	#htitle='提交成功'
	#hbody='''<p>提交成功 ， <a href='/'>返回</a></p>'''
	#hf.send_html(s,hf.format_html(title=htitle,body=hbody))

	return [0,rtnJSON]
