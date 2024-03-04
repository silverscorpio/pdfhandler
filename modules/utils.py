# https://pypdf.readthedocs.io/en/stable/index.html
import sys
from pathlib import Path
import os

import click
from pypdf import PdfWriter, PdfReader


def read(filepath: str):
    try:
        pdf = PdfReader(filepath)
    except FileNotFoundError:
        print(f"{filepath} not found")
        sys.exit()
    else:
        return pdf


def get_filename(file_path: str) -> str:
    fp = Path(file_path)
    return fp.name.split(".")[0]


def parse_input_for_reduce(input_str: str) -> list:
    # for compression funcs
    return [i.strip().lower() for i in input_str.split()]


def write_pdf(filename: str, writer_obj: PdfWriter):
    # generate in a dir in the current dir (main.py)
    if not os.path.isdir("./pdf_results"):
        os.mkdir("./pdf_results")

    with open(f"./pdf_results/{filename}.pdf", "wb") as f:
        writer_obj.write(f)


def prompt_compress_level(prompt_text: str, min_val: int, max_val: int, default_val: int, clamp: bool = True) -> int:
    return click.prompt(
        prompt_text,
        type=click.IntRange(min_val, max_val, clamp=clamp),
        default=default_val,
    )


def pages_parser(pages: str) -> list[int]:
    # for combine, delete, rearrange ops
    final_pages = []
    indiv_pages = [i.strip() for i in pages.split(',')]
    for i in indiv_pages:
        if '-' not in i:
            final_pages.append(int(i))
        else:
            num_range = [int(i) for i in i.split('-')]
            final_pages.extend(range(num_range[0], num_range[1] + 1))

    return final_pages


def parser(input_data: tuple[str]) -> dict:
    # CLI ('a.pdf 1,2', 'b.pdf 4,5,6, 8-19', 'c.pdf', 'd.pdf 4-10')
    data = {}
    for i in input_data:
        split_data: list[str] = i.split(maxsplit=1)
        if len(split_data) == 1:
            data[split_data[0].strip().lower()] = []
        else:
            data[split_data[0].strip().lower()] = pages_parser(pages=split_data[1])

    return data


# combine pdfs
def combine(raw_data: tuple[str]):
    """{pdf1: [1,3,4], pdf2: [4,5], pdf3:[], ...}"""
    parsed_data = parser(input_data=raw_data)
    writer = PdfWriter()

    for file, pages in parsed_data.items():
        pages = sorted(pages)
        pdf = read(file)
        if pages:
            for page in [i - 1 for i in pages]:
                writer.add_page(pdf.pages[page])
        else:
            for page in pdf.pages:
                writer.add_page(page)

    write_pdf(filename="combined", writer_obj=writer)


# delete pages from pdfs
def delete_pages(raw_data: tuple[str]):
    # delete pages (combine excluding the pages to be deleted)
    parsed_data = parser(input_data=raw_data)
    for file, pages in parsed_data.items():
        pages = sorted(pages)
        writer = PdfWriter()
        pdf = read(file)
        for req_page in [
            p for p in pdf.pages if p.page_number not in [i - 1 for i in pages]
        ]:
            writer.add_page(req_page)

        write_pdf(
            filename=f"{get_filename(file)}_with_del_pages",
            writer_obj=writer,
        )


# rearrange pdfs (pages)
def rearrange(raw_data: tuple[str]):
    # rearrange pages (combine with the given order of pages)
    # preferable for small rearrangement - GUI best
    parsed_data = parser(input_data=raw_data)
    for file, pages in parsed_data.items():
        writer = PdfWriter()
        pdf = read(file)
        req_page_idx = [i - 1 for i in pages]
        for idx in req_page_idx:
            writer.add_page(pdf.pages[idx])

        write_pdf(
            filename=f"{get_filename(file)}_rearranged", writer_obj=writer
        )


# compress pdf
def compress(pdf_file: str, def_level: int = 5):
    # level [0-9]: 9 max
    # compress pdf
    # https://pypdf.readthedocs.io/en/stable/user/file-size.html
    pdf = read(pdf_file)
    writer = PdfWriter()
    for page in pdf.pages:
        writer.add_page(page)

    for page in writer.pages:
        page.compress_content_streams(level=def_level)

    write_pdf(
        filename=f"{get_filename(pdf_file)}_compressed", writer_obj=writer
    )


# compress images in pdfs
def pdf_img_compress(pdf_file: str, def_quality: int = 50):
    # compress images in pdf file
    # scale - quality [0-100]
    pdf = read(pdf_file)
    writer = PdfWriter()

    for page in pdf.pages:
        writer.add_page(page)

    for page in writer.pages:
        for img in page.images:
            img.replace(img.image, quality=def_quality)

    write_pdf(
        filename=f"{get_filename(pdf_file)}_img_compressed",
        writer_obj=writer,
    )
