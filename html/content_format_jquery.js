/*
 * 这个脚本实现与content-format相关的函数
 * 1.格式化
 * 2.操作
 * */
 
 /**
  * refs
  * 	/index.py
  * 	/search.py
  * */

//引入jquery
function getFormattedContentAsString(content,datetime,id)
{
	return '<pre content_id="'+id+'">'+content+'\n<i>['+datetime+']</i><button onclick="postDeleteData(this);">删除</button>  <button onclick="postModifyData(this);">修改</button></pre>';
}

function postModifyData(which)
{
	var preNode=$(which).parent();
	var preText=preNode.contents().eq(0);
	var mdata=prompt('Make a change',preText.text());
	if(mdata&&mdata!=preText.text())
	{
		$.post('/modify.html',JSON.stringify({id:preNode.attr('content_id') , content:mdata}),
			function(resp,status)
			{
				if( resp==preNode.attr('content_id'))
				{
					preText.replaceWith(mdata+'\n');//textNode uses replace with
				}
			}
		);
	}
}

function postDeleteData(which)
{
	var id=$(which).parent().attr('content_id');
	if(id&&id>=0)
	{
		$.get('/delete.html',{id:id},function(resp){
			if(resp==id)
			{
				$(which).parent().remove();//pre is removed
			}
		});
	}
}
	
	function postUpdateData($content)
	{
		var t=$content.val();
			if(t)
			{
				$.post('/upload.html',t,function(resp){
					var rtn=JSON.parse(resp);
					$(getFormattedContentAsString(t,rtn['date'],rtn['id'])).insertAfter($('#lister').children().first());
					$content.val('');
				});
			}
	}
