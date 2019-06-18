#libraries
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

#makes a csv file
filename = "metacritic.csv"
f = open(filename, "w")

headers = "game_title, genre, platforms, release_date, developers,metascore_rating\n"

f.write(headers)

### Metacritic Page Information ###

mc_genres = ["action", "adventure","fighting","first-person","flight", "party", "platformer","puzzle", "racing","real-time", "role-playing", "simulation", "sports", "strategy", "third-person", "turn-based", "wargame", "wrestling"]


### MAIN PAGE ###
for genre in mc_genres: 	
	#Last Page Grabber
	p_url = 'https://www.metacritic.com/browse/games/genre/metascore/'+ genre + '/all?view=condensed'
	pClient = Request(p_url, headers={'User-Agent': 'Mozilla/5.0'})
	page_number_html = urlopen(pClient).read()
	urlopen(pClient).close
	page_number_soup = soup(page_number_html, "html.parser")
	page_container = page_number_soup.findAll("li", {"class":"page last_page"})[0].text

	#Function that converts page number into integer
	def page_number(con):
		if ord(con[0]) == 8230:
			return int(con[1:])
		else:
			return int(con)			

	last_page = page_number(page_container)

	for page in range(last_page):

		number = str(page)

		#Notifier
		print('Currently at:' + genre + ' - ' + 'page: ' + number)

		mc_url = 'https://www.metacritic.com/browse/games/genre/metascore/' + genre + '/all?view=condensed&page=' + number

		if page == 0:
			mc_url = 'https://www.metacritic.com/browse/games/genre/metascore/'+ genre + '/all?view=condensed'
			

		uClient = Request(mc_url, headers={'User-Agent': 'Mozilla/5.0'})
		page_html = urlopen(uClient).read()
		urlopen(uClient).close

		#html parser
		page_soup = soup(page_html, "html.parser")

		#containers - <an array>
		con_first = page_soup.findAll("li", {"class":"product game_product first_product"})
		con_first_last = page_soup.findAll("li", {"class":"product game_product first_product last_product"})
		con_body = page_soup.findAll("li", {"class":"product game_product"})
		con_last = page_soup.findAll("li", {"class":"product game_product last_product"})

		containers = (con_first + con_first_last + con_body)

		#grabs href(link) of each container
		for container in containers:
			page_empty = False
			link = container.findAll('a')[0].get('href')

			#Game Rating
			rating_container = container.findAll("div", {"class":"metascore_w small game positive"}) + container.findAll("div", {"class":"metascore_w small game mixed"}) + container.findAll("div", {"class":"metascore_w small game negative"})
			game_rating = rating_container[0].text.strip()

			### GAME URL ###

			game_url = 'https://www.metacritic.com' + link

			gClient = Request(game_url, headers={'User-Agent': 'Mozilla/5.0'})
			try:
				game_page_html = urlopen(gClient).read()
				urlopen(gClient).close
			except:
				page_empty = True


			#html parser for each game page
			game_page_soup = soup(game_page_html, "html.parser")

			### GAME PAGE ###

			#Detects if game page has an error
			if page_empty:
				pass

			else:
				#Game Title
				game_title = game_page_soup.findAll('a', {"href": link})[0].text.strip().replace(',', ' ')
				print(game_title)

				#Game Genre
				genre_container = game_page_soup.findAll('li', {"class": 'summary_detail product_genre'})[0].findAll('span',{"class": 'data'})
				game_genres = []
				for genre_tag in genre_container:
					game_genres = game_genres + [genre_tag.text]

				game_genres = list(set(game_genres))

				game_genres = '|'.join(str(x) for x in game_genres)

				#Game Platforms
				game_platforms = [game_page_soup.findAll('span', {'class':'platform'})[0].text.strip()]

				if game_page_soup.findAll('li', {"class":'summary_detail product_platforms'}):
					platform_container = game_page_soup.findAll('li', {"class":'summary_detail product_platforms'})[0].findAll('a', {"class":"hover_none"})
					for platform in platform_container:
						game_platforms = game_platforms + [platform.text.strip()]

				game_platforms = '|'.join(str(x) for x in game_platforms)

				#Game Release Date 
				game_release = game_page_soup.findAll('li', {'class':'summary_detail release_data'})[0].findAll('span', {'class':'data'})[0].text.strip().replace(',', '')

				#Game Developer
				if game_page_soup.findAll('li', {"class": 'summary_detail developer'}):
					developer_container = game_page_soup.findAll('li', {"class": 'summary_detail developer'})[0].findAll('span',{"class": 'data'})
					game_developers = []
					for developer_tag in developer_container:
						game_developers = game_developers + [developer_tag.text.strip().replace(',','|')]

					game_developers = list(set(game_developers))

					game_developers = '|'.join(str(x) for x in game_developers)
				else:
					game_developers = 'N/A'

				f.write(game_title + "," + game_genres + "," + game_platforms + "," + game_release + "," + game_developers + "," + game_rating + "\n")
			
f.close()




