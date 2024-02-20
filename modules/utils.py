# https://pypdf.readthedocs.io/en/stable/index.html
from pathlib import Path
import re
import os
from pypdf import PdfWriter, PdfReader

# constants
PDF_PATHS = [
    "../sample_pdfs/projects.pdf",  # 10 pages
    "../sample_pdfs/internships.pdf",  # 9 pages

    # "../sample_pdfs/sample1.pdf",
    # "../sample_pdfs/sample2.pdf",
]
PDF_PAGES_REGEX = re.compile(r"(^\d+-\d+$)|(^(\d,)+\d$)")


def parse_filepath(file_path: str) -> str:
    fp = Path(file_path)
    return fp.name.split(".")[0]


def parse_input(input_str: str) -> dict:
    # without '&' between pdf-pages pair
    split_input = input_str.split()
    parsed_pdf_pages = {}
    for idx, val in enumerate(split_input):
        if not (match := re.search(PDF_PAGES_REGEX, val)) and (
                match1 := re.search(PDF_PAGES_REGEX, split_input[idx + 1])):
            parsed_pdf_pages[val] = split_input[idx + 1]
        elif not (match := re.search(PDF_PAGES_REGEX, val)) and not (
                match1 := re.search(PDF_PAGES_REGEX, split_input[idx + 1])):
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
    """ {pdf1: [1,3,4], pdf2: [4,5], pdf3:[], ...} """

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
        for req_page in [p for p in pdf.pages if p not in pages]:
            writer.add_page(req_page)

        write_pdf(filename=f"{parse_filepath(file)}_with_del_pages", writer_obj=writer)


def rearrange(pdf_pages: dict):
    # rearrange pages (combine with the given order of pages)
    for file, pages in pdf_pages.items():
        writer = PdfWriter()
        pdf = read(file)
        req_page_idx = [i - 1 for i in pages]
        for idx in req_page_idx:
            writer.add_page(pdf.pages[idx])

        write_pdf(filename=f"{parse_filepath(file)}_rearranged", writer_obj=writer)


def compress(pdfs: list[str], level: int):
    # compress pdf
    # https://pypdf.readthedocs.io/en/stable/user/file-size.html
    for file in pdfs:
        pdf = read(file)
        writer = PdfWriter()
        for page in pdf.pages:
            writer.add_page(page)

        for page in writer.pages:
            page.compress_content_streams(level=level)

        write_pdf(filename=f"{parse_filepath(file)}_compressed", writer_obj=writer)


if __name__ == "__main__":
    pdf_pages_dict = {
        PDF_PATHS[0]: [8, 9],  # projects
        PDF_PATHS[1]: [6, 7],  # internships
    }

    # combine(pdfs_pages=pdf_pages_dict)
    delete(pdf_pages=pdf_pages_dict)
