
#post /echo.html --data '${data}'
__doc__='''提供echo 服务'''
def generate_html(s):
	data=s.sf.getPostData(s)
	return [2,data]
