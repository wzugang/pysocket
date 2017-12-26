#!/usr/bin/env python

import time
import urllib
#conding=utf-8
#http://blog.sina.com.cn/s/articlelist_1191258123_0_1.html
#http://blog.sina.com.cn/s/articlelist_1315591982_0_1.html
url = ['']*(50*22)

page = 1
link = 1
while page <= 22:
	con = urllib.urlopen('http://blog.sina.com.cn/s/articlelist_1315591982_0_'+str(page)+'.html').read()
	title = con.find(r'<a title=')
	href = con.find(r'href=',title)
	html = con.find(r'.html',href)
	i = 0
	while title != -1 and href != -1 and html != -1 and i < 50:
		url[link-1] = con[href+6:html+5]
		print link, ' ' ,url[i]
		title = con.find(r'<a title=',html)
		href = con.find(r'href=',title)
		html = con.find(r'.html',href)
		i += 1
		link += 1
	else:
		print page,'find end'
	page += 1
else:
	print 'all find end'
	j = 0
	while j < link-1:
		print url[j]
		content = urllib.urlopen(url[j]).read()
		print "read over...."
		open(r'blog2/'+url[j][-26:],'w+').write(content)
		print "write over...."
		print "downloading... ",j+1,' ',url[j]
		j += 1
		#time.sleep(5)
	else:
		print "download article finished !"
	
	
	
	