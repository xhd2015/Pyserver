
/**
 * to use this function,there must be an area with id='__echo'
 * 
 * */
function echo(s){
	if(!window.fulton)
		window.fulton={}
	if(!window.fulton.echo)
		window.fulton.echo=$('#__echo');
	if(window.fulton.echo && s)
	{
		window.fulton.echo.val(window.fulton.echo.val()+s.toString()+'\n');
	}
}
