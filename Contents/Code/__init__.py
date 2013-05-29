BASE_URL = 'http://www.collegehumor.com'
ORIGINALS_HOME = '%s/originals' % BASE_URL
RECENT = '%s/videos' % BASE_URL
MOST_VIEWED = '%s/videos/most-viewed' % BASE_URL
SKETCH_COMEDY = '%s/sketch-comedy/alphabetical/page:%%d' % BASE_URL

####################################################################################################
def Start():

	ObjectContainer.title1 = 'CollegeHumor'
	HTTP.CacheTime = CACHE_1HOUR
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0'

####################################################################################################
@handler('/video/collegehumor', 'CollegeHumor')
def MainMenu():

	oc = ObjectContainer()

	oc.add(DirectoryObject(key=Callback(OriginalsMenu, title='Originals'), title='Originals'))
	oc.add(DirectoryObject(key=Callback(ShowMenu, url=RECENT, title='Recently Added'), title='Recently Added'))
	oc.add(DirectoryObject(key=Callback(ShowMenu, url=MOST_VIEWED, title='Most Viewed'), title='Most Viewed'))
	oc.add(DirectoryObject(key=Callback(SketchMenu, title='Sketch Comedy'), title='Sketch Comedy'))

	return oc

####################################################################################################
@route('/video/collegehumor/originals')
def OriginalsMenu(title):

	oc = ObjectContainer(title2=title)
	html = HTML.ElementFromURL(ORIGINALS_HOME)

	for show in html.xpath('//div[@id="series-carousel"]//a/img/parent::a'):
		url = BASE_URL + show.get('href')
		title = show.get('title')
		thumb = show.xpath('./img/@src')[0]

		oc.add(DirectoryObject(
			key = Callback(ShowMenu, url=url, title=title),
			title = title,
			thumb = Resource.ContentsOfURLWithFallback(url=thumb)
		))

	return oc

####################################################################################################
@route('/video/collegehumor/sketchcomedy')
def SketchMenu(title):

	oc = ObjectContainer(title2=title)
	html = HTML.ElementFromURL(SKETCH_COMEDY % 1)

	last_page = html.xpath('//div[@class="pagination"]/a[not(@class)][last()]/@href')
	if len(last_page) < 1:
		pages = 1
	else:
		pages = int(last_page[0].split(':')[1])

	for page in range(1, pages+1):
		for show in HTML.ElementFromURL(SKETCH_COMEDY % page).xpath('//div[@class="primary"]//div[contains(@class, "sketch-group")]/a'):
			url = BASE_URL + show.get('href')
			title = show.get('title')
			thumb = show.xpath('./img/@src')[0]

			oc.add(DirectoryObject(
				key = Callback(ShowMenu, url=url, title=title),
				title = title,
				thumb = Resource.ContentsOfURLWithFallback(url=thumb)
			))

	return oc

####################################################################################################
@route('/video/collegehumor/show', page=int)
def ShowMenu(url, title, page=1):

	oc = ObjectContainer(title2=title)
	html = HTML.ElementFromURL('%s/page:%d' % (url, page))

	for item in html.xpath('//div[@class="primary"]//div[contains(@class, "media")]/a'):
		video_url = BASE_URL + item.get('href')

		if '/playlist/' in video_url:
			continue

		video_title = item.get('title')
		thumb = item.xpath('./img/@src')[0]

		oc.add(VideoClipObject(
			url = video_url,
			title = video_title,
			thumb = Resource.ContentsOfURLWithFallback(url=thumb)
		))

	if len(html.xpath('//a[@class="next"]')) > 0:
		oc.add(NextPageObject(
			key = Callback(ShowMenu, url=url, title=title, page=page+1),
			title = 'More...'
		))

	return oc
