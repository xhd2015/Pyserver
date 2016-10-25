#-*-coding:utf8;-*-
#qpy:3
#qpy:console
import socket as s
import sys
sys.path.append('/storage/emulated/0/com.hipipal.qpyplus/scripts3')

def makeSocket():
    return s.socket(s.AF_INET,s.SOCK_STREAM)
def makeServer(addr='127.0.0.1',port=5533):
    svr=makeSocket()
    svr.bind((addr,port))
    svr.listen(1)
    return svr
'''u'''
def socketRecv(skt,SZ=1024):
    '''note:this method goes wrong if data to 
read is 1024*n bytes,n denotes an integer,
however,for most cases,you can set the arg SZ
into 1023,or 1025 etc,to fix this issue'''
    data=bytearray()
    buf=memoryview(bytearray(b'0'*SZ))
    rdn=skt.recv_into(buf,SZ)
    data.extend(buf[:rdn].tobytes())
    while rdn==SZ:
        rdn=skt.recv_into(buf,SZ)
        data.extend(buf[:rdn].tobytes())
    return data
    
def getRqSrc_depreciated(head):
    i=head.find(' ')
    j=head.find(' ',i+1)
    return head[i+1:j]
    
def getPostData(s):#s be type of http
#.server.BaseHTTPRequestHandler
    length=s.headers.get('content-length')
    if not length:
        length=0
    return s.rfile.read(int(length))
def parseArgData(data):
    '''data is a http quoted data like 'a=x%AE%FF&b=y&c='  '''
    import re
    rgx=re.compile(r'(\w+)=([^&]*)')
    m=re.findall(rgx,data)
    return dict(m)
    
def httpHeadParser_bug(head):
    #use named tuple
    import collections as c
    headc=c.namedtuple('headc',('method',
    	'rqsrc','version','getdata'))
   
    i,j=0,0
    i=head.find(' ')
    method=head[:i]
    
    
    if method.lower()=='get':
        j=head.find('?',i+1)
        rqsrc=head[i+1:j]
        i=head.find(' ',j+1)
        getdata=head[j+1:i]
        i,j=j,i
    else:
        j=head.find(' ',i+1)
        rqsrc=head[i+1:j]
        getdata=None
    	
    i=head.find('\r\n',j+1)
    version=head[j+1:i]
    
    rtparsed=headc(method,rqsrc,version,None if not getdata else getdata)
    return rtparsed
    	
def serverAccept(svrSkt):
    return (svrSkt.accept())[0]
'''test'''
if __name__=='__could_run__':
    x=httpHeadParser('GET /J.HT HTTP/1.1\r\n\r\n')
    print(x)
    with makeServer() as svr:
        with serverAccept(svr) as clt:
            data=socketRecv(clt)
            print(data)
