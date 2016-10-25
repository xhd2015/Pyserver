

def generate_html(s):
	title='SQLite3 Execution !!!'
	script=r'''
		function execPython()
		{
			var inputer=document.getElementById('pycode');
			var pyresult=document.getElementById('pyresult');
			if(inputer.value){
				var prevalue=inputer.value
				var xhr=new XMLHttpRequest();
				xhr.onreadystatechange=function(){
					if(xhr.readyState==4 && xhr.status==200)
					{
						pyresult.value+=prevalue+':\n';
						pyresult.value+='\t'+xhr.responseText+'\n';
					}
				};
				xhr.open('POST','/script/sqlite3_exec_postdata.html',true);
				xhr.send(inputer.value);
				inputer.value='';
			}
		}
	
	'''
	style=r'''
	#pycode , #pyresult{
		width: 90%;
	}
	#pycode{
		height: 5em;
	}
	#pyresult{
		height:	15em;
	
	}
	'''
	body=r'''
		<textarea id='pycode' ></textarea>
		<br />
		<button id='submit' onclick='execPython();'>提交</button>
		<button onclick='document.getElementById("pyresult").value="";'>清除</button>
		<hr />
		<textarea id='pyresult' readonly style="overflow-y: scroll;" ></textarea>
	'''
	html=s.hf.format_html(title=title,script=script,body=body,style=style);
	return [0,html]
