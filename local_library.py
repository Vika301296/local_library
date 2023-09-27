import os
import requests
import warnings
import urllib3

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from pathlib import Path
from urllib.parse import urljoin, urlsplit

warnings.filterwarnings("ignore")
# Disable SSL certificate verification warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.NotOpenSSLWarning)
folder = "books"
current_directory = os.getcwd()
images_directory = os.path.join(current_directory, 'images')

# Create the 'images' directory if it doesn't exist
os.makedirs(images_directory, exist_ok=True)
# /Users/viktoriafedorova/Desktop/Devman/local_library/images
url = "https://tululu.org/b9/"


def get_bookimage(url):
    try:
        response = requests.get(url, verify=False, allow_redirects=False)
        soup = BeautifulSoup(response.text, "lxml")
        bookimage_div = soup.find("div", class_="bookimage")
        if bookimage_div:
            book_image = bookimage_div.find("img")['src']
            book_image_url = urljoin('https://tululu.org/', book_image)
            return book_image_url
        else:
            return "No picture available"
    except requests.HTTPError:
        print(f"HTTPError for book {url}")


def download_bookimage(url, folder='images'):
    image_name = os.path.basename(urlsplit(
        url, scheme='', allow_fragments=True)[2])
    response = requests.get(url, verify=False, allow_redirects=False)
    filename = os.path.join(
        folder, image_name)
    with open(filename, 'wb') as file:
        file.write(response.content)


# book_image_url = get_bookimage(url)
# print(download_bookimage(book_image_url))


def get_book_title(url):
    response = requests.get(url, verify=False, allow_redirects=False)
    try:
        check_for_redirect(response)
        soup = BeautifulSoup(response.text, "lxml")
        book_title_and_author = soup.find("h1").text.split("::")
        book_title = book_title_and_author[0].strip()
        book_author = book_title_and_author[1].strip()
        return book_title
    except requests.HTTPError:
        print(f"HTTPError for book {url}")


def download_txt(url, filename, folder="books/"):
    filename = sanitize_filename(filename)
    filepath = os.path.join(folder, f"{filename}.txt")
    return filepath


def check_for_redirect(response):
    if response.status_code != 200:
        raise requests.HTTPError


for book in range(1, 11):
    download_url = f'https://tululu.org/txt.php?id={book}'
    info_url = f'https://tululu.org/b{book}/'
    book_title = get_book_title(info_url)
    books_filepath = download_txt(download_url, book_title)
    response = requests.get(download_url, verify=False, allow_redirects=False)
    book_image_url = get_bookimage(info_url)

    if book_image_url == "No picture available":
        print(f"The book {book_title} has no picture.")
    else:
        download_bookimage(book_image_url)


    # try:
    #     check_for_redirect(response)
    #     with open(books_filepath, 'wb') as file:
    #         file.write(response.content)
    # except requests.HTTPError:
    #     print(f"HTTPError for book {book}")
