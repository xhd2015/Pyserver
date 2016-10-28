/**
 * 
 * 
 * rely-->
 *	 	Utils{toJSONDict}
 * 		Hdata_support
 * 
 * 
 * 设计的原则:
 * 1.更少的js代码,更多的html设计
 * 2.在已有基础上进行修改,而不是自定义
 * 
 * 在form的基础上进行修改
 * 
 */

Ajaxform_support={};

(function($$){


/**
*上下文由e.data.self
* 
* 增加上下文:
* 	e.data.jform
* 	e.data.action
* 	e.data.url -- 这个是重复的,可以从jform中获取
*/
$$.submitPerform=function(e){
	//alert(JSON.stringify($(this).serializeArray()));
	
	let jself=e.data.jself;
	let thisform=jself.parent("form");//找到元素form
	let url=thisform.attr("action");
	let subaction=jself.attr("action");//找到子类型action
	
	e.data.jform=thisform;
	e.data.url=url;
	e.data.action=subaction;
	
	let data=e.data.getData(e);
	
	$.post(url,JSON.stringify(data),function(resp){
		e.data.resp=resp;
		e.data.onResp(e);
	});
		
}
$$.defaultOnResp=function(e){
	console.log(e.data.resp);
}
/**
 * action属性来自submit的action属性
 * 这个defaultGetData意指将数据将数据json化,然后添加其action属性.
 * 注意,你有可能input name=action,name action会有多个值
 */
$$.defaultGetData=function(e){
	let formdata=e.data.jform.serializeArray();
	formdata.push({"name":"action","value":e.data.action});
	return Utils.toJSONDict(formdata);
}
/**
 * 将数据化成action:,data:的形式
 * @depreciated
 */
$$.standardActionData=function(e){
	let data=$$.defaultGetData(e);
	let thisdata={};
	thisdata.action=data.action;
	delete data.action;
	thisdata.data=data;
	console.log(JSON.stringify(thisdata));
	return thisdata;
}
/**
 * 获取Hdata格式
 * 
 * 某些特性,如""作为undefined处理
 */
$$.actionHdata=function(e){
	return {"action":e.data.action,
			"data":Hdata_support.data(e.data.jform)
		}
	
}
$$.actionHdataNull=function(e){
	return {
		"action":e.data.action,
		"data":Hdata_support.getAccessData(e.data.jform,true)
	}

	
}

/**
 * 这个函数设置form的每个submit的上下文.
 * 
 * 在使用了clone(false)之后的form中,使用此函数重新注册submit事件.
 * 
 * 上下文包括:
 * 	e.data.jself
 * 	e.data.getData
 * 	e.data.onResp -- 如果使用clone,那么考虑到频繁的eval函数是低效的,因此建议最好使用统一的函数设置而非定义新的函数
 * 
 * 所有submit共用一个响应函数:
 * 		submitPerform
 * 
 * 返回:
 * 	所有重新设置了上下文的form对象
 */
$$.registerAjaxForm=function(jform){
	if(!jform)
	{
		jform=$("form");
	}
	jform.submit(function(){return false;});//注销预定义的submit
	jform.find(":submit").each(function(){
		let jself=$(this);
		let defmap={"getData":$$.defaultGetData,
				"onResp":$$.defaultOnResp,
				};
		for(let key in defmap)
		{
			let attr=jself.attr(key);
			let f;
			if(attr){	
				try{
					f=eval(attr);
				}catch(e){
					console.log("exception eval "+key+" . "+e);
				}
			}
			if(f &&( typeof f===typeof $))
			{
				defmap[key]=f;
			}
			
		}
		defmap["jself"]=jself;
		jself.off("click");//取消原来的click函数,无论是clone(true)还是clone(false)
		jself.click(defmap,$$.submitPerform);
	});
	return jform;
}

$(document).ready(function(){
	$$.registerAjaxForm();
});


	
}(Ajaxform_support));






