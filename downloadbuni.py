#! python3
# downloadbuni.py - downloads specified number of bunicomics.

import requests, os, bs4

url = 'http://www.bunicomic.com/'
os.makedirs('bunicomic', exist_ok = True)
for i in range(0,5):
	print('Downloading page %s...' %url)
	res = requests.get(url)
	res.raise_for_status()

	soup = bs4.BeautifulSoup(res.text, "html.parser")

	comicElem = soup.select('#comic img')
	if comicElem == []:
		print('Could not find comic image.')
	else:
		try:
			comicUrl = comicElem[0].get('src')
			print('Downloading image %s...' % (comicUrl))
			res = requests.get(comicUrl)
			res.raise_for_status()
		except requests.exceptions.MissingSchema:
			prevLink = soup.find_all("a", attrs={"class": "comic-nav-base comic-nav-previous"})[0]
			url = prevLink.get('href')
			continue

	imageFile = open(os.path.join('bunicomic', os.path.basename(comicUrl)), 'wb')
	for chunk in res.iter_content(100000):
		imageFile.write(chunk)
	imageFile.close()

	prevLink = soup.find_all("a", attrs={"class": "comic-nav-base comic-nav-previous"})[0]
	url = prevLink.get('href')

print('Done.')


