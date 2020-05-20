import argparse
import json
import math
import os
from livereload import Server, shell
from jinja2 import Environment, FileSystemLoader, select_autoescape

def on_reload():
    create_template(template, books_description, step)
    print('reload!')

def create_template(template, books_description, step):

    books_count = len(books_description)
    total_pages = math.ceil(books_count/step)
    page_numbers = list(range(1,total_pages+1))
    page_number = 1
    folder = 'pages'
    os.makedirs(folder, exist_ok=True)

    for books in range(0,books_count, step):
        rendered_page = template.render(
            books_description=books_description[books:books+step],
            page_numbers=page_numbers,
            current_page=page_number,
            next_page=page_number+1,
            previous_page=page_number-1,
        )
        filename = f'index{page_number}.html'
        filename_path = os.path.join(folder, filename)
        with open(filename_path, 'w', encoding="utf8") as file:
            file.write(rendered_page)
        page_number = page_number + 1


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Library creater (tululu.org)')
    parser.add_argument('--books', default=20, help='Books per page (default 20)')
    args = parser.parse_args()

    step = int(args.books)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    try:
        with open("books_description.json", "r") as my_file:
            books_description_json = my_file.read()
    except FileNotFoundError:
        print('File "books_description.json" does not exist')
        exit()
    books_description = json.loads(books_description_json)

    create_template(template, books_description, step)

    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')