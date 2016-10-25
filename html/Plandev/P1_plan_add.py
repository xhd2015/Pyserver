


'''
我们将设计划分为以下几部分:
	1.设计输入  --  这个可以由一般的函数生成,html生成
	2.输入获取  --  同上,javascript生成
	3.提交并在服务器端存储  --  使用sqlite和python完成
	4.查看所有的计划

设计需要注意的一些细节:
	1.将某些函数通用化
		比如生成JSON数据的表单
	2.输入的字符串去除首尾空白(当然,最好不要这样做)

******帮助信息
each函数
	$(selector).each(function(index,element)) , index位置,element为元素
'''

import __plandev_library as plandev

def generate_html(s):
	#目前还不支持处理可变的同类型数据
	title="Addddd"
	script=r'''
</script>
<script src='/jquery-3.1.0.min.js'></script>
<script src='/Plandev/freeform.js'></script>
<script>
function setPrompt(text){
	$("#pending").find(".prompt").html(text);
}
function setPromptForAdd(resp,$form){
	var rdata=JSON.parse(resp);
	if(rdata["status"]=="failed")
	{
		setPrompt("failed , reason : "+rdata["default"]);
	}else{
		setPrompt("successful.id : "+rdata["id"]+" , datetime : "+rdata["datetime"]);
	}
}

$(document).ready(function(){
	registerFreeform();
});	

'''
	body=r'''	<a href="/Plandev/P1_plan_add.html">Add</a> <br/>
	<a href="/Plandev/P1_plan_showitems.html">Show All Items</a><br/>
	<a href="/Plandev/feedback.html">Post a Feedback</a> <br/>
	<a href="/Plandev/index.html">Index</a> <br/>
	<div class="freeform" targeturi="/Plandev/ajax-services/addplan.html" onresp="setPromptForAdd">
		<pre>Title        <input type="text" name="title"></input> </pre>
		<pre>Description  <textarea name="description"></textarea> </pre>
		<pre>Universal    <input type="text" name="universal"></input> </pre>
		<pre>     Part 1    <textarea name="p1"></textarea> </pre>
		<pre>     Part 2    <textarea name="p2"></textarea> </pre>
		<pre>     Part 3    <textarea name="p3"></textarea> </pre>
		<pre>     Part 4    <textarea name="p4"></textarea> </pre>
		<pre>     Part 5    <textarea name="p5"></textarea> </pre>
		<button name="submit">Submit</button>
		<button name="clear">Clear</button>
	</div>
	<a href="/Plandev/P1_plan_showitems.html" target="_blank">Show All Plans</a>
	<div id="pending">
		<p class="prompt"></p>
	</div>

'''
	
	head=r''''''

	body+=plandev.get_content(s.html_dir+"/Plandev/footer.html")

	html=s.hf.format_html(title=title,head=head,script=script,body=body)
	return [0,html]
