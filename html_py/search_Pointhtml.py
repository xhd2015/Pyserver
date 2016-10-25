#!/bin/python3
from urllib.parse import unquote_to_bytes
import time

def generate_html(s):
    sf=s.sf
    sq=s.sq
    hf=s.hf

    data=sf.getPostData(s)#.decode('u8')
 
    data=data.replace(b'+',b'%20')
   
    data=sf.parseArgData(data.decode('u8'))
    scontent=unquote_to_bytes(data.get('scontent','')).decode('u8')
    res=[]
    if scontent:
        with sq.connect(s.dbs) as conn:
            c=conn.cursor()
            c.execute('SELECT * FROM alldata')
            fetchdata=c.fetchall()
            
            for d,i in enumerate(fetchdata):
                if i[1].find(scontent)!=-1:
                    res.append(d)

    html_style='''body{font-size: 3em;}'''
    html_body='''<lable>搜索结果</label><br />'''
    if len(res):
        for i in reversed(res):
            ctn=fetchdata[i]
        
            a=time.localtime(ctn[2])
            
            subfmt='0>2d'
            datefmt='{1}.{2:{0}}.{3:{0}} {4:{0}}:{5:{0}}:{6:{0}}'
            b=datefmt.format(subfmt,a.tm_year,a.tm_mon,a.tm_mday,a.tm_hour,a.tm_min,a.tm_sec)
            precnt=ctn[1].replace('&','&amp')
            precnt=precnt.replace('<','&lt')
            precnt=precnt.replace('>','&gt')
            html_body+=s.content_fmt.format(content=precnt,date=b,id=ctn[0])
            
    else:
        html_body+='<p>无{}搜索结果</p>'.format('"'+scontent+'"')
        
        
    html_body+='''<a href="/" >返回</a>'''
    html=hf.format_html(body=html_body)
    
    return ['',html]