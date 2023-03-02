import database
import lib
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


def main(book_id: str):
    response = lib.get_html(f"http://www.kuaishuku.net/{book_id}/")
    book_name = response.xpath("/html/body/div[2]/div[1]/div/div[2]/div[2]/h1/text()").get()

    if response:
        book_info = {
            "book_id": book_id,
            "book_name": book_name,
            "book_author": response.xpath("/html/body/div[2]/div[1]/div/div[2]/div[2]/h3/a/text()").get(),
            "book_last_update_time": response.xpath(
                "/html/body/div[2]/div[1]/div/div[2]/div[2]/p[2]/font/text()").get(),
            "book_url": f"http://www.kuaishuku.net/{book_id}/",
            "book_cover": "http://www.kuaishuku.net" + response.xpath(
                "/html/body/div[2]/div[1]/div/div[2]/div[1]/img/@src").get(),
        }
        if database.database_book_info.get(book_id):
            database.database_book_info.update_many(book_id, book_info)
        else:
            database.database_book_info.insert(book_id, book_info)

        chapter_info_list = response.xpath("/html/body/div[2]/div[3]/div/div/div[2]/ul/li/a")
        par = tqdm(total=len(chapter_info_list.getall()), desc=book_name)

        # print(database_chapter_info.find_all())
        with ThreadPoolExecutor(max_workers=32) as executor:
            for index, chapter_info in enumerate(chapter_info_list):
                executor.submit(_thread_chap, par, book_id, index, chapter_info)

        # for index, chapter_info in enumerate(chapter_info_list):
        #     _thread_chap(par, book_id, index, chapter_info)
        par.close()

    database.database_book_info.save()
    database.database_chapter_info.save()


if __name__ == '__main__':

    import argparse

    main(str(1))
    # for i in range(1, 70000):
    #     main(str(i))

