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
	HTTP.SetCacheTime(CACHE_1HOUR)
	
####################################################################################################

def MainMenu():
	oc = ObjectContainer()
	oc.http_cookies = HTTP.CookiesForURL(CH_ROOT)
    oc.add(DirectoryObject(key=Callback(OriginalsMenu), title="CH Originals"))
    oc.add(DirectoryObject(key=Callback(ShowMenu, url = CH_ROOT + CH_RECENT), title="Recently Added"))
	oc.add(DirectoryObject(key=Callback(ShowMenu, url = CH_ROOT + CH_VIEWED), title="Most Viewed"))
    oc.add(DirectoryObject(key=Callback(ShowMenu, url = CH_ROOT + CH_VIDEO_PLAYLISTS), title="Video Playlists"))
	return oc
    
####################################################################################################
			
def OriginalsMenu():
	oc = ObjectContainer(title2="CH Originals")
	
	for show in HTML.ElementFromURL(CH_ROOT + '/videos').xpath('//div[@class="sidebar_nav"]/ul[2]/li/a')[:-1]:
		url = CH_ROOT + show.get('href')
		title = show.text
        oc.add(DirectoryObject(key=Callback(ShowMenu, url=url), title=title))
	return oc
    
####################################################################################################
	
def VideoPlaylistsMenu(sender, url):
	# FIXME: get FLV url from webpage
	dir = MediaContainer(title2=sender.itemTitle)
	for item in HTML.ElementFromURL(url).xpath("//div[@class='media video playlist horizontal']"):
		title = item.xpath('./a')[0].get('title')
		summary = item.xpath('./div/p')[0].text
		thumb = item.xpath("a/img")[0].get('src')
		videoURL = urljoin(CH_ROOT + CH_VIDEO_PLAYLIST, item.xpath('a')[0].get('href'))
		dir.Append(Function(DirectoryItem(ShowMenu, title=title, thumb=thumb, summary=summary), url=videoURL))
	next = getNext(url, VideoPlaylistsMenu)
	if next != None: dir.Append(next)
	return dir
	
def SketchMenu(sender, url):
	dir = MediaContainer(title2=sender.itemTitle)
	for item in HTML.ElementFromURL(url).xpath("//div[@class='media horizontal sketch_group']"):
		title = item.xpath('./a')[0].get('title')
		videoURL = urljoin(url, item.xpath('./a')[0].get('href'))
		summary = item.xpath('./div[@class="details"]/p')[0].text.strip()
		thumb = item.xpath('./a/img')[0].get('src')
		dir.Append(Function(DirectoryItem(ShowMenu, title=title, summary=summary, thumb=thumb), url=videoURL))
	next = getNext(url, SketchMenu)
	if next != None: dir.Append(next)
	return dir

def ShowMenu(sender, url):
	dir = MediaContainer(title2=sender.itemTitle)
	for item in HTML.ElementFromURL(url).xpath('//div[@class="media video horizontal"]'):
		title = item.xpath('./a')[0].get('title')
		itemURL = item.xpath('./a')[0].get('href')
		summary = item.xpath('./div[@class="details"]/p')[0].text.strip()
		thumb = item.xpath('./a/img')[0].get('src')
		dir.Append(Function(VideoItem(GetFlvUrl, title=title, summary=summary, thumb=thumb), url=itemURL))
	next = getNext(url, ShowMenu)
	if next != None: dir.Append(next)
	return dir

def getNext(url, menu):
    next = HTML.ElementFromURL(url).xpath('//a[@class="next"]')
	if len(next) != 0:
		return Function(DirectoryItem(menu, title='Next', thumb=R('Next.png')), url=urljoin(CH_ROOT, next[0].get('href')))
