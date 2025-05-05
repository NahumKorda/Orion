import pymupdf4llm


def get_text(file_path: str) -> str:
    return pymupdf4llm.to_markdown(file_path, margins=(0, 0))
