import os
import requests

# filename = 'dvmn.svg'
# filename_1 = 'book.txt'
# url = "https://dvmn.org/filer/canonical/1542890876/16/"

# url_1 = 'https://tululu.org/txt.php?id=32168'

# response = requests.get(url_1, verify=False)
# response.raise_for_status()

# with open(filename_1, 'wb') as file:
#     file.write(response.content)
folder = 'books'
for book in range(1, 11):
    url = f'https://tululu.org/txt.php?id={book}'
    filename = os.path.join(
        folder, f'book_{book}.txt')
    response = requests.get(url, verify=False)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)
