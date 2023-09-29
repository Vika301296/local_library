# Парсер книг с сайта tululu.org

Данный парсер позволяет скачивать книги, изображения, а также выводит информацию о книге:
- название
- автора
- жанр
- комментарии

### Как установить

Для запуска блога у вас уже должен быть установлен Python 3.

- Скачайте код
- Установите зависимости командой `pip install -r requirements.txt`

### Аргументы

При работе со скриптом используются два необязательных аргумента:
- `--start_page` обозначает id книги, с которой вы хотите начать скачивание
- `--end_page` обозначает id книги, на которой вы хотите закончить скачивание 
Если аргументы не указаны, скачивание начнется с 1-й книги и закончится на 9-й
### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).