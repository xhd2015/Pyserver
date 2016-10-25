/*
 * 这个脚本实现与content-format相关的函数
 * 1.格式化
 * 2.操作
 * */

function getFormattedContentAsElement(content,datetime,id)
	{
		var pre=document.createElement('pre');
		var i=document.createElement('i');
		var btnDel=document.createElement('button');
		var btnMod=document.createElement('button');

		pre.setAttribute('content_id',id)
		i.appendChild(document.createTextNode('['+datetime+']'));
		btnDel.setAttribute('onclick','postDeleteData(this);');
		btnDel.appendChild(document.createTextNode('删除'));
		btnMod.setAttribute('onclick','postModifyData(this);');
		btnMod.appendChild(document.createTextNode('修改'));

		pre.appendChild(document.createTextNode(content+'\n'));
		pre.appendChild(i);
		pre.appendChild(btnDel);
		pre.appendChild(document.createTextNode('  '));
		pre.appendChild(btnMod);

		return pre; //实际上没有什么不同
	}
function getFormattedContentAsString(content,datetime,id)
{
	return '<pre content_id="'+id+'">'+content+'\n<i>['+datetime+']</i><button onclick="postDeleteData(this);">删除</button>  <button onclick="postModifyData(this);">修改</button></pre>';
}

	function postModifyData(which)
	{
		var preNode=which.parentNode;
		var preText=preNode.firstChild.textContent;
		var mdata=prompt('Make a change',preText);
		if(mdata&&mdata!=preText)
		{
			var xhr=new XMLHttpRequest();
			xhr.open('POST','/modify.html',true);//使用异步
			xhr.onreadystatechange=function(){
				if(xhr.readyState==4 && xhr.status==200)
				{
					if(xhr.responseText==preNode.getAttribute('content_id'))//如果返回的id是同一个
					{
						preNode.firstChild.textContent=mdata+'\n';
					}
				}
			};
			xhr.send(JSON.stringify(
			{id:preNode.getAttribute('content_id') , content:mdata}
			));
		}

}
	function postDeleteData(which)
	{
		var id=which.parentNode.getAttribute('content_id');
		if(id&&id>=0)
		{
			var xhr=new XMLHttpRequest();
			xhr.open('GET','/delete.html?id='+id,true);//使用异步
			xhr.onreadystatechange=function(){
				if(xhr.readyState==4 && xhr.status==200)
				{
				if(xhr.responseText==id)//如果返回的id是同一个
					{
					pNode=which.parentNode;//pre
					ppNode=pNode.parentNode;//lister
					if(pNode && ppNode)
					{
						ppNode.removeChild(pNode);
					}
				}
				}
			};
			xhr.send();
		}
	}
