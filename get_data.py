from bs4 import BeautifulSoup
from urllib2 import urlopen
import nltk.data
from unidecode import unidecode
import os
import xml.etree.cElementTree as ET

sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

BLOG_URLS = [
	{
		"url": 'https://creatingmemories.blogspot.ca',
		"bad": 'filters/demblog1_bad.txt',
		"quest": 'filters/demblog1_questionable.txt'
	},
	{
		"url": 'http://living-with-alzhiemers.blogspot.ca',
		"bad": 'filters/demblog2_bad.txt',
		"quest": 'filters/demblog2_questionable.txt'
	},
	{
		"url": 'http://parkblog-silverfox.blogspot.ca',
		"bad": 'filters/demblog3_bad.txt',
		"quest": 'filters/demblog3_questionable.txt'
	},
	{
		"url": 'http://journeywithdementia.blogspot.ca',
		"bad": "",
		"quest": ""
	},
	{
		"url": 'http://earlyonset.blogspot.ca',
		"bad": "",
		"quest": ""
	},
	{
		"url": 'http://helpparentsagewell.blogspot.ca',
		"bad": "",
		"quest": ""
	},
]


def create_corpus(path):
	root = ET.Element("root")
	for blog in BLOG_URLS:
		posts_to_xml(root, blog['url'], blog['quest'], blog['bad'])
	tree = ET.ElementTree(root)
	tree.write(path)


def posts_to_xml(root, url, questurl, badurl):
	blog = ET.SubElement(root, "blog", name=url)
	print "Gathering posts from: %s" % url
	r = urlopen(url).read()
	
	# Gather posts
	soup = BeautifulSoup(r, 'html.parser')
	posts = _get_posts_xml_helper(soup, questurl, badurl)
	href = soup.find("a", {"class": "blog-pager-older-link"})
	while href:
		link = href['href']
		r = urlopen(link).read()
		soup = BeautifulSoup(r, 'html.parser')
		posts += _get_posts_xml_helper(soup, questurl, badurl)
		href = soup.find("a", {"class": "blog-pager-older-link"})
		print "%d posts collected" % len(posts)

	# Make xml
	for post in posts:
		xmlpost = ET.SubElement(blog, "post", date=post['date'], quality=post['quality'])
		for idx, s in enumerate(post['sentences']):
			ET.SubElement(xmlpost, "sentence", id=str(idx)).text = s


# Small helper function to turn file with dates into array
# Returns empty array from empty path
def _date_reader(path):
	if not path:
		return []
	else:
		dir = os.path.dirname(__file__)
		path = os.path.join(dir, path)
		with open(path) as file:
			dates = file.readlines()
			dates = [l.strip() for l in dates]
		return dates[1:]


# Helper to extract, parse and tag sentences from post 
def _get_posts_xml_helper(soup, questurl, badurl):
	posts = []
	for div in soup.findAll("div", {"class": "date-outer"}):
		date = div.h2.text
		text = div.find('div', "post-body entry-content").text
		post = filter(None, text.replace(u'\xa0', u' ').splitlines())
		sentence_segmented_post = sent_detector.tokenize(" ".join(post))
		decoded = [unidecode(s) for s in sentence_segmented_post]

		quest_posts = _date_reader(questurl)
		badposts    = _date_reader(badurl)

		if date in quest_posts:
			quality = 'questionable'
		elif date in badposts:
			quality = 'bad'
		else:
			quality = 'good'

		post = {
			'sentences': decoded,
			'date': date,
			'quality': quality,
		}

		posts.append(post)
	return posts


if __name__ == '__main__':
	create_corpus("blog_corpus.xml")
