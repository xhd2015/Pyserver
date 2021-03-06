#!/bin/python3
import sys
sys.path.append('/home/Fulton Shaw/libpython')
import htmlutil_fulton as hf
import sqlite3 as sq
import time


def generate_html(s):
    '''响应式设计范例'''
    qz_title='AQzLike'
    qz_style='''
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
div#footer{
width: 100%;
}
p#foot_content{
float: center;
}
form textarea{
width: 100%;
height: 5em;
font-size: 1em;
}
form input{
font-size: 1em;
}
form input[name=scontent]{
width: 80%;
float: left;
}
form input[value=查找]{
    width: 20%;
    float: left;
}
'''
    qz_body='''
<div id='container'>
<div id='prompter'>
<label>----内容----</label>
</div>
<div id='inputter'>
<form action="./upload.html" method="post">
<textarea name="content">
</textarea>

<br/>  <!--我去年换了个行-->
<input type="checkbox" value='c' name='clear' disabled='disabled'>清除</input>
<input type="submit" value="提交"/>
</form>

<form action='/search.html' method='post'>
<input type='text' name='scontent'/>
<input type='submit' value='查找'/>
</form>
</div>
<div id='lister'>
<hr/>
'''

    with sq.connect(s.dbs) as conn:
        c=conn.cursor()
        c.execute('SELECT * FROM alldata')
        data=c.fetchall()
        for ctn in reversed(data):
            a=time.localtime(ctn[2])
            
            subfmt='0>2d'
            datefmt='{1}.{2:{0}}.{3:{0}} {4:{0}}:{5:{0}}:{6:{0}}'
            b=datefmt.format(subfmt,a.tm_year,a.tm_mon,a.tm_mday,a.tm_hour,a.tm_min,a.tm_sec)
            precnt=ctn[1].replace('&','&amp;')
            precnt=precnt.replace('<','&lt;')
            precnt=precnt.replace('>','&gt')
            qz_body+=s.content_fmt.format(content=precnt,date=b,id=ctn[0])
    qz_body+='''
    </div>
   <div id='footer'>
       <p id='foot_content'><u>http://www.you.cannot.visit.com</u></p>
   </div>
   </div>
'''
    
    qz_html=hf.format_html(title=qz_title,style=qz_style,body=qz_body)
    return ['',qz_html]