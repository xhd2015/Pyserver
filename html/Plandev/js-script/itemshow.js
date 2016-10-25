
/**
 * dataitemshow["x"]["i"]
 * <div class="itemshow" dataindex="x">
 * 	<p class="itemshow_property" access_key="i" access="html"></p>
 *  
 * <button class="itemshow_delete">Delete</button>
 * <button class="itemshow_change">Change</button>
 * <button class="itemshow_cancle">Cancle</button>
 * <button class="itemshow_confirm">Confirm</button>
 * </div>
 *
 */
 

 //默认的change函数将所有的转换成textarea
 //除非有属性itemunchangeable=true
//define class Itemshow
function Itemshow($dom)
{
	if(Itemshow.isItemshow($dom))
	{
		this.$dom=$dom;//$dom和data未必同步
		this.status="show";//show change
		
		//开始注册函数onlick,指定他们的itemonclickf为指定的函数名,能够通过window查询
		this.registerButtonClicks();
	}
	else
	{
		throw "DOM is not '.itemshow'";
	}
}
Itemshow.MAINCLASS="itemshow";
Itemshow.PROPERTYCLASS="itemshow_property";
Itemshow.CHANGECLASS="itemshow_change";
Itemshow.DELETECLASS="itemshow_delete";
Itemshow.CANCLECLASS="itemshow_cancle";
Itemshow.CONFIRMCLASS="itemshow_confirm";

Itemshow.isItemshow=function($dom){
	return $dom.is("."+Itemshow.MAINCLASS);
}
//done
//两个参数-->第一个指定父元素属性,第二个指定子类值
//一个参数-->仅指定子类值
Itemshow.prototype.showData=function(arg1,arg2){
	if(arg2)
	{
		this.setProperty(arg1);
		this.showData(arg2);
	}else if(arg1){
		this.$dom.find(".itemshow_property").each(function(index,self){
			var attr=$(self).attr("access_key");
			if(attr in arg1)
			{
				var method=$(self).attr("access")||"html";
				$(self)[method](arg1[attr]);
			}
		});
	}
}

//$(selector).get(index)-->获取dom
//			.size() -->数量
//			.data(t)  t0:name  t1:name value  t2:obj{name:value} 向一个dom对象添加数据
//			.removeData()
//			.toArray() -->获取数组形式的所有dom
Itemshow.defaultAccessMapping={
	"input":"val",
	"textarea":"val",
	"*":"html",
}
Itemshow.defaultTransferMapping={
	"p":"textarea",
	"pre":"textarea",
	"textarea":"pre",
	"input":"p",
	"*":"textarea"
}
//done return JDOM
Itemshow.getPrompt=function(){
	var $prompt=$(".prompt");
	if(!$prompt.is(".prompt"))
	{
		$prompt=$('<pre class="prompt" access="html">default</pre>');
		$("body").append($prompt);
	}else{
		$prompt=$prompt.first();
	}
	return $prompt;
}
//done
//return JDOM
Itemshow.setPrompt=function(p){
	p=""+p;
	var $prompt=Itemshow.getPrompt();
	var method=$prompt.attr("access")||"html";
	$prompt[method](Itemshow.quoteData(p));
	return $prompt;
}
//done
Itemshow.addPrompt=function(p){
	p=""+p;
	var $prompt=Itemshow.getPrompt();
	var method=$prompt.attr("access")||"html";
	return Itemshow.setPrompt(Itemshow.unquoteData($prompt[method]())+'\n'+p);
}

//done
Itemshow.getAccess=function(arg)
{
	if(typeof arg === typeof $("<br/>")){
		let access=arg.attr("access");
		let tag=arg.get(0).tagName.toLowerCase();
		return access || Itemshow.getAccess(tag);
	}else if(typeof arg === typeof "p")
	{	
		
		return Itemshow.defaultAccessMapping[arg] || Itemshow.defaultAccessMapping["*"];
	}
	else
		return undefined;
}
//done
Itemshow.quoteData=function(data){
	var mapping={
		">":"&gt;",
		"<":"&lt;",
		"&":"&amp;"
	}
	//先替换&,再替换>,<
	//function(matched,p1,p2,..,offset,wholestring),px不是下标,而是真正的字符
	var replacer=function(matched,p1){
		return mapping[matched];
	}
	data=data.replace(new RegExp("(&)","gm"),replacer);
	data=data.replace(new RegExp("(>|<)","gm"),replacer);
	return data;
};
//done
Itemshow.unquoteData=function(data){
	var mapping={
		"&gt;":">",
		"&lt;":"<",
		"&amp;":"&"
	};
	//先替换&,再替换>,<
	//function(matched,p1,p2,..,offset,wholestring),px不是下标,而是真正的字符
	var replacer=function(matched,p1){
		return mapping[matched];
	}
	data=data.replace(new RegExp("(&gt;|&lt;)","gm"),replacer);
	data=data.replace(new RegExp("(&amp;)","gm"),replacer);
	
	return data;
};

//done
Itemshow.createDefaultItemshow=function(access_keys){
	  var html='<div class="itemshow">\n'
	  for(var i=0;i<access_keys.length;i++)
	  {
		  html+='<p class="itemshow_property" access_key="'+access_keys[i]+'"></p>\n';
		}
	html+='<button class="itemshow_delete">Delete</button>\
	   <button class="itemshow_change">Change</button>\
	   <button class="itemshow_cancle" style="display:none">Cancle</button>\
	   <button class="itemshow_confirm"  style="display:none">Confirm</button>\
	</div>\
'
	  return new Itemshow($(html));
};
Itemshow.prototype.toString=function(){
	return this.$dom.html();
}
//done
Itemshow.prototype.getJDom=function(){
	return this.$dom;
};
//done
Itemshow.prototype.insertAfter=function(item){
	item.getJDom().after(this.$dom);
	return this.$dom;
};
//done
Itemshow.prototype.appendTo=function($holder){
	$holder.append(this.$dom);
	return this.$dom;
};
//done
//将一个dom项复制出它的接受输入的项,access属性如果有进行修改
Itemshow.getChangeTypeOfElement=function($dom,additionMappings){
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
	var oriTag=$dom.get(0).tagName.toLowerCase();
	var dstTag=additionMappings["*"];
	if(oriTag in additionMappings)
	{
		dstTag=additionMappings[oriTag];
	}
	var targetHTML="<"+dstTag+">"+$dom.html()+"</"+dstTag+">";
	var $tdom=$(targetHTML);
	var attrs=$dom.get(0).attributes;
	for(var i=0;i<attrs.length;i++)
	{
		var attrname=attrs[i]["nodeName"];
		var attrval=attrs[i]["value"];
		if(attrname == "access")
		{
			if(dstTag in Itemshow.defaultAccessMapping)
			{
				attrval=Itemshow.defaultAccessMapping[dstTag];
			}else{
				attrval=Itemshow.defaultAccessMapping["*"];
			}
		}
		$tdom.attr(attrname,attrval);//属性复制
	}
	
	return $tdom;
	
}
//done
//那些按钮的操作都设置一个参数item,表示其自身
//由于元素名不可改变,将标签复制后,隐藏原来的
//如果想避免这种转换,使用unchangeable选项
Itemshow.defaultChange=function(item)
{
	//除非属性具有不可写属性,unchangeable
	item.status="change";
	item.getJDom().find("."+Itemshow.PROPERTYCLASS).not("[unchangeable]").each(function(index,self){
		var jself=$(self);
		);
		jself.hide();
		jself.after(jtarget);
		jtarget.addClass("tempItemInchange");
		jtarget.show();
	});
	//定义哪些按键需要隐藏,需要显示
	item.getJDom().find("."+Itemshow.CANCLECLASS).show();
	item.getJDom().find("."+Itemshow.CONFIRMCLASS).show();
	item.getJDom().find("."+Itemshow.CHANGECLASS).hide();
	item.getJDom().find("."+Itemshow.DELETECLASS).hide();
	
};
Itemshow.defaultDelete=function(item){
	item.$dom.remove();//向某个地址发出请求,默认发送 targetUri data={operation:delete}
};
Itemshow.defaultCancle=function(item){
	//默认将处于change状态的item
	item.status="show";
	//查找那些处于输入状态的
	item.getJDom().find(".tempItemInchange").each(function(index,self){
		//previous
		var jself=$(self);
		jself.prev().show();
		jself.remove();
	});
	item.getJDom().find("."+Itemshow.CANCLECLASS).hide();
	item.getJDom().find("."+Itemshow.CONFIRMCLASS).hide();
	item.getJDom().find("."+Itemshow.CHANGECLASS).show();
	item.getJDom().find("."+Itemshow.DELETECLASS).show();
	
};
Itemshow.defaultConfirm=function(item){
	item.status="show";
	
}

//return JDOM
Itemshow.getParent=function($dom){
	return $dom.parent("."+Itemshow.MAINCLASS);
};

//done
Itemshow.prototype.setProperty=function(props)
{
	for(var i in props)
	{
		if(i=="class")
		{
			this.$dom.addClass(props[i]);
		}else{
			this.$dom.attr(i,props[i]);
		}
	}
};
Itemshow.prototype.collectData=function(){
		var data={};//对于"",认为是空键
		this.$dom.find(".itemshow_property").filter("[access_key]").each(function(index,self){
			var $self=$(self);
			var method=$self.attr("access")||"html";
			var key=$self.attr("access_key");
			
			//get val
			var value=$self[method]();
			if(value)
				data[key]=$self[method]();
		});
		
		return data;
};


Itemshow.prototype.registerButtonClicks=function(){
		var fkeyName="itemonclickf";
		var thisitem=this;
		var onclickfs={
			"itemshow_delete":Itemshow["defaultDelete"],
			"itemshow_cancle":Itemshow["defaultCancle"],
			"itemshow_confirm":Itemshow["defaultConfirm"],
			"itemshow_change":Itemshow["defaultChange"]
		}
		for(var i in onclickfs)
		{
			var jx;
			jx=this.$dom.find("."+i);
			var jxattr=jx.attr(fkeyName);
			if(window[jxattr])
			{
				onclickfs[i]=window[jxattr];
			}
			//i的值会永久停留,内部不能这样使用
			//这是因为它生成了一个模式函数而非数个函数
			
			jx.click(function(){
				for(var ikey in onclickfs)
				{
					if($(this).hasClass(ikey))
					{
						onclickfs[ikey](thisitem);//标准的监听函数是f(item);
						return;
					}
				}
				
			});
		}
};
