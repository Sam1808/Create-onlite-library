import argparse
import json
import os
from livereload import Server, shell
from more_itertools import chunked
from jinja2 import Environment, FileSystemLoader, select_autoescape

def on_reload():
    create_template(books_description, step)
    print('reload!')

def create_template(books_description, step):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    folder = 'pages'
    os.makedirs(folder, exist_ok=True)

    books_count = len(books_description)
    books_perpage_catalog = list(chunked(range(0,books_count), step))
    page_numbers = list(range(1,len(books_perpage_catalog)+1))

    for kit_id, books_kit in enumerate(books_perpage_catalog):
        page_number = kit_id+1
        rendered_page = template.render(
            books_description=books_description[books_kit[0]:books_kit[-1]],
            page_numbers=page_numbers,
            current_page=page_number,
            next_page=page_number+1,
            previous_page=page_number-1,
        )
        filename = f'index{page_number}.html'
        filename_path = os.path.join(folder, filename)
        with open(filename_path, 'w', encoding="utf8") as file:
            file.write(rendered_page)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Library creater (tululu.org)')
    parser.add_argument('--books', default=20, help='Books per page (default 20)')
    args = parser.parse_args()
    step = int(args.books)

    try:
        with open("books_description.json", "r") as my_file:
            books_description_json = my_file.read()
    except FileNotFoundError:
        print('File "books_description.json" does not exist')
        exit()

    books_description = json.loads(books_description_json)
    create_template(books_description, step)

    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')

