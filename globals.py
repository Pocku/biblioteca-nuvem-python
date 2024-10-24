from enum import StrEnum

DATE_FORMAT = "%d/%m/%y"

class BookStatus(StrEnum):
    DISPONIVEL = "disponivel"
    EMPRESTADO = "emprestado"

current_book_id = None