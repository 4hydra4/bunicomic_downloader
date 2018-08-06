#! python3
# multidownloadbuni.py - downloads specified number of bunicomics.

import requests, os, bs4, threading

os.makedirs('bunicomic', exist_ok = True)

def downloadbuni(startComic, endComic):
	for urlNumber in range(startComic,endComic):
		print('Downloading page http://www.bunicomic.com/comic/buni-%s...' %urlNumber)
		res = requests.get('http://www.bunicomic.com/comic/buni-%s' %(urlNumber))
		res.raise_for_status()

		soup = bs4.BeautifulSoup(res.text, "html.parser")

		comicElem = soup.select('#comic img')
		if comicElem == []:
			print('Could not find comic image.')
		else:
			
			comicUrl = comicElem[0].get('src')
			print('Downloading image %s...' % (comicUrl))
			res = requests.get(comicUrl)
			res.raise_for_status()
			

		imageFile = open(os.path.join('bunicomic', os.path.basename(comicUrl)), 'wb')
		for chunk in res.iter_content(100000):
			imageFile.write(chunk)
		imageFile.close()

downloadThreads = []
for i in range(1110, 1130, 5):
	downloadThread = threading.Thread(target = downloadbuni, args=(i, i+4))
	downloadThreads.append(downloadThread)
	downloadThread.start()

for downloadThread in downloadThreads:
	downloadThread.join()
print('Done.')


