# https://pypdf.readthedocs.io/en/stable/index.html

import re
from pypdf import PdfWriter, PdfReader

# constants
PDF_PATHS = [
    "../sample_pdfs/projects.pdf",  # 10 pages
    "../sample_pdfs/internships.pdf",  # 9 pages

    # "../sample_pdfs/sample1.pdf",
    # "../sample_pdfs/sample2.pdf",
]
PDF_PAGES_REGEX = re.compile(r"(^\d+-\d+$)|(^(\d,)+\d$)")


# Pdf handling functions
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
    with open(f"./pdf_results/{filename}.pdf", "wb") as f:
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

    write_pdf(filename='combined', writer_obj=writer)


def delete(pdf_pages: dict):
    # delete pages (combine excluding the pages to be deleted)
    for file, pages in pdf_pages.items():
        writer = PdfWriter()
        pdf = read(file)
        for req_page in [p for p in pdf.pages if p not in pages]:
            writer.add_page(req_page)

        write_pdf(filename=f"{file}_with_del_pages.pdf", writer_obj=writer)


def rearrange(pdf_pages: dict):
    # rearrange pages (combine with the given order of pages)
    for file, pages in pdf_pages.items():
        writer = PdfWriter()
        pdf = read(file)
        req_page_idx = [i - 1 for i in pages]
        for idx in req_page_idx:
            writer.add_page(pdf.pages[idx])

        write_pdf(filename=f"{file}_rearranged.pdf", writer_obj=writer)


def compress(pdfs: list[str], level: int):
    # compress pdf
    for file in pdfs:
        pdf = read(file)
        writer = PdfWriter()
        for page in pdf.pages:
            writer.add_page(page)

        for page in writer.pages:
            page.compress_content_streams(level=level)

        write_pdf(filename=f"{pdf}_compressed.pdf", writer_obj=writer)


if __name__ == "__main__":
    pdf_pages_dict = {
        PDF_PATHS[0]: [],
        PDF_PATHS[1]: [2],
    }
