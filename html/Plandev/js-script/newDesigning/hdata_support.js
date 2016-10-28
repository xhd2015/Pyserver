/**
 * rely-->
 * 		
 *hdata意思是HTMLData
 */
Hdata_support={};
(function($$){

/**
 * 设置或者获取所有的内含name属性的值,access指定其获取方法,默认input,textarea,select为val,其他为html
 * 注意,这里指定的是jQuery的获取方法
 *
*
 * 除了jdom之外,
 * 	无参数   获取所有data
 * 	一个参数	设置data
 * 
 * done 2016.10.18 18.22
 */
$$.data=function(jdom,setdata){
	if(setdata)//一个参数
	{
		$$.setAccessData(jdom,setdata);	
	}else{
		
		return $$.getAccessData(jdom);
	}
}
/**
 * 获取name的数据
 * 如果值为空,不获取
 * 如果有多个相同的键,则添加成数组
 * 
 * issue: 对checkbox,radio的选项进行改进 2016-10-26 15:19:16
 */
$$.getAccessData=function(jdom,nullable)
{
	let data={};
	jdom.find("[name]").not("[disabled]").each(function(){
		let jself=$(this);
		//如果是多选按钮,单选按钮,只选择选中的
		if(jself.is(":checkbox") || jself.is(":radio"))
			{
				if(!jself.is(":checked"))
					{
						return;
					}
			}
		let key=jself.attr("name");
		//仅当不为空的时候加入这个值
		//当为checkbox的时候只选择checked
		let srcVal=jself[$$.getAccess(jself)]();
//		alert("srcval:"+srcVal);
		if(nullable || srcVal)
		{
			if(!(key in data)) //如果还不存在
			{
				data[key]=srcVal;
			}else if(typeof data[key]===typeof []){//如果是数组
				data[key].push(srcVal)
			}else{//已经存在一个单值类型,需要转换成数组{
				data[key] = [ data[key] ];
				data[key].push(srcVal)
			}
		}
	});
	return data;
}
/**
 * 
 * 设置含有name的data.如果某一个键是数组,就会将其逐个赋值
 * 
 * 一般情况下,会认为组名是足够数据存放的;但是有的时候组数不定,可能需要使用更好的自动适应的列植. 多了就删除,少了就新建. 与行为有关
 * 
 * issue:
 * 		radio -- 数据设置时不再是普通的getAccess,而是checked属性
 * 		checkbox -- 等需要用到再说吧
 */
$$.setAccessData=function(jdom,data)
{
	jdom.find("[name]").not("[disabled]").each(function(){
		var jself=$(this);
		var key=jself.attr("name");
		if(key in data)
		{
			let realdata;
			if($.isArray(data[key]) && data[key].length > 0)
			{
				realdata=data[key][0];
				data[key].shift();
			}else{
				realdata=data[key];
			}
			//如果是radio button或者checkbox,使用checked选项
			if(jself.is(":radio"))
			{
				if(realdata===jself.val())
				{
					jself.attr("checked","");
				}
			}else{
//				alert("key :"+key+" realdata:"+realdata+" before :"+jself[$$.getAccess(jself)]());
				jself[$$.getAccess(jself)](realdata);
//				alert("after :"+jself[$$.getAccess(jself)]());
			}
			
		}
	});
}
/**
 * 清除数据
 */
$$.reset=function(jdom){
	jdom.find("[name]").not("disabled").each(function(){
		var jself=$(this);
		jself[$$.getAccess(jself)]("");
	});
	return jdom;
}
/**
 * 获取所有的键
 */
$$.keys=function(jdom){
	let keys=[];
	jdom.find("[name]").not("[disabled]").each(function(){
		var jself=$(this);
		var key=jself.attr("name");
		keys.push(key);
	});
	return keys;
}
/**
 * 获取元素的值设置类型
 */
$$.getAccess=function(jitem){
	let valMap={"textarea":"","input":"","select":""};
	let method=jitem.attr("access");
	let tagName=jitem.get(0).tagName.toLowerCase();
	if(!method)
	{
		if(tagName in valMap)
		{
			method="val";
		}else{
			method="html";
		}
	}
	return method;
}
	
	
}(Hdata_support));
