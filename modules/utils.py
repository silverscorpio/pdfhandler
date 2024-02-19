import re
from pypdf import PdfWriter, PdfReader
from pprint import pprint

# constants
PDF_PATHS = [
    "../sample_pdfs/sample1.pdf",
    "../sample_pdfs/sample2.pdf",
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

    with open("../sample_pdfs/combined.pdf", "wb") as f:
        writer.write(f)


def delete():
    # delete pages (combine excluding the pages to be deleted)
    pass


def rearrange():
    # rearrange pages (combine with the given order of pages)
    pass


def compress():
    # compress pdf
    pass


def play():
    pdfs = [read(i) for i in PDF_PATHS]
    pdf = pdfs[1]
    print(pdf.pages)


if __name__ == "__main__":
    given_dict = {
        PDF_PATHS[0]: [],
        PDF_PATHS[1]: [2],
    }
    combine(pdfs_pages=given_dict)
