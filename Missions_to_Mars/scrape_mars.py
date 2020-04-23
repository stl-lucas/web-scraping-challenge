from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd

def scrape():
    scraped_dict = {}

    # Initialize Browser
    executable_path = {"executable_path": "chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)

    # Nasa Mars News
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")

    scraped_dict['news_title'] = soup.find("div", class_="list_text").find("div", class_="content_title").find("a").get_text()
    scraped_dict['news_p'] = soup.find("div", class_="article_teaser_body").get_text()

    # JPL Mars Images
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")

    s = soup.find("article", class_="carousel_item")['style']
    start = s.find("url('")
    end = s.find("');")
    scraped_dict['feature_image_url'] = 'https://www.jpl.nasa.gov' + s[start+len("url('"):end]

    # Mars Twitter Feed
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")

    scraped_dict['mars_weather'] = soup.find("span", {"class": "css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0"})

    # Mars Hemisphere Data
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")
    image_links = soup.find_all("div", {"class": "description"})

    links = []
    for item in image_links:
        links.append(item.find("a").find("h3").get_text())

    hemisphere_image_urls = []
    base_url = 'https://astrogeology.usgs.gov/'
    for link in links:
        browser.click_link_by_partial_text(link)
        new_html = browser.html
        new_soup = bs(new_html, "html.parser")
        title = new_soup.find("h2", {"class": "title"}).get_text()
        img_url = base_url + new_soup.find("img", {"class": "wide-image"})['src']
        hemisphere_image_urls.append({"title": title, "img_url": img_url})
        browser.back()
    
    scraped_dict['hemisphere_image_urls'] = hemisphere_image_urls
    
    return scraped_dict