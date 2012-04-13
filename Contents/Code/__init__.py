CH_ROOT = "http://www.collegehumor.com"
CH_PLUGIN_PREFIX = "/video/college_humor"
CH_RECENT = "/videos"
CH_VIEWED = "/videos/most-viewed"

CH_VIDEO_PLAYLIST = '/videos/playlists'
CH_WEB_CELEB = '/web-celeb-hall-of-fame'
CH_SKETCH = '/sketch-comedy'
CH_PLAYLIST        = "/moogaloop"

####################################################################################################

def Start():
	Plugin.AddPrefixHandler(CH_PLUGIN_PREFIX, MainMenu, "College Humor", "icon-default.png", "art-default.jpg")
	ObjectContainer.title1 = L('College Humor')
	ObjectContainer.art = R('art-default.jpg')
	DirectoryObject.thumb = R('icon-default.png')
	HTTP.CacheTime = CACHE_1HOUR
	
####################################################################################################

def MainMenu():
	oc = ObjectContainer()
	oc.http_cookies = HTTP.CookiesForURL(CH_ROOT)
	oc.add(DirectoryObject(key=Callback(OriginalsMenu), title="CH Originals"))
	oc.add(DirectoryObject(key=Callback(ShowMenu, url=CH_ROOT+CH_RECENT, title="Recently Added"), title="Recently Added"))
	oc.add(DirectoryObject(key=Callback(ShowMenu, url=CH_ROOT+CH_VIEWED, title="Most Viewed"), title="Most Viewed"))
	oc.add(DirectoryObject(key=Callback(VideoPlaylistsMenu, url=CH_ROOT+CH_VIDEO_PLAYLIST), title="Video Playlists"))
	oc.add(DirectoryObject(key=Callback(SketchMenu, url=CH_ROOT+CH_SKETCH), title="Sketch Comedy"))
	return oc

####################################################################################################
			
def OriginalsMenu():
	oc = ObjectContainer(title2="CH Originals")
	
	for show in HTML.ElementFromURL(CH_ROOT + '/videos').xpath('//div[@class="sidebar_nav"]/ul[2]/li/a')[:-1]:
		url = CH_ROOT + show.get('href')
		title = show.text
		oc.add(DirectoryObject(key=Callback(ShowMenu, url=url, title=title), title=title))
	return oc

####################################################################################################
	
def VideoPlaylistsMenu(url):
	oc = ObjectContainer(title2="Video Playlists")
	for item in HTML.ElementFromURL(url).xpath("//div[@class='media video playlist horizontal']"):
		title = item.xpath('./a')[0].get('title')
		summary = item.xpath('./div/p')[0].text
		thumbURL = item.xpath("a/img")[0].get('src')
		videoURL = CH_ROOT + CH_VIDEO_PLAYLIST + item.xpath('a')[0].get('href')
		oc.add(DirectoryObject(key=Callback(ShowMenu, url=videoURL, title=title), title=title, summary=summary,
			thumb=Resource.ContentsOfURLWithFallback(url=thumbURL, fallback='icon-default.png')))
	
	next = getNext(url, VideoPlaylistsMenu)
	if next != None: oc.add(next)
	return oc

####################################################################################################
	
def SketchMenu(url):
	oc = ObjectContainer(title2="Sketch Comedy")
	for item in HTML.ElementFromURL(url).xpath("//div[@class='media horizontal sketch_group']"):
		title = item.xpath('./a')[0].get('title')
		videoURL = url + item.xpath('./a')[0].get('href')
		summary = item.xpath('./div[@class="details"]/p')[0].text.strip()
		thumbURL = item.xpath('./a/img')[0].get('src')
		oc.add(DirectoryObject(key=Callback(ShowMenu, url=videoURL, title=title), title=title, summary=summary,
			thumb=Resource.ContentsOfURLWithFallback(url=thumbURL, fallback='icon-default.png')))
	
	next = getNext(url, SketchMenu)
	if next != None: oc.add(next)
	return oc

####################################################################################################

def ShowMenu(url, title=''):  
	oc = ObjectContainer(title2=title)
	for item in HTML.ElementFromURL(url).xpath('//div[@class="media video horizontal  "]'):
		title = item.xpath('./a')[0].get('title')
		itemURL = CH_ROOT+item.xpath('./a')[0].get('href')
		summary = item.xpath('./div[@class="details"]/p')[0].text.strip()
		thumbURL = item.xpath('./a/img')[0].get('src')
		oc.add(VideoClipObject(url=itemURL, title=title, summary=summary, 
			thumb=Resource.ContentsOfURLWithFallback(url=thumbURL, fallback='icon-default.png')))
	
	next = getNext(url, ShowMenu)
	if next != None: oc.add(next)
	return oc

####################################################################################################

def getNext(url, menu):
	next = HTML.ElementFromURL(url).xpath('//a[@class="next"]')
	if len(next) != 0:
		return (DirectoryObject(key=Callback(menu, url=CH_ROOT + next[0].get('href')), title='Next', thumb=R('Next.png')))
	else:
		return None
