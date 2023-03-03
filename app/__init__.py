import lib
import models


def get_book_info_by_book_id(book_id: str) -> models.BookInfo:
    url = f"http://www.kuaishuku.net/{book_id}/"
    response = lib.get_html(url)
    if response:
        return models.BookInfo(
            book_id=book_id,
            book_name=response.xpath("/html/body/div[2]/div[1]/div/div[2]/div[2]/h1/text()").get(),
            book_author=response.xpath("/html/body/div[2]/div[1]/div/div[2]/div[2]/h3/a/text()").get(),
            book_last_time=response.xpath("/html/body/div[2]/div[1]/div/div[2]/div[2]/p[2]/font/text()").get(),
            book_url=url,
            book_cover=response.xpath("/html/body/div[2]/div[1]/div/div[2]/div[1]/img/@src").get(),
            chapter_info_list=response.xpath("/html/body/div[2]/div[3]/div/div/div[2]/ul/li/a")
        )




def get_book_info_by_book_name(book_name: str) :
    url = f"https://www.kuaishuku.net/search.php?searchkey={book_name}"
    response = lib.get_html(url)
    if response:
        book_info_list = response.xpath("/html/body/div[1]/div/div[2]/table/tbody/tr/td[2]/div/a")
        print(book_info_list.getall())
