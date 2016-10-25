#-*-coding:utf8;-*-
#qpy:3
#qpy:console

base_html=(r'''
<!DOCTYPE html>
<html>
<head>
	<meta charset='utf-8'/>
    {0[0]}
    <style type='text/css'>
        {0[1]}
    </style>
</head>
<body>
    {0[2]}
</body>
</html>'''
,('head','style','body'))

regular_html=(
r'''
<!DOCTYPE html>
<html>
<head>
    <title>{0[0]}</title>
	<meta charset='utf-8'/>
    <meta name="viewport" content="initial-scale=1.0, minimum-scale=1.0=
">
    <script>
{0[4]}
    </script>
    <style type='text/css'>
        pre{{
           white-space: pre-wrap;
           white-space: -moz-per-wrap;
           word-wrap: break-word;
        }}
        {0[1]}
    </style>
    {0[2]}
</head>
<body>
    {0[3]}
</body>
</html>'''
,('title','style','head','body','script'))
	
#200 OK
def send_html(s,html,content_type='text/html; charset=utf-8'):
	__doc__=r'''response必须是200'''
	if type(html) in {str,bytes}:#必须保证发送的数据是可编码流，如果是空数据，表面只发送一个头部
		try:
			eHtml=html.encode('u8')
		except AttributeError as e:#该文件可能已经编码过
			eHtml=html
		s.send_response(200)
		if content_type:
			s.send_header('content-type',content_type)
		s.send_header('content-length',len(eHtml))
		s.end_headers()
		s.wfile.write(eHtml)

#200 OK
def send_data(s,data,content_type=None):
	__doc__='''必须保证发送的数据非空并且为二进制流'''
	if type(data)==bytes:#
		s.send_response(200)
		if content_type:
			s.send_header('content-type',content_type)
		s.send_header('content-length',len(data))
		s.end_headers()
		s.wfile.write(data)
		
#301 moved permanently
#302 moved temperory
def send_redirect(s,location,response=302):
    s.send_response(response)
    s.send_header('Location',location)
    s.end_headers()
    
#404 not found
def send_notfound(s):
    s.send_response(404)
    s.end_headers()
    
 #500 internal erro
def send_internerror(s):
	s.send_response(500)
	s.end_headers()

    
def format_html(fmt=regular_html,**eles):
    #from collections import defaultdict as fdct
    v=[]
    for k in fmt[1]:
        v.append(eles.get(k,''))
    return fmt[0].format(v)
        	
        	
def mktag(tag,content='',**props):
    strict_single={'br'}
       
    prop=''
    propfmt='{name}="{value}" '
    for pk,pv in props.items():
        prop+=propfmt.format(name=pk,value=pv)
    res='<'+tag+' '+prop
    if tag in strict_single:
        res+='/>'
    else:
        res+='>'+content+'</'+tag+'>'
    return res
def mknote(content):
    return '<!-- {} -->'.format(content)
def trim_html(html):
    pass
    

#__name__='__test__'
if __name__=='__test__':
    h=format_html(title='haha',body='<p>呆</p>')
    print(h)
   
    input()
    t=mktag('select','狡猾',name='h',value='r')
    t=mktag('br')
    print(t)
