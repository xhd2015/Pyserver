//=====Example Utils START====
/**
 * getDefault(x,p,d) -- x[p]?x[p]:d
 * quotePreDate(data) -- make data quoted
 * String.format(s,...) -- format str
*/
//=====Example Utils END  ====
//=====Util Functions START======
function getDefault(x,p,d)
{
	if(p in x)
	{
		return x[p];
	}else{
		return d;
	}
}
function quotePreData(data)
{
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
}
//format
String.format = function() {
	if( arguments.length == 0 )
		return null;

	var str = arguments[0];
	for(var i=1;i<arguments.length;i++) {
		var re = new RegExp('\\{' + (i-1) + '\\}','gm');
		str = str.replace(re, arguments[i]);
	}
	return str;
} 
//=====Util Functions END  ======
