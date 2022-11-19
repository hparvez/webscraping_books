from typing import List
import requests
import bs4
from bs4 import BeautifulSoup

RATINGS_DICT = {
    "ONE": 1,
    "TWO": 2,
    "THREE": 3,
    "FOUR": 4,
    "FIVE": 5
}


def get_page_soup(page_num: int) -> bs4.BeautifulSoup:
    """
    Function to generate a "soup" of a page, containing all
    the HTML tags

    Args:
        page_num (int): target page number

    Returns:
        bs4.BeautifulSoup: BeautifulSoup object of our target
        page number
    """
    url = f"https://books.toscrape.com/catalogue/page-{page_num}.html"
    response = requests.get(url)
    page_contents = response.text
    soup = BeautifulSoup(page_contents, "html.parser")
    return soup


def get_num_pages(doc: bs4.BeautifulSoup) -> int:
    """
    Function to extract the number of pages from a BeautifulSoup
    object, assuming its contained within the "current" class and
    is of the form "page x of y"

    Args:
        doc (bs4.BeautifulSoup): BeautifulSoup object of target web page

    Returns:
        int: number of pages in document
    """
    # Find element containining number of pages
    num_pages_element = doc.find("li", {"class": "current"}).text.strip()
    
    # Extract text for number of pages
    num_pages = num_pages_element.replace("Page 1 of ", "")
    num_pages_int = int(num_pages)
    return num_pages_int


def get_containers(doc: bs4.BeautifulSoup) -> List[bs4.BeautifulSoup]:
    """
    Function to extract the "product_pod" article from a BeautifulSoup
    object

    Args:
        doc (bs4.BeautifulSoup): BeautifulSoup objet of target web page

    Returns:
        List[bs4.BeautifulSoup]: list of BeautifulSoup objects containing
        the "product_pod" articles
    """
    return doc.find_all("article", {"class": "product_pod"})


def get_title(doc: bs4.BeautifulSoup) -> str:
    """
    Function to extract the title from a BeautifulSoup container object,
    assuming the title is contained with the "title" of an "<a>" tag within
    the <h3> tag

    Args:
        doc (bs4.BeautifulSoup): BeautifulSoup object container obtained via
        the "get_containers" method

    Returns:
        str: Book title
    """
    title_tag = doc.find("h3")
    a_tag = title_tag.find("a")
    return a_tag["title"]


def get_price(doc: bs4.BeautifulSoup) -> float:
    """
    Function to extract the price from a BeautifulSoup container object,
    assuming the price is contained within the "price_color" container

    Args:
        doc (bs4.BeautifulSoup): BeautifulSoup object container obtained via
        the "get_containers" method

    Returns:
        foat: price of book
    """
    # Of the form "Â£x.xx"
    price = doc.find("p", {"class": "price_color"}).text
    clean_price = price.replace("Â", "").replace("£", "")
    return float(clean_price)


def get_star_rating(doc: bs4.BeautifulSoup) -> int:
    """_summary_

    Args:
        doc (bs4.BeautifulSoup): _description_

    Returns:
        int: _description_
    """
    rating_words = doc.find('p').get("class")[1].upper()
    ratings_nums = RATINGS_DICT[rating_words]
    return ratings_nums

if __name__ == "__main__":
    
    # Generate soup of first page
    home_page = get_page_soup(page_num=1)

    # Get total number of pages to iterate over
    num_pages = get_num_pages(home_page)

    # Will take a list of dicts as the output
    book_results = []

    for page in range(num_pages):
        page_soup = get_page_soup(page_num=page)    
        
        book_containers = get_containers(page_soup)
        
        for container in book_containers:
            book_result = {
                "TITLE": get_title(container),
                "RATING": get_star_rating(container),
                "PRICE": get_price(container)
            }
            book_results.append(book_result)
