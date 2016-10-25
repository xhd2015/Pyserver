/**
 * 依赖
 * 	Dynamiccolumn_support($D.a,$D.r)
 * 基本的列
 * 
 * 要求的属性:
 * 	single-item
 * 
 * 其思想是首先判断
 * 
 * $V.feed()
 *  <ANY jparent>
 *  	<firstcolumn/>
 *  	<button add/>
 *  	<button remove/>
 *  </ANY>
 *
 */
Vargroup_support={};

(function($$){
	/**
	 * 对于一个数组型的data[key],总是期望有一个group与之对应.
	 * 
	 * tested: isarr
	 * 			not arr
	 */
	$$.feed=function(jform,data)
	{
		let visited={};
		/*
		 *先调整数据,然后再设置
		 */
		for(let key in data)
		{
			if(typeof data[key]===typeof [] && !visited[key])
			{
				/*
				 *设置key的访问特性,防止大量重复
				 */
				let jfirst=jform.find("[name="+key+"]").parent("[firstcolumn]");
				jfirst.find("[name]").each(function(){
					let jself=$(this);
					let thiskey=jself.attr("name");
					visited[thiskey]=true;
				});
				
				$$.fix(jfirst.parent(),data[key].length);
			}
		}
		Hdata_support.data(jform,data);
		
	}
	
	//传入数目,
	/**
	 * 结果至少保持一项
	 * 
	 * tested: same
	 * 			more
	 * 			less
	 * 	
	 */
	$$.fix=function(jgroup,num)
	{
		let curNum=0;
		let jfirst=jgroup.find("[firstcolumn]");
		let jstart=jfirst;
		while(!jstart.is(":button"))//无需复制的项数
		{
			curNum++;
			jstart=jstart.next();
		}
		//alert(curNum);
		//jstart now is jbutton
		let jadd=jstart;
		while(curNum>num)//删除
		{
			curNum--
			if(jadd.prev().is("[firstcolumn]")) //保留第一项
			{
				continue;
			}else{
				jadd.prev().detach();
			}
		}
		//这里curNum<=num
		while(curNum<num)//增加
		{
			Dynamiccolumn_support.addColumn(jadd);
			curNum++;
		}
		
	}
	
}(Vargroup_support));