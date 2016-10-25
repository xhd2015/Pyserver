/**
 * 
 * rely:
 * 		Hdata_support{data}
 * 
 * attributes:
 * 		firstcolumn
 * 
 * schema:
 * 		<ANY>
 * 			<col1 name>
 * 			<add click=
 * 			<remove click=
 * 		</ANY>
 * 针对简化代码编程而不是针对0代码编程
 */
/*Demo -- Copy
 
 <div>
			<span firstcolumn>
				&nbsp;&nbsp;
				<lable for="subplan">Part</lable>
				<textarea name="subplan"></textarea> <br/>
			</span>
			<button onclick="$D.a(this);">+</button>
			<button onclick="$D.r(this);">-</button>
</div>
 
 
 */
Dynamiccolumn_support={};

(function($$){

$$.addColumn=function(btn,dataOption){
	let jself=$(btn);
	let jcloned=jself.parent().find("[firstcolumn]").clone(true).removeAttr("firstcolumn");
	if(dataOption)
	{
		Hdata_support.data(jcloned,dataOption);
	}else{
		Hdata_support.reset(jcloned);
	}
	
	jcloned.insertBefore(jself);
	return jcloned;
}
$$.removeCloumn=function(btn){
	let jself=$(btn);
	jself.prev().prev().not("[firstcolumn]").detach();
}

//alias
$$.a=$$.addColumn;
$$.r=$$.removeCloumn;
	
}(Dynamiccolumn_support));
