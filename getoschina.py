import time
import urllib
#coding=utf-8

#sync html can't be crawlered

#http://my.oschina.net/wzugang/favorites
#http://my.oschina.net/wzugang/favorites?type=0&p=1
#http://my.oschina.net/wzugang/favorites?type=0&p=2
#http://my.oschina.net/wzugang/favorites?type=0&p=3
#'http://my.oschina.net/wzugang/favorites?type=0&p='+str(page)

page_count = 1
url = ['']*(20*192)
titles = ['']*(20*192)
page = 1
link = 0
while page <= page_count:
	con = urllib.urlopen('favorites.html').read()
	open(r'test.txt','w+').write(con)
	
	#id = con.find(r'&lt;li <span class="html-attribute-name">id</span>=')
	#mid = con.find(r'</span>',id)
	href = con.find(r'<a class="html-attribute-value html-external-link" target="_blank" href="')
	href_end = con.find(r'"',href)
	#title_prev = con.find(r'>',href_end)
	#title_next = con.find(r'</a>',title_prev)
	i = 0
	#while id != -1 and href != -1 and href_end != -1 and title_prev != -1 and title_next != -1 and i < 20:
	while href != -1 and href_end != -1 and i < 20:
		url[link] = con[href+len('<a class="html-attribute-value html-external-link" target="_blank" href="'):href_end]
		#titles[link] = con[title_prev+1:title_next]
		titles[link] = str(link+1)
		print link+1, ' ', url[link]
		
		#id = con.find(r'<li id=',title_next)
		#mid = con.find(r'</span>',id)
		#href = con.find(r'<a href=',mid)
		#href_end = con.find(r'"',href)
		#title_prev = con.find(r'>',href_end)
		#title_next = con.find(r'</a>',title_prev)	
		
		href = con.find(r'<a class="html-attribute-value html-external-link" target="_blank" href="',href_end)
		href_end = con.find(r'"',href)
		
		i += 1
		link += 1
	else:
		#print id,href,href_end,title_prev,title_next
		print page,'find end'
	page += 1
else:
	print 'all find end'
	j = 0
	while j < link:
		print url[j]
		content = urllib.urlopen(url[j]).read()
		print "read over...."
		open(r'oschina/'+titles[j],'w+').write(content)
		print "write over...."
		print "downloading... ",j+1,' ',url[j]
		j += 1
		#time.sleep(5)
	else:
		print "download article finished !"

		
		
		
		
		
		
		
		
		
		
		