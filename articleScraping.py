import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

# Function to fetch the content of a single page
def scrape_fashion_articles(url):
    # Fetch the page content
    response = requests.get(url)

    # Check for successful response
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Use a list of possible class names for articles
    articles = soup.find_all(class_=["SummaryItemContent-eiDYMl fSburJ summary-item__content", 
                                     "SummaryItemContent-eiDYMl dogWHS summary-item__content"])  # Get all article blocks
    
    article_data = []
    
    for article in articles:
        # Extracting title, URL, and other details
        title_element = article.find(class_="SummaryItemHedBase-hiFYpQ gXMLHo summary-item__hed")
        title = title_element.get_text() if title_element else "No title"
        
        # Extract the link; handle missing link with a fallback
    
        link_element = article.find('a', class_=["SummaryItemHedLink-civMjp dVrbhU summary-item-tracking__hed-link summary-item__hed-link",
                                                 "SummaryItemHedLink-civMjp bMCiCb summary-item-tracking__hed-link summary-item__hed-link"])
        link = link_element['href'] if link_element else "No link"
        
        # If the link is relative, join with base URL
        if link != "No link" and not link.startswith('http'):
            link = urljoin(url, link)
        
        # Store the data in a dictionary
        article_data.append({
            'title': title,
            'link': link,
        })
    
    return article_data

# Function to fetch and parse content from an individual article page
def get_article_data(url):
    # Fetch the page content
    response = requests.get(url)

    # Check for successful response
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return "No content"
    
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract title of the article
    title_element = soup.find(class_="BaseWrap-sc-gjQpdd BaseText-ewhhUZ ContentHeaderHed-NCyCC iUEiRd lehtlV isouMH")
    title = title_element.get_text() if title_element else "No title"

    # Extract content of the article
    content_element = soup.find('p')
    content = content_element.get_text() if content_element else "No content"
    
    return content


# Function to export data to JSON
def export_to_json(article_data, filename="/Users/dhurgadharani/Fashion/data/fashion_articles.json"):
    # Open the JSON file in write mode
    with open(filename, mode='w') as file:
        json.dump(article_data, file, indent=4, ensure_ascii=False)  # Write the data to the file

# Example usage
fashion_url = 'https://www.vogue.com/fashion'  # Replace with a real URL
articles = scrape_fashion_articles(fashion_url)

# Display the scraped data
for article in articles:
    #print(f"Title: {article['title']}")
    #print(f"Link: {article['link']}")
    
    link = article['link']

    if link == "No link":
        article['content'] = "No content"
    else:
        content = get_article_data(link)
        article['content'] = content
        #print(f"Content: {article['content'][:150]}...")  # Print first 150 characters of content
        
    #print('-' * 80)

# Example usage
export_to_json(articles)
print("Done!")
