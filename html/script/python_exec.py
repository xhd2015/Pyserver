

def generate_html(s):
	title='Python Execution !!!'
	script=r'''
		function execPython()
		{
			var inputer=document.getElementById('pycode');
			var pyresult=document.getElementById('pyresult');
		
			var xhr=new XMLHttpRequest();
			xhr.onreadystatechange=function(){
				if(xhr.readyState==4 && xhr.status==200)
				{
					pyresult.value=xhr.responseText;
				}
			};
			xhr.open('POST','/script/python_exec_postdata.html',true);
			xhr.send(inputer.value);
		}
	'''
	style=r'''
	#pycode , #pyresult{
		width: 90%;
	}
	#pycode{
		height: 20em;
	}
	#pyresult{
		height:	10em;
	
	}
	'''
	body=r'''
		<textarea id='pycode' ></textarea>
		<br />
		<button id='submit' onclick='execPython();'>提交</button>
		<hr />
		<textarea id='pyresult' readonly ></textarea>
	'''
	html=s.hf.format_html(title=title,script=script,body=body,style=style);
	return [0,html]
