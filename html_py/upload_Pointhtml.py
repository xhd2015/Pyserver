#!/bin/python3

from urllib.parse import unquote_to_bytes
import time

def generate_html(s):
    sf=s.sf
    sq=s.sq
    
    
    data=sf.getPostData(s)#.decode('u8')
     #posted data read as bytes
   # print(data)
    data=data.replace(b'+',b'%20')
   # print(data)
    #在此阶段，sp转换为+，+正常转换
    #input()
    data=sf.parseArgData(data.decode('u8'))
 
    content=unquote_to_bytes(data['content']).decode('u8')
    #print('XXX:',len(content))
    clear=data.get('clear','')
   
    #一时疏忽，把数据库clear了
    with sq.connect(s.dbs) as conn:
       
        c=conn.cursor()
  
            
        if len(content)>0:
            
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
            c.execute('''
                INSERT INTO alldata VALUES(?,?,?)
                ''',(last,content,time.time())
                )
        conn.commit()
    #htitle='提交成功'
    #hbody='''<p>提交成功 ， <a href='/'>返回</a></p>'''
    #hf.send_html(s,hf.format_html(title=htitle,body=hbody))
    return ['/index.html']