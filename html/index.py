#!/bin/python3

import time
def quoteToJavascrip(t):
	t=t.replace('\\',r'\\\\')
	t=t.replace("'",r"\'")
	t=t.replace('&','&amp;')
	t=t.replace('<','&lt;')
	t=t.replace('>','&gt;')
	t=t.replace("\n",r"\n")
	t=t.replace("\r",r"\r")

	return t

def generate_html(s):
	hf=s.hf
	sq=s.sq
	'''响应式设计范例'''

	additional_head=r'''
	<script src='/content_format_jquery.js'></script>
	<script src='/jquery-3.1.0.min.js'></script>
	<script>
	/*1em=16px ， 通常，内部em用来指代父元素字体的像素*/
	$(document).ready(function(){
	$('#btn_update').click(function(e){
	postUpdateData($('#content'));
	});
	});
	</script>'''
	qz_title='AQzLike'
	qz_style=r'''
	div#container{
	width: 100%;
	}
	div#prompter{
	background-color: #99bbbb;
	width: 100%;
	}
	div#lister{
	width: 100%;
	}
	p#foot_content{
	float: center;
	}
	#updater textarea{
	width: 100%;
	height: 5em;
	}

	#search_form input[name=scontent]{
	width: 70%;
	}
	#search_form input[value=查找]{
	width:  20%;
	}
	'''
	qz_body=r'''
	<div id='container'>
	<div id='prompter'>
	<label>----内容----</label>
	</div>
	<div id='inputter'>
	<!-- 原来的提交是一个form，暗示着页面跳转，现在，使用ajax技术只取回更新的数据 -->
	<div id='updater'>
	<textarea name="content" id="content"></textarea>
	<br/>  <!--我去年换了个行-->
	<input type="checkbox" value='c' name='clear' disabled='disabled'>清除</input>
	<button type="submit"  id='btn_update'>提交</button>
	</div>

	<form action='/search.html' method='post' id='search_form'>
	<input type='text' name='scontent'/>
	<input type='submit' value='查找'/>
	</form>
	</div>
	<div id='lister'>
	<hr/>
	<script>
	'''
	with sq.connect(s.dbs) as conn:
		c=conn.cursor()
		c.execute('SELECT * FROM alldata Order By id Desc Limit 50')
		data=c.fetchall()
		for ctn in data:
			dateString=s.formatTime(ctn[2])
			precnt=quoteToJavascrip(ctn[1])
			qz_body+=r'''document.write(getFormattedContentAsString('{content}','{datetime}',{id}));'''.format(content=precnt,datetime=dateString,id=ctn[0])+'\n'
	qz_body+=r'''</script>
	</div>
	<footer>
	<p id='foot_content'><u>http://www.you.cannot.visit.com</u></p>
	</footer>	
	</div>
	'''

	qz_html=hf.format_html(head=additional_head,title=qz_title,style=qz_style,body=qz_body)
	return [0,qz_html]
