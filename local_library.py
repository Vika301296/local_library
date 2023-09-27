import os
import requests

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

folder = 'books'


def get_book_title(url):
    response = requests.get(url, verify=False, allow_redirects=False)
    try:
        check_for_redirect(response)
        soup = BeautifulSoup(response.text, 'lxml')
        book_title_and_author = soup.find('h1').text.split('::')
        print(book_title_and_author)
        book_title = book_title_and_author[0].strip()
        book_author = book_title_and_author[1].strip()
        print(book_title)
        return book_title
    except requests.HTTPError:
        print(f"HTTPError for book {url}")


def download_txt(url, filename, folder='books/'):
    filename = sanitize_filename(filename)
    filepath = os.path.join(folder, f'{filename}.txt')
    print(filepath)
    return filepath


def check_for_redirect(response):
    if response.status_code != 200:
        raise requests.HTTPError


for book in range(1, 11):
    download_url = f'https://tululu.org/txt.php?id={book}'
    info_url = f'https://tululu.org/b{book}/'

    # filename = os.path.join(
    #     folder, f'book_{book}.txt')
    filename = get_book_title(info_url)
    print(filename)
    filepath = download_txt(download_url, filename)
    print(filepath)
    response = requests.get(download_url, verify=False, allow_redirects=False)

    try:
        check_for_redirect(response)
        with open(filepath, 'wb') as file:
            file.write(response.content)
    except requests.HTTPError:
        print(f"HTTPError for book {book}")
