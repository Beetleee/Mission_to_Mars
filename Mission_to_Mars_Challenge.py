# Import Splinter and BeautifulSoup
from splinter import Browser
import pandas as pd
from bs4 import BeautifulSoup as soup
import time
from webdriver_manager.chrome import ChromeDriverManager


# executable_path = {'executable_path': ChromeDriverManager().install()}
# browser = Browser('chrome', **executable_path, headless=False)
executable_path = {'executable_path': ChromeDriverManager(version = '98.0.4758.102').install()}

browser = Browser('chrome', **executable_path, headless=False)


# Visit the NASA Mars News Site


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
#we're searching for elements with a specific combination of tag (div) and attribute (list_text). As an example, ul.item_list would be found in HTML as <ul class="item_list">.
#Secondly, we're also telling our browser to wait one second before searching for components.
browser.is_element_present_by_css('div.list_text', wait_time=1)

# set up the HTML parser:
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

# assign the title and summary text to variables we'll reference later. (.find = this variable holds a ton of info, so look inside of that info to find this)
slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# Find and click the full image button; indexing on first line of code stipulates that we want our browser to click the second button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# Find the relative image url; An img tag is nested within this HTML, so we've included it.
# .get('src') pulls the link to the image.
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/image/featured/mars2.jpg'
img_url


# Mars Facts


# go to a new website to grab a table; creating a new DataFrame from the HTML table. 
# The Pandas function read_html() specifically searches for and returns a list of tables found in the HTML. 
# By specifying an index of 0, we're telling Pandas to pull only the first table it encounters, or the first item in the list. 
# Then, it turns the table into a DataFrame.
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


df.to_html()


# D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# Hemispheres


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)

html = browser.html

img_soup = soup(html, 'html.parser')


# Retreive all items that contain mars hemispheres information
parent = img_soup.find_all('div', class_='item')

# 2. Create empty list for hemisphere urls 
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
# 3A. create lists for images and titles 
images = []
titles = []
for item in parent:
    images.append(url + item.find('a')['href'])
    titles.append(item.find('h3').text.strip())
print(images)
titles


# 3B. create full length url template
browser.visit(images[0])
html = browser.html
img_soup = soup(html, 'html.parser')

single_url = url + img_soup.find('img',class_='wide-image')['src']
single_url


# 3C. create full length url  for each image
img_urls = []
for single_url in images:
    browser.visit(single_url)
    html = browser.html
    img_soup = soup(html, 'html.parser')
#  3D. savetofile
    single_url = url+img_soup.find('img',class_='wide-image')['src']
    img_urls.append(single_url)
    
img_urls


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls = []

for i in range(len(titles)):
    hemisphere_image_urls.append({'title':titles[i],'img_url':img_urls[i]})

hemisphere_image_urls


# 4A. Print the individual linked image url and title.
for i in range(len(hemisphere_image_urls)):
    print(hemisphere_image_urls[i]['title'])
    print(hemisphere_image_urls[i]['img_url'] + '\n')


# 5. Quit the browser
browser.quit()

hemisphere_image_urls




