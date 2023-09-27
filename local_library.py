import os
import requests
import warnings
import urllib3

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlsplit

url = "https://tululu.org/b9/"


def check_for_redirect(response):
    if response.status_code != 200:
        raise requests.HTTPError


def parse_book_page(url):
    try:
        response = requests.get(url, verify=False, allow_redirects=False)
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
        return None  # Return None if there's an error


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


def download_txt(url, filename, folder="books/"):
    filename = sanitize_filename(filename)
    filepath = os.path.join(folder, f"{filename}.txt")
    return filepath


for book in range(1, 11):
    download_url = f'https://tululu.org/txt.php?id={book}'
    info_url = f'https://tululu.org/b{book}/'
    try:
        book_info = parse_book_page(info_url)

        if book_info is not None:
            # Continue with the rest of your code here
            pass
        else:
            print(f"Skipping book {book} due to error.")

    except requests.HTTPError:
        print(f"HTTPError for book {book}")
        continue  # Continue to the next book
    except Exception as e:
        print(f"Error for book {book}: {e}")
        continue  # Continue to the next book

    # book_title = get_book_title(info_url)
    # books_filepath = download_txt(download_url, book_title)
    # response = requests.get(download_url, verify=False, allow_redirects=False)
    # book_image_url = get_bookimage(info_url)
    # if book_image_url == "No picture available":
    #     print(f"The book {book_title} has no picture.")
    # else:
    #     download_bookimage(book_image_url)

    # try:
    #     genres = get_genres(info_url)
    #     if genres is not None:
    #         # Continue with the rest of your code here
    #         pass
    #     else:
    #         print(f"Skipping book {book} due to error.")
    # except Exception as e:
    #     print(f"Error for book {book}: {e}")
