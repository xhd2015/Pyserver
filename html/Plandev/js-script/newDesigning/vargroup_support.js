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
		if(!data)
			return;
		let visited={};
		//alert(jform.html());
		/*
		 *先调整数据,然后再设置
		 */
		for(let key in data)
		{
			if($.isArray(data[key]) && !visited[key])
			{
				/*
				 *设置key的访问特性,防止大量重复
				 */
				/*
				 * 
				 * 一个form可能具有多个firstcolumn的数组项
				 */
				jform.find("[firstcolumn]").has("[name="+key+"]").each(function(){
					let jfirst=$(this);
					jfirst.find("[name]").each(function(){
						let jself=$(this);
						let thiskey=jself.attr("name");
						visited[thiskey]=true;
					});
					$$.fix(jfirst.parent(),data[key].length);
				});
				
				
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
	 * @ifZero:=function(hide)
	 * 	
	 */
	$$.fix=function(jgroup,num,ifZero)
	{
		if(!ifZero){
			ifZero=function(jcolumn){
				jcolumn.hide();
			}
		}
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
			if(jadd.prev().is("[firstcolumn]")) //保留第一项
			{
				ifZero(jadd.prev());
			}else{
				jadd.prev().detach();
			}
			curNum--;
		}
		//这里curNum<=num
		while(curNum<num)//增加
		{
			Dynamiccolumn_support.addColumn(jadd);
			curNum++;
		}
		//这里curNum==num,正是我们想要的结果
		
	}
	
}(Vargroup_support));