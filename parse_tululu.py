import argparse
import os
import requests
import urllib3

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlsplit

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://tululu.org/b9/"
download_url = 'https://tululu.org/txt.php?id=9'


def check_for_redirect(response):
    if response.history:
        print(f"Redirect detected for {response.url}")
        raise requests.HTTPError


def download_comments(url, folder='comments'):
    response = requests.get(url, verify=False, allow_redirects=False)
    check_for_redirect(response)
    soup = BeautifulSoup(response.text, "lxml")
    comments = soup.find_all("div", class_="texts")
    book_title = (soup.find("h1").text.split("::"))[0].strip()
    os.makedirs(folder, exist_ok=True)
    filename = os.path.join(folder, f'{book_title}.txt')
    with open(filename, 'w', encoding='utf-8') as file:
        for comment in comments:
            full_comment = comment.get_text()
            full_comment.split(')')
            comment_text = (full_comment.split(')'))[1].strip()
            file.write(comment_text + '\n')


def parse_book_page(url):
    try:
        response = requests.get(url, verify=False, allow_redirects=False)
        check_for_redirect(response)
        soup = BeautifulSoup(response.text, "lxml")
        genres = (soup.find(
            "span", class_="d_book").find('a')['title']).split('-')[0]
        comments = soup.find_all("div", class_="texts")
        comment_texts = []
        for comment in comments:
            full_comment = comment.get_text()
            full_comment.split(')')
            comment_text = (full_comment.split(')'))[1].strip()
            comment_texts.append(comment_text)
        book_title_and_author = soup.find("h1").text.split("::")
        book_title, book_author = (book_title_and_author[0].strip(),
                                   book_title_and_author[1].strip())
        book_info = {'title': f'{book_title}',
                     'author': f'{book_author}',
                     'genres': f'{genres}',
                     'comments': f'{comment_texts}'}
        return book_info
    except requests.HTTPError:
        print(f"HTTPError for book {url}")


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
    check_for_redirect(response)
    filename = os.path.join(
        folder, image_name)
    with open(filename, 'wb') as file:
        file.write(response.content)


def download_book(url, payload, filename, folder="books/"):
    filepath = os.path.join(folder, f"{filename}.txt")
    response = requests.get(url, verify=False, allow_redirects=False)
    response.raise_for_status()
    check_for_redirect(response)
    with open(filepath, 'wb') as file:
        file.write(response.content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Downloads books and their covers from tululu.org')
    parser.add_argument(
        'start_id', type=int,
        help='С какой книги начнется скачивание', default=1)
    parser.add_argument(
        'end_id', type=int,
        help='На какой книге закончится скачивание', default=11)
    args = parser.parse_args()
    try:
        for book in range(args.start_id, args.end_id + 1):
            download_url = 'https://tululu.org/txt.php'
            download_payload = {'id': book}
            book_info_url = f'https://tululu.org/b{book}/'
            response = requests.get(
                book_info_url, verify=False, allow_redirects=False)
            response.raise_for_status()
            if response.status_code == 302:
                continue
            check_for_redirect(response)
            soup = BeautifulSoup(response.text, "lxml")
            book_title = (soup.find("h1").text.split("::"))[0].strip()
            download_book(download_url, download_payload, book_title)
            download_bookimage(get_bookimage(book_info_url))
            download_comments(book_info_url)
    except Exception as e:
        print(f'Something went wrong: {e}')
