import pydantic

from typing import List, Optional, Any

class BookInfo(pydantic.BaseModel):
    book_id: Optional[str]
    book_name: Optional[str]
    book_author: Optional[str]
    book_last_update_time: Optional[str]
    book_url: Optional[str]
    book_cover: Optional[str]
    chapter_info_list:  Any = None

    # class Config:
    #     orm_mode = True
