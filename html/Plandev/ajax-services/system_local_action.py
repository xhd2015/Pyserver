
import fulton_utils.action.action as gaction
import fulton_utils.lib_system.util_fulton as uf

class Handler(gaction.Handler):
	def __init__(self,s):
		super().__init__(s)
	def actionSystem(self):
		data=self.data['data']
		cmd=data['cmd']
		out=uf.mysystem(cmd)
		self.setRtndata(status="success",reason="cmd out is sent.",data=out)
		
	def prepare(self):
		pass
		
		
def generate_html(s):
	return Handler(s).setDebug(True).serve().finishServe();
