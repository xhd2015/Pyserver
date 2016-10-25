

Utils={};

(function($$){
/**
 *获取字符串表示形态
 */
$$.repr=function(s){
	if(typeof s!==typeof "")
	{	
		s=JSON.stringify(s);
	}
	return s;
}

/**
 * 将JSON Array数据转成JSON Dict的形式
 */
$$.toJSONDict=function(data){
	let thisdata={};
	for(let i in data)
	{
		let name=data[i]["name"];
		let value=data[i]["value"];
		if(name in thisdata)
		{
			if(typeof thisdata[name]!== typeof [])
			{
				thisdata[name]=[ thisdata[name] ];
			}
			thisdata[name].push(value);
		}else{
			thisdata[name]=value;
		}
	}
	return thisdata;
}

/**
 * console log
 */
$$.l=function(p){
	p=$$.repr(p);
	console.log(p);
}

/**
 * expose some Object
 */
$$.exports=function(){
	 $A=Ajaxform_support;
	 $H=Hdata_support;
	 $P=Prompt_support;
	 $T=Transfer_support;
	 $U=Utils;
	 $D=Dynamiccolumn_support;
	 $V=Vargroup_support;
}
/**
 *撤销exports的变量 
 */
$$.poll=function(){
	
}
}(Utils));
