#!/bin/python3
from urllib.parse import unquote_to_bytes
import time

class NoSearchResultException(Exception):pass
def generate_html(s):
	sf=s.sf
	sq=s.sq
	hf=s.hf

	additional_head=r'''
	<script src='/jquery-3.1.0.min.js'></script>
	<script src='/content_format_jquery.js'></script>'''
	html_style='''body{font-size: 3em;}'''
	data=sf.getPostData(s)

	data=data.replace(b'+',b'%20')

	data=sf.parseArgData(data.decode('u8'))
	scontent=unquote_to_bytes(data.get('scontent','')).decode('u8')
	res=[]
	html_body=''
	try:
		if not scontent:
			raise NoSearchResultException()
		with sq.connect(s.dbs) as conn:
			c=conn.cursor()
			#id integer , content text , date read
			execution='SELECT * FROM alldata WHERE content LIKE ? ';
			pattern=['%'+scontent+'%']
			c.execute(execution,pattern)
			res=c.fetchall()

			html_body=r'''<lable>搜索结果</label><br /> '''
			if len(res):
				#标准以下一行开始换行
				html_body+=r'''
				<script>'''
				for ctn in reversed(res):

					dateString=s.formatTime(ctn[2])
					precnt=s.quoteToJavascrip(ctn[1])
					html_body+=r'''document.write(getFormattedContentAsString('{content}','{datetime}',{id}));'''.format(content=precnt,datetime=dateString,id=ctn[0])+'\n'
				html_body+=r'''
				</script>'''
			else:
					raise NoSearchResultException()
	except NoSearchResultException as e:
		html_body+='<p>无{}搜索结果</p>'.format('"'+scontent+'"')


	html_body+='''<a href="/" >返回</a>'''
	html=hf.format_html(head=additional_head,body=html_body)

	return [0,html]
