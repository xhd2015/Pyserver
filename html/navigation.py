import os
def listdir_R(f,html_dir=''):
	curpath=html_dir+'/'+f;
	if os.path.isdir(curpath):
		res=f+'\n'
		for i in os.listdir(curpath):
			res+=listdir_R(f+'/'+i,html_dir)
	elif f.endswith(".html"):
		res='<a href="'+f+'">'+f+'</a>'+'\n'
	elif f.endswith(".py") and f not in ['/initShares.py']:
		res='<a href="'+f[:-3]+".html"+'">'+f[:-3]+".html"+'</a>\n';
	else:
		res=''
	return res


def generate_html(s):
	title='Navigation for Douglas Fulton Shaw'
	script=r'''</script>
	<script src='/jquery-3.1.0.min.js'></script><script>
	$(document).ready(function(){
		$('a').attr('target','_blank');
	
	});
	'''
	body='<pre>'+listdir_R('',s.html_dir)+'</pre>';
	body+=r'''
	
	<footer>
		About more source info,see <a href="/debuginfo.html">here</a>
	</footer>
	'''
	html=s.hf.format_html(title=title,script=script,body=body);
	
	return [0,html]
