import pydantic

from typing import List, Optional


class BookInfo(pydantic.BaseModel):  # type: ignore
    book_id: Optional[str]
    book_name: Optional[str]
    book_author: Optional[str]
    book_last_update_time: Optional[str]
    book_url: Optional[str]
    book_cover: Optional[str]

    class Config:
        orm_mode = True



