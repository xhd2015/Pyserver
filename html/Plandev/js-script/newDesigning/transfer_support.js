/**
 * rely
 * 	Hdata_support{data,getAccess}
 * 	Vargroup_support(feed)
 * 
 * 这个类只定义行为,不定义ajax操作.ajax操作由form的submit定义.reset已经有了.
 * 所有的ajax操作只由type=submit完成
 * 
 * 设计方式:
 * 只对form进行相应的转换
 * 	由attr=example_show,example_change确定转换关系.
 * 		change--->1隐藏,创造2,并显示
 * 		cancle ----> 1显示,2detach
 * 		confirm--->1设置2的数据, 2 detach
 * 		delete--->1 detach
 * 所有的example被隐藏
 * 	复制的的example_show具有属性 item_show
 * 			复制的example_change具有属性 item_change
 * 
 * 
 * 由于type值单一
 * 
 * type=reset
 * type=toshow
 * type=tochange
 * 
 * 
 * transfer转换只对:visible,not :disabled
 */
Transfer_support={};

(function($$){
/**
 * 在同级的前面查找example_change.
 * 	$(this).prev("[example_change]").first().clone()
 * 
 * 重新注册新的submit事件
 */
$$.getChangeType=function(jdom){
	jcopied=jdom.prev("[example_change]").first().clone().removeAttr("example_change").attr("item_change","");
	$A.registerAjaxForm(jcopied);
	return jcopied;
}
/**
 *获取一个显示项 
 */
$$.getNewshow=function(jholder,data){
	if(typeof jholder===typeof "")
	{
		jholder=$(jholder);
	}
	jcopied=jholder.find("form[example_show]").first().clone().removeAttr("example_show").attr("item_show","").show();
	$A.registerAjaxForm(jcopied);
	$H.data(jcopied,data);
	return jcopied;
}
/**
 * 获取显示类型,其类型已经在前一个蔡遵
 */
$$.getShowType=function(jdom){
	return jdom.prev();
}
/**
 * 将数据转移,然后显示
 */
$$.change=function(jdom_show){
	let data=$H.data(jdom_show);
	let jdom_change=$$.getChangeType(jdom_show);
	$V.feed(jdom_change,data);
	jdom_show.after(jdom_change.show()).hide();
}
/**
 */
$$.cancle=function(jdom_change){
	$$.getShowType(jdom_change).show();
	jdom_change.detach();
}
/**
 * 这个confirm会以feed的形式进行
 */
$$.confirm=function(jdom_change){
	let data=$H.data(jdom_change);
	let jdom_show=$T.getShowType(jdom_change);
	
	$V.feed(jdom_show,data);//设置数据项,相当于先改变上下文
	
	$$.cancle(jdom_change);//设置完上下文以后,取消显示
}

$$.delete=function(jdom_show){
	jdom_show.detach();
}

$$.add=function(){
	
	
}


}(Transfer_support));
