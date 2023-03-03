import app
import lib
import models

import argparse
import database
from tqdm import tqdm
from rich import print
from concurrent.futures import ThreadPoolExecutor


def _thread_chap(par, book_id, index, chapter_info):
    chapter_id = chapter_info.xpath("./@href").get()
    try:
        if database.database_chapter_info.get(chapter_id.replace(".html", "")):
            print("已存在", chapter_info.xpath("./text()").get())
        else:
            response = lib.get_html("http://www.kuaishuku.net" + chapter_id)
            if response:
                chapter_content = response.xpath("/html/body/div[2]/div[1]/div/div[2]/div[3]/div[2]/text()").getall()
                database.database_chapter_info.insert(chapter_id.replace(".html", ""), {
                    "book_id": book_id,
                    "chapter_index": index,
                    "chapter_id": chapter_id,
                    "chapter_name": chapter_info.xpath("./text()").get(),
                    "chapter_content": '\n'.join(chapter_content),
                })

                # database.database_chapter_info.save()

    finally:
        par.update(1)


def current_download_book(book_id: str):
    book_info = app.get_book_info_by_book_id(book_id)  # type: models.BookInfo
    if book_info:
        if database.database_book_info.get(book_info.book_id):
            database.database_book_info.update_many(book_info.book_id, book_info.dict())
        else:
            database.database_book_info.insert(book_info.book_id, book_info.dict())

        par = tqdm(total=len(book_info.chapter_info_list.getall()), desc=book_info.book_name)

        with ThreadPoolExecutor(max_workers=32) as executor:
            for index, chapter_info in enumerate(book_info.chapter_info_list):
                executor.submit(_thread_chap, par, book_info.book_id, index, chapter_info)

        par.close()
        database.database_book_info.save()
        database.database_chapter_info.save()

def current_download_search_book(book_name: str):
    app.get_book_info_by_book_name(book_name)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--download", nargs="?", help="download book")
    parser.add_argument("-u", "--update", nargs="?", help="update book")
    parser.add_argument("-s", "--search", nargs="?", help="search book")

    args = parser.parse_args()

    if args.download:
        current_download_book(args.download)
    elif args.update:
        pass
    elif args.search:
        current_download_search_book(args.search)
    else:
        parser.print_help()
