import urllib.request, os, sys, string
from bs4 import BeautifulSoup

class App:

	def __init__(self):
		self.url = 'http://feeds.reuters.com/Reuters/worldNews' 
		self.update_feed()

	def update_feed(self):
		response = request(self.url)
		self.data = parse_feed(response)

	def display(self):

		options = '[1] Go Back\n[2] Read Full Article\n>>> '

		while True:

			clear()
			print(self.title_page())
			print('0.  To quit')

			for e, data in enumerate(self.data):
				if e >= 9:
					print('%d. %s'%((e+1), data))
				else:
					print('%d.  %s'%((e+1), data))
			try:
				selection = int(input('\nSelect a Story (by number)\n>>> '))
				if selection == 0:
					clear()
					sys.exit(0)
				else:
					article = self.data[selection-1]
			except (ValueError, IndexError) as e:
				print('Selection must be a number in the list.')
			else:

				clear()
				print(repr(article))

				if input(options) == '1':
					continue
				else:					
					text = self.fetch(article)
					input('\n[END OF ARTICLE]\n')
					while True:
						clear()
						print('Select an option...\n')
						print('[1] go back to Feed.')
						print('[2] Save [%s] to txt file.'%(article.title))
						option = input('>>> ')
						if option == '2':
							self.save(article, text)
							break
						elif option == '1':
							break

	def fetch(self, article):
		print()
		response = request(article.link)
		return parse_article(response)

	def save(self, article, text):
		template = '{border}\n{date}\n{title}\n{border}\n\n'
		fname = article.title
		for symbol in string.punctuation:
			fname = fname.replace(symbol, '')
		fname = fname+'.txt'
		fhand = open(fname, 'w')
		fhand.write(template.format(**article.dict))
		fhand.write(text)
		fhand.close()
		print('\nArticle has been saved to: %s'%os.getcwd())
		input('\nPress [ENTER] to continue...')

	def title_page(self):
		return '''{0}
{1} Reuters World News RSS Feed Reader {1}
{0}
'''.format(('='*80), ('#'*22))

class DataObject:

	def __init__(self, data):
		self.data  = data
		self.title = data.title.text.title()
		self.desc  = data.description.text
		self.link  = data.guid.text.split('?')[0]
		self.date  = data.pubdate.text
		self.dict  = dict()
		self.dict['border'] = '='*80
		self.dict['title']  = self.title
		self.process_data()

	def process_data(self):
		self.process_desc()
		self.process_date()

	def process_desc(self):
		desc = self.desc.split('.')[0]+'.'
		desc = desc.split()
		count, temp = 0, ''
		for word in desc:
			count += len(word)+1
			if count < 76:
				temp += word+' '
			else:
				temp += '\n\t'+word+' '
				count = len(word)+1
		self.dict['desc'] = temp+'\n'
	
	def process_date(self):
		date = ' '.join(self.date.split()[:4])
		self.dict['date'] = date

	def __repr__(self):
		template = '{border}\n{date}\n{title}\n{border}\n\n\t{desc}\n{border}\n'
		return template.format(**self.dict)

	def __str__(self):
		return self.title
	
def request(url):
	headers = {'user-agent': 'Firefox'}
	req = urllib.request.Request(url, headers=headers)
	try:
		response = urllib.request.urlopen(req)
	except Exception as e:
		print(str(e))
	return response if response.code == 200 else None

def parse_feed(response):
	data = []
	html = response.read()
	soup = BeautifulSoup(html, 'html.parser')
	data_items = soup.find_all('item')
	for data_item in data_items:
		data.append(DataObject(data_item))
	return data

def parse_article(response):
	html = response.read()
	soup = BeautifulSoup(html, 'html.parser')
	paragraphs = soup.find_all('p')
	text_object = ''
	print('(press enter for next paragraph...)\n')
	for text in paragraphs:
		text = text.text
		text = process_text(text)
		text_object += text+'\n\n'
		input(text+'\n')
	return text_object

def process_text(text):
	text = text.split()
	count, temp = 0, ''
	for word in text:
		count += len(word)+1
		if count < 80:
			temp += word+' '
		else:
			temp += '\n'+word+' '
			count = len(word)+1
	return temp
	
def clear():
	if 'win' in sys.platform:
		os.system('cls')
	else:
		os.system('clear')

def main():
    app = App()
    app.display()

if __name__ == '__main__':
	main()
