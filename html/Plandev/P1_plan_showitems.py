import __plandev_library as plandev
#plan可以任意多
#通用性很受考验
def generate_html(s):
	head=''
	style=r'''
	
	.item_change .title,.item_show .title{
		font-size:2em;
		color: rgb(255,20,200);
	}
	.item_change .description, .item_show .description{
		font-size:1.4em;
		color:rgb(20,200,255);
	}
	.item_change .universal, .item_show .universal{
		font-size:1.2em;
		color:rgb(200,255,20);
	}


	'''
	title="Quertssss"
	script=r'''
	</script><script src='/jquery-3.1.0.min.js'></script><script>
	function setSingleItem($item,stuff)
	{
		for(var i in stuff)
		{
			$item.find("."+i).html(stuff[i]);
		}
	}
	function showAllItems(respdata)
	{
		clearAllShown();
		$holder=$("#items_holder")
		$template=$holder.find(".item_show_example");
		
		for(var i in respdata)
		{
				$cloned=$template.clone().removeClass("item_show_example").addClass("item_show").show();
				$holder.append($cloned);
				setSingleItem($cloned,respdata[i]);
		}
	}
	function clearAllShown()
	{
		$("#items_holder").find(".item_show").remove();
	}
	function getAllPlanData()
	{
		//q=[all] 表明查询所有数据
		//不要在查询中使用多值键
		getPlanData({"q":"[all]"});
	}
	//pattern是形如 {q:xxx}的形式,q,xxx中  { = & ? / : } , 被转义
	function getPlanData(pattern)
	{
		$.post("/Plandev/ajax-services/findplans.html",JSON.stringify(pattern),function(resp){
			data=JSON.parse(resp);
			data=data.reverse()
			showAllItems(data);
		});
	}
	
	//for delete START
	function getIdOfItems($items)
	{
		//使用,分割
		var ids="";
		$items.each(function(index,self){
			ids+=$(self).find(".id").html()+",";
		});
		return ids;
	}
	//for single item
	function postDeletePlan(argBtn)
	{
		var $item=$(argBtn).parent().parent();
		var id=getIdOfItems($item);
		//应当将id视为一组数据,因为可能需要同时删除多组id
		$.post("/Plandev/ajax-services/deleteitems.html",JSON.stringify({"id":id}),function(resp){
			if(resp=="error")
			{
				alert("Deleting "+id+" returns error");
			}else if(resp=="success"){
				$item.remove();
			}
		});
	}
	//for delete END
	
	//======FOR CHANGE START======
	function getChangeForm($origin)
	{
		var changeClasses=["title","description","universal","p1","p2","p3","p4","p5"];
		var $templateChange=$(".item_change_example").clone().removeClass("item_change_example").addClass("item_change").show();
		
		//id单独设置
		$templateChange.find(".id").html($origin.find(".id").html());
		for(var i in changeClasses)
		{
			$templateChange.find("."+changeClasses[i]).val($origin.find("."+changeClasses[i]).html());
		}
		return $templateChange
	}
	function retrivToShow($change_form)
	{
		var changeClasses=["title","description","universal","p1","p2","p3","p4","p5"];
		var $origin=$change_form.prev();
		for(var i in changeClasses)
		{
			$origin.find("."+changeClasses[i]).html($change_form.find("."+changeClasses[i]).val());
		}
		$change_form.remove();
		$origin.show();
	}
	function changeToModify(argBtn)
	{
		var $origin=$(argBtn).parent().parent();
		var $change=getChangeForm($origin);
		$origin.after($change).hide();
	}
	function cancleChange(argBtn)
	{
		var $parent=$(argBtn).parent().parent();
		var $origin=$parent.prev();
		$parent.remove();
		$origin.show();
	}
	function getChangeData($item_change)
	{
		var data={};
		//id单独获取
		data["id"]=$item_change.find(".id").html();
		$item_change.find("input").each(function(index,self){
			var classname=$(self).attr("class");
			data[classname]=$(self).val();
		});
		return JSON.stringify(data);
	}
	function confirmChange(argBtn)
	{
		var data=getChangeData($(argBtn).parent().parent());
		$.post("/Plandev/ajax-services/changeplan.html",data,function(resp){
			if(resp=="error")
			{
				$(".prompt_holder").find(".prompt").html("error,can't change.");
				cancleChange(argBtn);
			}else if(resp=="success"){
				retrivToShow($(argBtn).parent().parent());
			}
		});	
		
	}
	//======FOR CHANGE END  ======
	
	$(document).ready(function(){
		getAllPlanData();
	});
'''
	#对于show item, 所有的class必须与返回的key相同,并且支持html()方法设置参数
	#定义返回的数据为JSON解析
	body=r'''
	<a href="/Plandev/P1_plan_add.html">Add</a> <br/>
	<a href="/Plandev/P1_plan_showitems.html">Show All Items</a><br/>
	<a href="/Plandev/feedback.html">Post a Feedback</a> <br/>
	<a href="/Plandev/index.html">Index</a> <br/>
	<div class="freeform">
		<input type="text" name="text"></input>
		<button onclick="getInputData(this);">Search</button>
	</div>
	<hr/>
	<div class="prompt_holder">
		<p class="prompt"></p>
	</div>
	<div id="items_holder">
		<div class="item_show_example" style="display:">
			<p>*********************************</p>
			<p class="id" style="display:none">Plan Id</p>
			Title : <label class="title">Title</label> <br/>	
			Description : <span class="description">Description</span> <br/>
			Universal : <span class="universal">Universal</span> <br/>
			<ul>
				<li><p class="p1">p1</p>
					<select>
						<option>--status--</option>
						<option>done</option>
						<option>undone</option>
					</select>
				</li>
				<li><p class="p2">p2</p></li>
				<li><p class="p3">p3</p></li>
				<li><p class="p4">p4</p></li>
				<li><p class="p5">p5</p></li>
			</ul>
			<div class="operation">
				<button onclick="postDeletePlan(this);">Delete</button>
				<button onclick="changeToModify(this);">Change</button>
			</div>
		</div>
		<div class="item_change_example" style="display:none">
			<p>*********************************</p>
			<p class="id" style="display:none">Plan Id</p>
			Title : <input type="text" class="title" value="Title"></input> <br/>
			Description : <input type="text" class="description" value="Description"></input> <br/>
			Univeral : <input type="text" class="universal" value="Universal"></input> <br/>
			<ul>
				<li><input type="text" class="p1" value="p1"></input></li>
				<li><input type="text" class="p2" value="p2"></input></li>
				<li><input type="text" class="p3" value="p3"></input></li>
				<li><input type="text" class="p4" value="p4"></input></li>
				<li><input type="text" class="p5" value="p5"></input></li>
			</ul>
			<div class="operation">
				<button onclick="cancleChange(this);">Cancle</button>
				<button onclick="confirmChange(this);">Confirm</button>
			</div>
		</div>
	</div>
'''
	body+=plandev.get_content(s.html_dir+"/Plandev/footer.html")
	html=s.hf.format_html(title=title,body=body,head=head,script=script,style=style)
	return [0,html]
