#!/bin/python3
import os
import pprint
def listdir_R(s,f):
	if os.path.isdir(s.html_dir+'/'+f):
		res=f+'\n'
		for i in os.listdir(s.html_dir+'/'+f):
			res+=listdir_R(s,f+'/'+i)
	else:
		res='<a href="'+f+'">'+f+'</a>'+'\n'
	return res

def generate_html(s):
	localdir=listdir_R(s,'')
	head=''
	script=r'''</script>
	<script src='/jquery-3.1.0.min.js'></script>
	<script>
		$(document).ready(function(e){
			//对不含#的连接使用所有的连接使用blank属性
			$("a").attr("target","_blank");
			//设置显示或者隐藏
			$('footer').attr('isShown','true');
			$('#footer_toggle').click(function(e){
				if($('footer').attr('isShown')=='true'){
					$('#footer_main').fadeOut('slow');
					$('footer').attr('isShown','false');
				}else{
					$('#footer_main').fadeIn('slow');
					$('footer').attr('isShown','true')
				}
				
			});
		});
	'''
	title='Debug Info'
	style=r'''
	body{
		background-color: transparent;
	}
	fulton{
		font-weight:bold;
		font-variant:small-caps;
		font-style:italic;
		font-size:2em;
	}
	footer{
		position:fixed;
		bottom:0;
		width: 100%;
		background-color:rgb(2,60,90);
	}
	'''
	body=r'''
	<nav style="border:1px solid;background-color: lightblue;">
		<h1 style='text-align:center;;'>Debug Info for <fulton>Fulton</fulton></h1>
		<ul>
			<li><a  href='#preview'>概览信息</a></li>
			<li>配置参数</li>
			<li>meta常量<sup>示例</sup></li>
			<li>headers常量<sup>示例</sup></li>
			<li>本地目录html</li>
			<li>Internet概念解释</li>
			<li>Shell 内置命令</li>
		</ul>
	</nav>
<article id='container' style="background-color:white;">
	<h4 id='preview'>概览信息<a href='#preview' class='inner_goto'></a></h4>
	<pre>'''+s.helpinfo+r'''</pre>
	
	<h4 id='setups'>配置参数</h4>'''
	setups=''
	for k in s.setups:
		setups+=k+'='+s.setups[k]+'\n'
	body+=r'''<pre>'''+setups+r'''</pre>
	<h4 id='argv'>命令行参数</h4>
	<pre>'''+str(s.argv)+r'''</pre>
	<h4 id="object_s">编程参数</h4>
	<pre>'''+pprint.pformat(dir(s))+r'''</pre>
	<h4 id='metas'>meta常量<sup>示例</sup></h4>
	<pre>'''+str(s.examples['metas'])+r'''</pre>
	<h4 id='headers'>headers常量<sup>示例</sup></h4>
	<pre>'''+str(s.examples['headers'])+r'''</pre>
	<h4 id='htmldir-content'>本地目录html</h4>
	<pre>'''+localdir+r'''</pre>
	<h4 id='inet-helper'>Internet概念解释</h4>
	<p>A generic URI is of the form:<br />
	&nbsp;&nbsp;&nbsp;&nbsp;scheme:[//[user:password@]host[:port]][/]path[?query][#fragment]
	</p>
	<h4 id='shell'>Shell 内置命令</h4>
	<p>
		<ul>
			<li>declare ： 设置变量，函数</li>
			<li>set : 设定shell的行为</li>
			<li>hash : 为执行文件指定快捷名称</li>
			<li>enable : 启用或禁用shell内置命令</li>
			<li>exec : 使用新的进程替换原来的进程 </li>
			<li>kill : 发送信号给进程</li>
		</ul>
	</p>
	<h4 id='linux-shell'>Linux 命令</h4>
	<ul>
		<li>dd:将输入文件输出到文件 dd if= of= count=读取总数	bs=一次处理的块大小	ibs=一次读取大小	obs=一次写入大小(默认512)	seek=skip output N*obs	skip=skip input N*ibs<br/>
		备份MBR:dd if=/dev/hdx of=/path/to/image count=1 bs=512<br />
		写入MBR:dd if=/path/to/image of=/dev/hdx<br/>
		MBR结构:代码:440(max up to 446)	选用软盘标志:4	空值:2	MBR分区表:64(4个16字节主分区)	MBR有效标志:2(值是0x55AA)
		</li>
		<li>service : 服务启动、停止或者重新启动；<br />
		示例：service httpd status；<br />
		相关命令：serviceconf(图形界面)；<br />
		介绍：所有的服务脚本在/etc/init.d下面 , service httpd x1 x2命令将会传递x1,x2参数给httpd , 大多数服务的x1参数为start , restart ,stop等。status命令-->[- 停止 +运行?不支持status命令]. /etc/init.d为System V的初始化脚本，/etc/init为新启用的脚本（非系统脚本） <br/>
		禁用服务 : 通过对/etc/init中相应的文件名称的改变，可以禁用某些服务.譬如sudo mv /etc/init/cups-browsed.conf /etc/init/cups-browsed.conf.disabled<br />
		由于/etc/rcX.d表示的是在运行级别X下相应的启动文件(S)，也就是服务，而这些服务实际上都是/etc/init.d的链接，所以如果将这些连接删除，就可以避免启动此类服务ls /etc/rc?.d/*cups*|
		</li>
		<li>wget : 从指定位置下载文件；和浏览器的区别在于，它不会分析文件内容，然后下载依赖文件</li>
		<li>elinks/lynx : 文本浏览器</li>
		<li>w : 显示当前登录的用户</li>
		<li>who : 当前登录系统的用户信息</li>
		<li>users : 显示所有在线用户</li>
		<li>finger : 查询用户信息，与cat /etc/passwd差不多</li>
		<li>chfn : 改变用户信息</li>
		<li>chsh : 改变默认登录shell</li>
		<li>passwd : 改变用户密码</li>
		<li>useradd/userdel : 添加/删除用户，这两个指令只能以root运行，需要修改/etc/passwd文件</li>
		<li>login : 登录一个域上的系统</li>
		<li>init /telinit: 改变系统级别；0.关机 1 .单用户root，用于维护系统 2.无nfs服务的3模式   3.完全多用户网络模式，服务器默认模式  4.未使用  5.图形界面模式  6.重启系统</li>
		<li>uname : 显示系统信息</li>
		<li>host  :  查询dns</li>
		<li>mount : mount /dev/sda1 /media/x/C 挂载硬盘</li>
		<li>umount : 卸载挂载的硬盘</li>
		<li>sync : 将所有缓存的数据存入磁盘</li>
		<li>pstree : 显示进程树</li>
		<li>uptime : --pretty 显示系统运行时间</li>
		<li>lsmod / modinfo :  显示模块信息</li>
		<li>insmode / modprobe : 加载模块</li>
		<li>rmmod: 删除模块</li>
		<li>sysctl  : 控制系统内核参数；系统参数保存在/etc/sysctl.conf中。一个示例：关闭ip路由----&gt;sysctl net.ipv4.ip_forward=0</li>
		<li>
		find :-name 指定名字模式，支持通配符；find符合标准的参数解析（除了用长参数替代短参数），其目标是目录。<br />
		-type 指定文件类型f <br />
		-exec 对查找到的文件执行命令，最后一个参数必须以';'结束，在命令中使用{}表示文件 ;可以连续使用多个-exec参数<br />
		 </li>
		 <li>arp , arping , arpwatch : 显示本机arp ，邻近主机arp信息或者监听。记住，arp只能用于同一个域，并且域与接口是相关的;arpwatch以服务模式启动，当有变化时记录到syslog中
		 </li>
		 <li>ipcalc : 计算ip地址的广播地址等。</li>
		 <li>ln : 将文件当做数组，inode当做下标，则文件实际上是一个指针，而文件夹则是指针数组，文件指向文件内容的位置。硬链接是创建新的指针（共享内容），软链接创建指针的指针（父子关系）。</li>
		<li>vsftpd : 在linux上开启ftp服务；</li>
		<li>ftp : 获取服务器上的文件</li>
		<li>whois : 查询dns数据库中某个域名的详细信息</li>
		<li>kill/killall : kill对pid操作，killall对进程名称; kill －9 324 强行kill一个程序</li>
		<li>chkconfig : 配置系统服务，适用于redhat系统</li>
		<li>/etc/services文件 : 系统根据程序名称到端口名的映射</li>
		<li>inetd/xinted : inetd是系统服务的自动化。当某个端口收到请求的时候，inetd都会按照services文件启动相应的服务。然而，对于安全而言，最好的方式是不要启用inetd
		</li>
		<li>make和linux下安装源程序.<br/>
			首先make,configure程序都是AUTOMAKE和AUTOCONF程序生成的用于发布c语言源程序的工具<br/>
			1. ./configure --prefix=... 程序用于生成Makefile,以及指定软件的安装地点 <br/>
			2. make编译整个Makefile,以检查系统的库完整性和支持程度<br/>
			3. make install将程序安装到系统<br/>
			4. make clean用于清除程序遗留的文件<br/>
			5. make dist用于生成安装包,包括packagename+version<br/>
			6. make all可能与配置文件相关<br/>
		</li>
		<li>Git 版本控制器 <br/>
<pre>
刚安装好git,就需要配置用户名和用户邮箱,以便在提交中标志提交者.使用git config --gloable user.name/user.email去配置
要从github clone仓库,先添加计算机ssh密文认证,如下ssh-keygen -t rsa -b 4096 -C $EMAIL,然后将~/.ssh/rsa.pub复制到github上,本地使用ssh git@github.com 测试是否成功.
git命令:
		status 查看状态
		commit [-m $COMMENT] : 标记一个新的节点
		add	$FILE : 将文件添加
		clone :git clone {local-rep , username@host:/path/to/repository}
			远程仓库如git@github.com:xhd2015/contest.git , 不过前提是该仓库的RSA计算机指纹能够接受请求计算机
		init :初始化仓库
		config :  --global(指向~/.gitconfig)|--system(指向/etc/gitconfig)|--local(指向$.git/config) user.name/user.email $ARG 用于配置用户信息,可以在
		push $LOCAL_RESP_NAME_FOR_REMOTE $REMOTE_BRANCH :当前分支推送到远程的分支
		checkout [-b] $BRANCH : [创建]切换到相应分支
		branch [-d] $BRANCH :创建或者删除分支
		merge :合并分支
		remote add $LOCAL_RESP_NAME $REMOTE_RESP_URI :
		diff $B1 $B2 : 查看B1 , B2的区别
		pull : 拉取远程仓库 , 相当于fetch & merge
		tag $TAGNAME $COMMIT_CODE_10: 创建一个节点的标签,以节点前10位作为标志
		log : 查看所有的节点

github的rsa/ssh认证指纹:(用于clone,push远程仓库)
	检查现存的rsa指纹 : 在~/.ssh目录下检查是否有*.pub文件
	生成指纹 :ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
	test远程仓库连接 :ssh git@github.com
.gitignore文件
	用于忽略文件,支持通配符
</pre>			
		</li>
		<li>cron
		
		</li>
		<li>pgrep <br/>
		progress grep, 进程正则表达式检索.含有逻辑含义: pgrep -G other,daemon -U root,daemon , 表示组为other或daemon,以及用户为root和daemon. <br/>
		
		</li>
		<li>pkill <br/>
		基于正则表达式的kill <br/>
		</li>
		<li>shutdown <br/>
		关机, 带有时间的条件.语法格式sudo shutdown $OPTION $TIMETOWAIT $MESSAGE,默认情况下时间为1,也可以取值为now, 0, 22:00(hh:mm), +45(+mm);halt意味着宕机, 电源不能真正的响应. 例子: <br/>
		sudo showdown --poweroff +45 "Your PC goes shutting down".
		</li>
		<li>manpages, manpages-de, manpages-de-dev, manpages-dev <br/>
		使用sudo apt-get install manpages-*可以安装man的数据库, 当man -k 失效的时候, 可以使用这个语法.
		</li>
		<li>/etc/init.d/network-manager <br/>
		管理网络服务
		</li>
		<li>ip<br/>
		和ifconfig对等的,是ifconfig的替代品.见<a href="http://www.68idc.cn/help/server/linux/20151006571068.html">ip命令详解</a> <br/>
	</ul>
	<section id='python-info'>
		<h4>Python库帮助</h4>
		<ul>
			<li>
			ftplib : FTP() login()  cwd()  mkd()  pwd()   getwelcome() delete() dir()--->'LIST'  nlst()-->'NLST' <br />
			retrlines('LIST',callback---->f(line)--->default:sys.stdout)-->get ls     <br />
			retrbinary('RETR filename'-->cmd,f.write-->callback)  <br />
			<b>use with</b> with FTP(...) as f: 
			</li>
		</ul>
	</section>
	<section id='database-info'>
		<h4>数据库帮助信息</h4>
		<ul>
			<li>数据库查找  :<b>IN 条件语句 </b> ... WHERE col IN (val1,val2,...) <br />
			<b>LIKE 条件语句 </b>LIKE也是一个条件语句，但是LIKE的用处在于其后面的操作数：支持通配符。{% : 零个或多个, _ : 一个  , [charlist]:字符列表 , [^charlist]:非字符列表 }
			</li>
			<li>AUTO_INCREMENT : 用在create table中，指的是int型数据在创建时自动增1</li>
			<li>PRIMARY KEY col :创建主键,通常在create table中的最后一行指定；然而，PRIMARY KEY也可以用在通常的列中 <br/>
			几种primary key的约束形式:	<br/>
			1.(befores...,PRIMARY KEY (id0)) <br/>
			2.(id int not null PRIMARY KEY,...)   <br/>
			3.多列约束 (befores...,CONSTRAINT key_name PRIMARY KEY (id1,id2)) <br/>
			
			</li>
			<li>FOREIGN KEY :用于连接运算符限制<br/>
			1.(befores...,FOREIGN KEY (Id_P) REFERENCES Persons(Id_P)) <br/>
			2.(Id_P int FOREIGN KEY REFERENCES Persons(Id_P),afters...) <br/>
			3.(befores...,CONSTRAINT fkey_name FOREIGN KEY (Id1,id2) REFERENCES Persons(Id1,id2)) <br/>
			</li>
			<li>UNION : 对多个集合的并运算，返回的结果总是以第一个表为参照 </li>
			<li>ALTER : 修改表信息；对于sqlite3，支持ALTER TABLE tab {RENAME TO new_tab,ADD COLUMN colname column_def},也就是说只能更改表名或者添加列</li>
			<li>子查询 : 子查询使用(selections)作为语法，可以认为子查询构成一个多值集合；因此可以对子查询使用IN等操作符</li>
			<li>子查询插入insert : 其关键是不需要使用values。INSERT INTO tab SELECT x,y FROM tab</li>
			<li>default限定 : create table t(id1 timestamp NOT NULL default CURRENT_TIMESTAMP) , default限定默认取值</li>
			<li>MySql数据类型:3大主类型:Text,Number,Date <br/>
<pre>Text:
	varchar(size)
	char(size)
	tinytext
	text
	blob
Number:
	tinyint(size)---1字节
	int(size)	----4字节
	double(size,d) --size为最大长度,d为小数点位数
Date:
	Date()	 YYYY-MM-DD
	Datetime()	YYYY-MM-DD hh:mm:ss
</pre>
			
			</li>
<pre>
		</ul>
	</section>
	<section id='network-scan'>
		<h4>网络扫描和系统安全</h4>
		<ul>
			<li>ping : ping与计算机端口无关，它用于发现开启的计算机</li>
			<li>telnet : 连接到计算机的某个服务，如telnet localhost echo,连接到echo服务</li>
			<li>fping : 同时发送多个包到目标网络集合</li>
			<li>nmap : 使用nmap提供-sP选项，提供ip地址和掩码长度，即可实现ping. nmap -sP localhost/24 <br/>
					端口扫描 <br />
					操作系统检测 <br />
			</li>
			<li>traceroute : 发现一个到目标主机最近的路径</li>
			<li>netcat : 主机端口扫描工具;nc是其简称；-w [n]超时，-v详细格式，-z只连接，不发送数据 -u查询udp端口;nc -vzw 4 www.example.com 1-65535</li>
			<li>嗅探器 : 用于截取网路上发送的数据包；hunt ， linux-sniff , </li>
			<li></li>
			<li>lsof  : 获取计算机上运行的服务 , (其中由inid启动的部分)</li>
			<li>netstat : -an 选项通常用于查看计算机的链接信息.使用sudo获得服务的进程号。</li>
			<li>route : 路由表管理.可以使用route add添加</li>
			<li></li>
		</ul>
	</section>
	<section>
		<h4>常用链接</h4>
		<ul>
		<li>
			<a href='/script/socket_info.html'  target="blank">Socket与网络通信</a>
		</li>
		<li>
			<h5>mysql</h5>
			<p>在linux系统上安装MySql需要MySql-Server运行时,使用sudo apt-get install mysql-server安装<br/>
			在java中使用mysql/其他数据库,需要通过加载类而不是import的方式 Class.forName("com.mysql.cj.jdbc.Driver").newInstance();<br/>
			 conn =
       DriverManager.getConnection("jdbc:mysql://localhost/test?" +
                                   "user=minty&password=greatsqldb");<br/>
			</p>
			<a href='http://dev.mysql.com/downloads/connector'  target="blank">mysql connector download</a>&nbsp;&nbsp;&nbsp;
			<a href='http://cs.dvc.edu/HowTo_JavaSQL.html'  target="blank">A JDBC Sample</a>
		</li>
		<li><a href='http://struts.apache.org/download.cgi' target="blank">Struts2 Java Package</a></li>
		<li>
			<a href="https://marketplace.eclipse.org"  target="blank">Eclipse Marketplace Official Site</a>
		</li>
		<li><a href="https://sourceforge.net">SourceForge软件下载</a></li>
		<li><a href="http://gmirror.org/#android-sdk-tools-only">Android SDK for ALL</a></li>
		<li><a href="http://m.sm.cn/s?q=site%3Apan.baidu.com%20struts2&from=smor&safe=1&snum=6">神马网盘搜索搜索</a></li>
		<li><a href="http://mirrors.neusoft.edu.cn">大连东软信息学院--Android SDK Source国内镜像</a></li>
		<li><a href="http://run.hit.edu.cn">哈工大国内镜像</a></li>
		<li><a href="http://mirror.bit.edu.cn">北理工镜像</a></li>
		<li><a href="http://mirror.bjtu.edu.cn">北京交通大学--Linux世界的中国镜像</a></li>
		<li><a href="http://mirrors.ustc.edu.cn">linux世界镜像</a></li>
		<li><a href="http://mirrors.cnnic.cn/apache/">Apache 镜像</a></li>
		<li><a href="http://wear.techbrood.com/index.html">Android 开发网站教程--国内镜像</a></li>
		<li><a href="http://www.linuxidc.com">Linux 公社</a></li>
		<li><a href="http://tools.android-studio.org/index.php/adt-bundle-plugin">ADT 百度网盘下载 <sup>注:adt由google开发,现已停止更新.</sup></a></li>
		<li><a href=http://android.vpn.ac.cn/index.php/get/vpn"> cheap VPN: $5/Month</a></li>
		
		<hr width="50%" style="float:left;"/> <br/> <!--强制换行-->
		<li><a href="http://tv.cctv.com/lm/sjzk/">世界周刊</a></li>
	
		</ul>
	</section>
	<section id="accounts">
		<h4>账号信息</h4>
		<ul>
			<li><a href="https://www.green-jsq.org"  target="blank">GreenVPN</a> <br/>
			账号: __Fulton <br/>
			密码: $common	<br/>
			注册邮箱:1377430541@qq.com <br/>
			</li>
			<li>Google 邮箱<br/>
			账号 : xhd2015@gmail.com <br/>
			密码 : $common	<br/>
			<li><a href="http://www.vpngate.net/cn"  target="blank">公共VPN</a> <br/>
			账号 : vpn	<br/>
			密码 : vpn 	<br/>
			镜像站点 : 	<br/>
			</li>
			<li>百度账号<br/>
			账号 : xhd2015 <br/>
			密码 : $common <br/>
			</li>
			<li>Github账号 <br/>
			账号 : xhd2015 <br/>
			密码 : $common <br/>
			注册邮箱 : Google邮箱 <br/>
			</li>
			<li>新浪账号
			账号: 
			手机账号: 1824503267 <br/>
			密码: $common	<br/>
			
			</li>
		</ul>
	</section>
	<section id='local-host-info'>
		<h4>本地Linux系统信息</h4>
		<ul>
			<li> mysql-connector库 <br/>
			/usr/lib/java/mysql-connector-java-6.0.4 <br/>
			/usr/lib/java/mysql-connector-java-5.1.39 <br/>
			</li>
			<li>Tomcat 服务器<br/>
			/home/x/installed/apache-tomcat-9.0.0.M10 <br/>
			/home/x/installed/apache-tomcat-7.0.70 <br/>
			</li>
			<li>JVM & JDK <br/>
			/usr/lib/jvm/default-java	<br/>
			/usr/lib/jvm/java-8-openjdk-amd64	<br/>
			/usr/lib/jvm/java-1.8.0-openjdk-amd64	<br/>
			#Those are all jres , not jdk , which means they do not contain 'javac' <br />
			JDK1.8.0u73: /usr/lib/jvm/jdk1.8.0_73	<br/>
			</li>
			<li>Struts2 库  <br/>
			/usr/share/struts-2.5.2	<br/>
			</li>
			<li>Eclipse	<br/>
			JavaEE: /usr/share/eclipse-ee	<br/>
			JavaSE:	/usr/share/eclipse	<br/>
			</li>
			<li> Log4j--Apache 开源项目<br/>
			/usr/lib/java/apache-log4j-2.6.2-bin <br/>
			</li>
			
		</ul>
	</section>
</article>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<footer>
	<div style='background-color:white;'><img id='footer_toggle' src='/favicon.ico' style='width:2%;height:1%;margin-left:50%;'></img></div>
	<div id='footer_main'>
	<hr style="width:100%;"/>
	<p style='text-align:center;font-size:medium;'><small>&copy;</small>copyright <fulton>Fulton Shaw</fulton> since 2012</p>
	</div>
</footer>
'''

	html=s.hf.format_html(script=script,head=head,body=body,style=style,title=title)
	return [0,html]
