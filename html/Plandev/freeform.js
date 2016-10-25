//=====Example Freeform START====
/**
	<!--需要编写的就是 onresp,targeturi,class="freeforminput",name; 这就是模式化-->
	<div class="freeform" targeturi="/Plandev/ajax-services/postfeedback.html" onresp="setItems">
		<textarea name="text" class="freeforminput" access="val"></textarea> <br/>
		<button name="submit">Submit</button>
		<button name="clear">Clear</button>
	</div>
	 //dot't forget to register it
	registerFreeform();
*/
//=====Example Freeform END  ====
//=====Freeform START=======
function getattr($self,key,defaultvalue)
{
	//mapping like {"access":"val"} ,键和默认值
	if($self.attr(key))
	{
		return $self.attr(key);
	}else{
		return defaultvalue;
	}
}
function getFreeformInput($form)
{
	//只要是.freeforminput都获取
	//不接受多值输入
	var data={};
	$form.find(".freeforminput").each(function(index,self){
		var $self=$(self);
		var method=getattr($self,"access","val");
		var keyname=getattr($self,"name","unknownkeyname");
		if(method in $self)
		{
			var x=$self[method]();
			if(x)
			{
				data[keyname]=$(self)[method]();
			}
		}
	});
	//console.log("getFormData:"+JSON.stringify(data));
	return data;
}
function clearFreeFormInput(argBtn)
{
	$(argBtn).parent().find(".freeforminput").each(function(index,self){
		var method=$(self).attr("access")?$(self).attr("access"):"val";
		($(self)[method])("");
	});
}
//access定义访问的方法,默认为val
//**测试:当网页中有多个freeform是否正常工作
function registerFreeform()
{
	//所有的input[type=text] textarea都是输入项class为freeforminput也是,除非特别指定它们不能作为freeforminput
	$(".freeform").find("input[type=text],textarea").not(".notfreeforminput").addClass("freeforminput");
	//如果有submit的click对象
	$(".freeform").find("[name=submit]").click(function(e){
		var $form=$(this).parent(".freeform");
		var uri=$form.attr("targeturi");
		var respfunc=$form.attr("onresp");
		
		if(! uri)
		{
			throw Error("No URI given");
		}
		if( !respfunc)
		{
			respfunc=function(res){
				alert(res);//默认的函数
			};
		}
		var data=JSON.stringify(getFreeformInput($form));
		$.post(uri,data,function(res){
			if(typeof respfunc == "function")
			{
				respfunc(res,$form);
			}else if(typeof respfunc == "string" && window[respfunc]){
				window[respfunc](res,$form);
			}
		});
	});
	//如果由clearinput的对象
	$(".freeform").find("[name=clear]").click(function(e){
		clearFreeFormInput(this);
	});
}

//=====Freeform END=======
