/**
作为扩展的建议: 所有的子类型都应当一致的支持item中所定义的函数,或者重写它们使其符合标准
*/
//========================
//class def
/**
 * 
 */
function Itemshow($dom)
{
	if(Itemshow.isItemshow($dom))
	{
		this.$dom=$dom;//除了包装之外,没有别的属性,其他属性存储到$dom.data中
	}
	else
	{
		throw "DOM is not '.itemshow'";
	}
	
}
(function($$){
//========================
//statics properties
$$.MAINCLASS="itemshow";
$$.ITEMMARK="access_key";
$$.IDMARK="itemid";
$$.CHANGE="change";
$$.DELETE="delete";
$$.CANCLE="cancle";
$$.CONFIRM="confirm";
$$.CLEAR="clear";
$$.TRANSTO="transto";
$$.classes=["confirm","delete","clear","cancle","change"];
$$.defaultAccessMapping={
	"input":"val",
	"textarea":"val",
	"select":"val",
	"*":"html",
}
$$.defaultTransferMapping={
	"p":"input",
	"pre":"textarea",
	"textarea":"pre",
	"input":"p",
	"span":"input",
	"*p":"textarea",
	"*":"p"
}


//========================
//methods
/**
 * 如果按钮不是默认的类,就使用my+key键.名称必须加上前缀my
 * 如mydelelet
 * 当然,这并不是强制性的,但最好这样做
 * 
 * reg(key,f)注册相应的类.如果f缺失,就从Itemshow.defonclickfs中查找相应的函数
 * 注册时,通过设置f
 * key 是click的类名
 * 通过clickargs获取这个数据,clickargs.item就是itemthis对象
 * farr是二元组 (func,args={})
 * 
 */
$$.prototype.reg=function(key,farr) 
{
	$$.regItem(this,key,farr);
}
/**
 * 对一个项进行监听注册
 */
$$.prototype.regDefault=function(){
	$$.registerItemshow(this.getJDom());
	return this;
}

/**
 * 获取对应的jdom对象
 */
$$.prototype.getJDom=function(){
	return this.$dom;
};

/**
 * 0参数
 * 1参数  字符串,过滤函数 jdoms f(jdoms)
 * 
 */
$$.prototype.subitems=function(filter)
{
	var jset=this.$dom.find("["+$$.ITEMMARK+"]");
	var type=typeof filter;
	if(type === typeof undefined)//no argument
	{
		//do nothing
	}
	if(type===typeof "")
	{
		jset=jset.filter(filter);
	}else if(type === typeof $){//如果是函数,则是一个过滤函数.接受所有的access,返回新的选择器集合
		jset=filter(jset);
	}
	return jset;
}
/**
 * data指定键值对
 * filter指定过滤函数或者过滤字符串
 * 
 * 无参数   获取所有data
 * 有一个参数	为function类型或者str类型,获取过滤的所有data
 * 			为其他类型,设置
 * 有两个参数 第一个是obj,第二个是过滤字符串或过滤函数
 * 
 * done 2016.10.18 18.22
 */
$$.prototype.data=function(arg1,arg2 /*data,filter*/){
	var subs;
	if(arg1)
	{
		if(arg2)//两个参数
		{
			subs=this.subitems(arg2);
			$$.setAccessData(subs,arg1);
		}else{//一个参数
			if((typeof arg1===typeof $) ||(typeof arg1 === typeof "") )//是过滤类型
			{
				subs=this.subitems(arg1);
				return $$.getAccessData(subs);
			}else{//是obj类型
				$$.setAccessData(this.subitems(),arg1);
			}
		}
	}else{
		return $$.getAccessData(this.subitems());
	}
}
/**
 *set for access_key=p
 */
$$.prototype.setStrOrData=function(p)
{
	var data={};
	if(typeof p===typeof "")
		data.p=p;
	else
		data.p=JSON.stringify(p);
	this.data(data);
}
/**
 *add for access_key=p
 */
$$.prototype.addStrOrData=function(p)
{
	var data=this.data();
	var strp;
	if(typeof p===typeof "")
		strp=p;
	else
		strp=JSON.stringify(p);
	data.p+='\n'+strp;
	this.data(data);
}



//========================
//static functions
$$.isItemshow=function($dom){
	return $dom.is("."+$$.MAINCLASS+"["+$$.IDMARK+"]");
}
/**
 * 
 * 设置含有access_key的data
 */
$$.setAccessData=function(jdoms,data)
{
//	alert(typeof jdoms);
	jdoms.each(function(){
		var jself=$(this);
		var key=jself.attr($$.ITEMMARK);
		if(key in data)
		{
			jself[$$.getAccess(jself)](data[key]);
		}
	});
}
/**
 * 获取access_key的数据
 * 如果值为空,不获取
 * 如果有多个相同的键,则添加成数组
 * 
 */
$$.getAccessData=function(jdoms)
{
	let data={};
	jdoms.each(function(){
		let jself=$(this);
		let key=jself.attr($$.ITEMMARK);
		//仅当不为空的时候加入这个值
		let srcVal=jself[$$.getAccess(jself)]();
		if(srcVal)
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
 * return if id exists,return the first
 * else return undefined.
 */
$$.findId=function(id)
{
	var jdom=$$.findIdAsJDom(id);
	//alert("."+$$.MAINCLASS+"["+$$.IDMARK+"="+id+"]");
	//alert(jdom.length);
	if(jdom.length>0)
	{
		return new Itemshow(jdom.first());
	}else{
		return undefined;
	}
}
/**
 * 无参数时返回所有的itemshow
 * 
 */
$$.findIdAsJDom=function(id)
{
		var strQuery="."+$$.MAINCLASS+"["+$$.IDMARK;
		if(id)
		{
			strQuery+="="+id;
		}
		strQuery+="]";
		return jdom=$(strQuery);
		
}
/**
 * arg可以是jdom或者字符串tagName
 */
//done
$$.getAccess=function(arg)
{
	if(typeof arg === typeof $("<br/>")){
		let access=arg.attr("access");
		let tag=arg.get(0).tagName.toLowerCase();
		return access || $$.getAccess(tag);
	}else if(typeof arg === typeof "p")
	{	
		
		return $$.defaultAccessMapping[arg] || $$.defaultAccessMapping["*"];
	}
	else
		return undefined;
}
/**
 * 
 * 将一个dom项复制出它的希望转换的项
 * access属性是默认的.
 * 
 */
Itemshow.getChangeTypeOfElement=function(jdom,additionMappings){
	//构造一个新表
	if(!additionMappings)
	{
		additionMappings={};
	}
	for(var i in Itemshow.defaultTransferMapping)
	{
		if(!(i in additionMappings))
		{
			additionMappings[i]=Itemshow.defaultTransferMapping[i];
		}
	}
	//获取对应的转换名,应当在mapping提供
	var oriTag=jdom.get(0).tagName.toLowerCase();
	var dstTag=additionMappings["*"];
	if(oriTag in additionMappings)
	{
		dstTag=additionMappings[oriTag];
	}
	var targetHTML="<"+dstTag+"></"+dstTag+">";
	
	jdom[$$.getAccess(jdom)]()
	var jtdom=$(targetHTML);
	jtdom[$$.getAccess(dstTag)](jdom[$$.getAccess(oriTag)]());//设置值属性
	var attrs=jdom.get(0).attributes;
	//复制属性
	for(var i=0;i<attrs.length;i++)
	{
		var attrname=attrs[i]["nodeName"];
		var attrval=attrs[i]["value"];
		jtdom.attr(attrname,attrval);//属性复制
	}
	
	return jtdom;
	
}
/**
 * 将from的数据转移到jto上
 */
$$.transdata=function(jfrom,jto)
{
	jto[$$.getAccess(jto)](jfrom[$$.getAccess(jfrom)]());//设置值属性
}

/**
 * 为jdom注册监听指定的监听函数
 * 
 * item仅仅是jdom的一个包装.问题并不大
 * 
 * 当发生了dom复制的时候,应当保证参数也随之而变.因为reg的时候item已经给定了,只能重新reg.而我们希望复制的时候自动reg.那就去deepClone中修改.
 * 注册包括几方面的事情: 1.设置事件e.data中的item和itemthis,这表明函数是与具体的item无关的,它通过e.data来确定执行对象.
 * 2.将函数保存到itemthis.data.clickfunc中,以备将来复制调用.
 * 
 * 如果多余的参数中包含item,itemthis,它们会被预定义参数item,itemthis覆盖.
 * reg函数会为相应的element对象绑定data.cliclfunc,指向它的响应函数
 */
$$.regItem=function(item,key,farr)
{

	var func;
	var args={};
	if( key && (!farr) ) //没有给定farr,则获取默认的farr
	{
		$$.regItem(item,key,$$.defaultHandler[key.toUpperCase()]);
	}
	if(key)
	{	
		//设置额外的参数
		let jitem=item.getJDom().find("."+key).first();
		$$.regJsubs(item,jitem,farr);
	}
}

/**
 * 注册能够响应click事件的元素
 */
$$.regJsubs=function(item,jsubs,farr){
	let args={"item":item};
	let func;
	if(typeof farr === typeof $)//如果是函数,就没有参数
	{
		func=farr;
	}else if( typeof farr === typeof [])//是二元组
	{
		func=farr[0];
		for(let key in farr[1])//复制参数
		{
			args[key]=farr[1][key];
		}
	}	
	jsubs.each(function(){
		let jself=$(this);
		let argthis={};
		for(let key in args)
		{
			argthis[key]=args[key];
		}
		argthis["itemthis"]=jself;
		//先把原来的函数取消掉
		jself.off("click");
		jself.data("clickfunc",func);//将函数复制到jitem的data中
		jself.click(argthis,func);
	});
	
}
/**
 * 获取键类型,只能是已知的键名
 */
$$.getItemClass=function(jdom){
	for(let i in $$.CLASSES)
	{
		if(jdom.is("."+$$.CLASSES[i]))
		{
			return $$.CLASSES[i];
		}
	}
	return undefined;
}


/**
 * 从jsrc到jdst的五个类事件的复制.
 * 主要是设置e.data参数的item,itemthis
 */
$$.clickClone=function(jsrcdom){
	let jdstdom=jsrcdom.clone(true);
	let item=new Itemshow(jdstdom);
	
	for(let key in $$.classes)
	{
		var jitemthis=jdstdom.find("."+$$.classes[key]).first();
		var clickfunc=jsrcdom.find("."+$$.classes[key]).first().data("clickfunc");
		jitemthis.off("click");//取消click.这个复制的item实际上也继承了原来的事件处理函数,参数也是相同的.此处要做的就是修改参数而已.所以先off.避免触发前面的click,而那个click是指向原来的item的.导致一个click产生两个响应.
		
		//jitemthis.data["clickfunc"]=clickfunc;
		//由于都是相同的参数,所以func不必设置了
		jitemthis.click({"item":item,"itemthis":jitemthis},clickfunc);//避免在func中使用this
	}
	
	return jdstdom;
}



//====这一部分定义默认的click行为
/**
 * e.data.change_mapping 要转换的对应关系
 * e.data.filter  过滤器
 * 
 * 
 * 
 * 自动转移access_key属性
 * 不转换那些隐藏的,因为这样的转换压根看不到;  或者,不复制他们的css属性
 */
Itemshow.defaultChange=function(e)
{
	var item=e.data.item;
	
	var filter=e.data.filter;
	var jsubs=item.subitems(filter).not(":hidden");//.filter('[style="display:none"]');//对于是display
	
	jsubs.each(function(){
		var jself=$(this);
		let oriTag=jself.get(0).tagName.toLowerCase();
		let transto=jself.attr($$.TRANSTO); //读取transto属性
		let mychange={};
		if(transto)
		{
			mychange[oriTag]=transto; 
		}
		var jtarget=$$.getChangeTypeOfElement(jself,mychange);
		jself.hide();
		jself.removeAttr($$.ITEMMARK);
		jself.after(jtarget);
		if(transto)
		{
			jtarget.attr($$.TRANSTO,oriTag);//设置这个项
		}
		jtarget.show();
	});
	//定义哪些按键需要隐藏,需要显示
	item.getJDom().find("."+$$.CANCLE).show();
	item.getJDom().find("."+$$.CONFIRM).show();
	item.getJDom().find("."+$$.CHANGE).hide();
	item.getJDom().find("."+$$.DELETE).hide();
	item.getJDom().find("."+$$.CLEAR).show();
	
}
/**
 * cancle函数只接受item,filter
 */
Itemshow.defaultCancle=function(e){
	var item=e.data.item;
	var filter=e.data.filter;
	var jsubs=item.subitems(filter);//因为defaultChange只是转移了access_key,所以对所有的具有access_key属性的,且满足过滤函数的项,找到它们的前一项,转移access_key属性,然后删除
	jsubs.each(function(){
		//previous
		var jself=$(this);
		//设置显示然后转移属性,之后删除
		jself.prev().show().attr($$.ITEMMARK,jself.attr($$.ITEMMARK));
		jself.detach();
	});
	item.getJDom().find("."+$$.CANCLE).hide();
	item.getJDom().find("."+$$.CONFIRM).hide();
	item.getJDom().find("."+$$.CHANGE).show();
	item.getJDom().find("."+$$.DELETE).show();
	item.getJDom().find("."+$$.CLEAR).hide();
	
}
/**
 * 清除输入内容
 */
$$.defaultClear=function(e){
	var item=e.data.item;
	var filter=e.data.filter;
	var jsubs=item.subitems(filter);
	jsubs.each(function(){
		var jself=$(this);
		jself[$$.getAccess(jself)]("");
	});
	
}

/**
 * 删除
 */
 $$.defaultDelete=function(e){
	 var item=e.data.item;
	 item.getJDom().detach();
 }
 /**
  *
  *所有的此类函数都只接受item作为参数
  */
 $$.defaultConfirm=function(e){
	 var item=e.data.item;
	 var jsubs=item.subitems();
	jsubs.each(function(){
		var jself=$(this);
		var jprev=jself.prev();
		jprev.show().attr($$.ITEMMARK,jself.attr($$.ITEMMARK));//设置属性转移
		$$.transdata(jself,jprev);
		jself.detach();
	});
	item.getJDom().find("."+$$.CANCLE).hide();
	item.getJDom().find("."+$$.CONFIRM).hide();
	item.getJDom().find("."+$$.CHANGE).show();
	item.getJDom().find("."+$$.DELETE).show();
	item.getJDom().find("."+$$.CLEAR).hide();
 }
 
 //================
 /**
 * 预定义class 按钮/其他/接受onclick方法的对象
 *   change,delete
 *   confirm , cancle , clear
 * 默认具有自己的行为
 *   
 */
$$.defaultHandler={
	"CHANGE":$$.defaultChange,
	"CANCLE":$$.defaultCancle,
	"CLEAR" :$$.defaultClear,
	"DELETE":$$.defaultDelete,
	"CONFIRM":$$.defaultConfirm,
}
//=======================
//静态注册函数
$$.registerItemshow=function(jdoms){
	jdoms.each(function(){
		for(let key in $$.defaultHandler)
		{
			$$.regItem(new Itemshow($(this)),key.toLowerCase(),$$.defaultHandler[key]);
		}
	});
}
/**
 * 可以在任意时候再调用这些函数来设置默认行为
 * 一般是在所有预定义函数定义玩之后,所有工作开始之前再调用一次
 */
$$.register=function(){
	$$.registerItemshow($$.findIdAsJDom());
	console.log("register itemshow done");
}
$$.regIds=function(idarr,key,farr){
	if(typeof idarr!==typeof [])//是基本类型
	{
		idarr=[idarr];
	}
	for(let i in idarr)
	{
		let id=idarr[i];
		$$.findId(id).reg(key,farr);
	}
}
/**
 * 插件:itemshow_same
 */
$$.registerItemshowSame=function(){
	$(".itemshow").find(".itemshow_same").find(".itemshow_same_add").click(function(){
		$(this).parent(".itemshow_same").find('.itemshow_same_firstcolumn').
			clone().removeClass('itemshow_same_firstcolumn').
			find("[access_key]").val("").html("").end().
			insertBefore($(this));
	}).end().
	find(".itemshow_same_remove").click(function(){
		$(this).prev().prev().not('.itemshow_same_firstcolumn').remove();
	});
}
$$.dictCopy=function(dict){
	let newdict={};
	for(let key in dict)
		newdict[key]=dict[key]
	return newdict;
}
/**
 * registerAction 为singleAction,multiAction作准备
 * 
 * func是发生时调用的函数
 * chainflag : replace or enqueue
 */
$$.registerAction=function(filter,args,func)
{
	let jbase=$(".itemshow").filter(filter);
	let myarg=$$.dictCopy(args);

	if(!("dataProc" in myarg))
	{
		myarg["dataProc"]=defaultDataProc;
	}
	if( (!func) || (typeof func!==typeof $))//如果func不是是函数
	{
		func=ItemshowAdd.defaultConfirm;
	}
	jbase.each(function(){
		let jself=$(this);
		$$.regJsubs(
			new Itemshow(jself),
			jself.find(".itemshow_post"),
			[func,myarg]
			);
	});
}
/**
 * 内含一个action,其他为access_key的类型注册.这种类型很好
 * class="itemshow_singleaction"
 * 使用itemshow_post来定义这个按钮
 * 
 * 在itemshow顶部指定这个action
 * itemshow_post 现在具有data.clickfunc(e),e具有参数args
 */
$$.registerSingleAction=function(args,func){
	let defaultDataProc=function(data,e)
	{
		let action=e.data.item.getJDom().attr("action");
		sendata={"action":action,"data":data};
		//alert(JSON.stringify(sendata));
		return sendata;
	}
	$$.registerAction(
		".itemshow_singleaction",
		{"dataProc":defaultDataProc},
		ItemshowAdd.defaultConfirm
		);
}

/**
 * 是一个多action的itemshow
 * class="itemshow_multiacion
 */
 $$.registerMultiAction=function(){
	 //主要问题在于如何获取action,action设置成对应的button的action值即可
	 let defaultDataProc=function(data,e)
	{
		let action=e.data.itemthis.attr("action");
		sendata={"action":action,"data":data};
		//alert(JSON.stringify(sendata));
		return sendata;
	}
	$$.registerAction(
		".itemshow_multiaction",
		{"dataProc":defaultDataProc},
		ItemshowAdd.defaultConfirm
	);
 }
$(document).ready(function(){
	$$.register();
	$$.registerItemshowSame();
	$$.registerSingleAction();
	$$.registerMultiAction();
});
//========================
}(Itemshow));
