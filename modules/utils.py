# https://pypdf.readthedocs.io/en/stable/index.html
from pathlib import Path
import re
import os
from pypdf import PdfWriter, PdfReader

PDF_PAGES_REGEX = re.compile(r"(^\d+-\d+$)|(^(\d,)+\d$)")


def parse_filepath(file_path: str) -> str:
    fp = Path(file_path)
    return fp.name.split(".")[0]


def parse_input_for_reduce(input_str: str) -> list:
    # for compression funcs
    return [i.strip().lower() for i in input_str.split()]


def parse_input_for_edit(input_str: str) -> dict:
    # for combine, delete & rearrange pdf (pages required)
    split_input = input_str.split()
    parsed_pdf_pages = {}
    for idx, val in enumerate(split_input):
        if not (match := re.search(PDF_PAGES_REGEX, val)) and (
                match1 := re.search(PDF_PAGES_REGEX, split_input[idx + 1])
        ):
            parsed_pdf_pages[val] = split_input[idx + 1]
        elif not (match := re.search(PDF_PAGES_REGEX, val)) and not (
                match1 := re.search(PDF_PAGES_REGEX, split_input[idx + 1])
        ):
            parsed_pdf_pages[val] = []
    return parsed_pdf_pages


def read(filepath: str):
    return PdfReader(filepath)


def write_pdf(filename: str, writer_obj: PdfWriter):
    if not os.path.isdir("../pdf_results"):
        os.mkdir("../pdf_results")

    with open(f"../pdf_results/{filename}.pdf", "wb") as f:
        writer_obj.write(f)


# combine pdfs
def combine(pdfs_pages: dict):
    """{pdf1: [1,3,4], pdf2: [4,5], pdf3:[], ...}"""

    writer = PdfWriter()

    for file, pages in pdfs_pages.items():
        pdf = read(file)
        if pages:
            for page in [i - 1 for i in pages]:
                writer.add_page(pdf.pages[page])
        else:
            for page in pdf.pages:
                writer.add_page(page)

    write_pdf(filename="combined", writer_obj=writer)


def delete(pdf_pages: dict):
    # delete pages (combine excluding the pages to be deleted)
    for file, pages in pdf_pages.items():
        writer = PdfWriter()
        pdf = read(file)
        for req_page in [
            p for p in pdf.pages if p.page_number not in [i - 1 for i in pages]
        ]:
            writer.add_page(req_page)

        write_pdf(
            filename=f"{parse_filepath(file)}_with_del_pages",
            writer_obj=writer,
        )


def rearrange(pdf_pages: dict):
    # rearrange pages (combine with the given order of pages)
    for file, pages in pdf_pages.items():
        writer = PdfWriter()
        pdf = read(file)
        req_page_idx = [i - 1 for i in pages]
        for idx in req_page_idx:
            writer.add_page(pdf.pages[idx])

        write_pdf(
            filename=f"{parse_filepath(file)}_rearranged", writer_obj=writer
        )


def compress(pdfs: list[str], level: int):
    # level [0-9]: 9 max
    # compress pdf
    # https://pypdf.readthedocs.io/en/stable/user/file-size.html
    for file in pdfs:
        pdf = read(file)
        writer = PdfWriter()
        for page in pdf.pages:
            writer.add_page(page)

        for page in writer.pages:
            page.compress_content_streams(level=level)

        write_pdf(
            filename=f"{parse_filepath(file)}_compressed", writer_obj=writer
        )


def img_compress(pdfs: list[str], quality: int):
    # compress images in pdf file
    # scale - quality [0-100]
    for file in pdfs:
        pdf = read(file)
        writer = PdfWriter()

        for page in pdf.pages:
            writer.add_page(page)

        for page in writer.pages:
            for img in page.images:
                img.replace(img.image, quality=quality)

        write_pdf(
            filename=f"{parse_filepath(file)}_img_compressed",
            writer_obj=writer,
        )
