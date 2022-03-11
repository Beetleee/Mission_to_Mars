# Import Splinter and BeautifulSoup
from splinter import Browser
import pandas as pd
import datetime as dt
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
# executable_path = {'executable_path': ChromeDriverManager().install()}
# browser = Browser('chrome', **executable_path, headless=False)
   executable_path = {'executable_path': ChromeDriverManager(version = '98.0.4758.102').install()}
   browser = Browser('chrome', **executable_path, headless=True)

   news_title, news_paragraph = mars_news(browser)
   # Run all scraping functions and store results in a dictionary
   data = {

    "news_title": news_title,
    "news_paragraph": news_paragraph,
    "featured_image": featured_image(browser),
    "facts": mars_facts(),
    "last_modified": dt.datetime.now(),
    "hemisphere_image_urls": hemispheres(browser),
    }

   # Stop webdriver and return data
   browser.quit()
   return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def hemispheres(browser):
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

    # 3B. create full length url template
    browser.visit(images[0])
    html = browser.html
    img_soup = soup(html, 'html.parser')

    single_url = url + img_soup.find('img',class_='wide-image')['src']

    # 3C. create full length url  for each image
    img_urls = []
    for single_url in images:
       browser.visit(single_url)
       html = browser.html
       img_soup = soup(html, 'html.parser')
    #  3D. savetofile
    single_url = url+img_soup.find('img',class_='wide-image')['src']
    img_urls.append(single_url)

    # 4. Print the list that holds the dictionary of each image url and title.
    hemisphere_image_urls = []

    for i in range(len(titles)):
       hemisphere_image_urls.append({'title':titles[i],'img_url':img_urls[i]})

    # 4A. Print the individual linked image url and title.
    for i in range(len(hemisphere_image_urls)):
       print(hemisphere_image_urls[i]['title'])
       print(hemisphere_image_urls[i]['img_url'] + '\n')

    # 5. Quit the browser
    browser.quit()

    return hemisphere_image_urls


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())
