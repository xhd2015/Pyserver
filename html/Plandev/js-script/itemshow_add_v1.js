
/**
 * requir itemshow first
 * 
 */
 
 
 /**
  * 以一个jdom作为ItemshowAdd来构造.
  */
function ItemshowAdd(jdom)
{
	if(ItemshowAdd.isItemshowAdd(jdom))
	{
		this.$dom=jdom;
		//默认的注册函数 , 不要在此处注册
		//this.reg(ItemshowAdd.MAINCLASS,ItemshowAdd.defaultConfirm);
	}else{
		throw "JDom is not ItemshowAdd";
	}
}
(function($$){
$$.URI="targeturi";
$$.ONRESP="onresp";
$$.MAINCLASS="confirm";//只要具有上面两个属性,就能成为
ItemshowAdd.prototype=Itemshow.prototype;//继承

//重写confirm 方法
//targetUri属性,onresp属性
$$.isItemshowAdd=function(jdom)
{
		if(Itemshow.isItemshow(jdom))
		{
			return jdom.find("["+$$.URI+"]"+"["+$$.ONRESP+"]").length > 0;
		}
		return false;
}
//还需要能对数据进行一次过滤的函数
/**
 * require args,item,itemthis
 * args requires dataProc-->f
 * onresp的参数(resp,e)
 * 
 * 隐含参数 dataProc,additionData想要附加的数据,如果存在同名键,就会替代
 * dataProc接受data,然后返回处理后的data;第二个可选的参数是e.
 * 
 */
$$.defaultConfirm=function(e)
{
	var item=e.data.item;
	var itemthis=e.data.itemthis;
	var dataProc=e.data.dataProc;
	var additionData=e.data.additionData;
	//alert(e.data.itemthis.data("clickfunc"));
	var data=item.data();
	if(additionData)
	{
		for(let key in additionData)
			data[key]=additionData[key];
	}
//	alert(dataProc);
	if(typeof dataProc === typeof $)//是函数
	{
		data=dataProc(data,e);
	//	alert(dataProc);
		//alert(JSON.stringify(data));
	}
	/**
	 * 所有的回调事件,都只有一个标准参数
	 */
	$.post(itemthis.attr($$.URI),JSON.stringify(data),function(resp){
		var onresp=itemthis.attr($$.ONRESP);
		var func=window[onresp];
		e.data.resp=resp;//写入resp
		if(typeof func===typeof $)//是函数
		{
			window[onresp](e);
		}
	});
}
/**
 * 这种应当设置为工厂函数
 */
$$.findId=function(id){
	var jdoms=$$.findIdAsJDom(id);
	if(jdoms.length >0)
	{
		return new ItemshowAdd(jdoms.first());
	}else{
		return undefined;
	}
}
$$.findIdAsJDom=function(id){
	return Itemshow.findIdAsJDom(id).has("["+$$.URI+"]"+"["+$$.ONRESP+"]");
}
//==============
//静态函数,注册默认函数
$$.registerItemshowAdd=function(jdoms){
	jdoms.each(function(){
		let jself=$(this);
		Itemshow.regItem(new Itemshow(jself),$$.MAINCLASS,ItemshowAdd.defaultConfirm);//默认只为confirm注册
	});
}
$$.register=function(){
	$$.registerItemshowAdd($$.findIdAsJDom());
	console.log("register itemshowadd done");
}

//为所有的ItemshowAdd注册默认函数
$(document).ready(function(){
	$$.register();
});

}(ItemshowAdd));
