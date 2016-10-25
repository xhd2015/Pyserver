
/**
 * rely:  
 * 	Hdata_support-->{data}
 * 	Utils-->{repr}
 * 
 */
Prompt_support={};

(function($$){


/**
 * 
 * 对具有p键的值进行设置
 * 默认情况下设置id=prompt的类型
 */
$$.setP=function(p,filter){
	p=Utils.repr(p);
	if(!filter)
	{
		filter="#prompt";
	}
	Hdata_support.data($(filter),{"p":p});
}
/**
 * 添加内容
 */
$$.addP=function(p,filter){
	p=Utils.repr(p);
	if(!filter)
	{
		filter="#prompt";
	}
	let prompter=$(filter);
	Hdata_support.data(
		prompter,
		{"p": $H.data(prompter)["p"]+"\n"+p}
	);
}
	
}(Prompt_support));
