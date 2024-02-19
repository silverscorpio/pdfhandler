import re

from pypdf import PdfWriter, PdfReader
from pprint import pprint
import re

PDF_PATHS = [
    "../sample_pdfs/sample1.pdf",
    "../sample_pdfs/sample2.pdf",
]

REGEX = re.compile(r"(^\d+-\d+$)|(^(\d,)+\d$)")


# for idx, val in enumerate(w):
#     if not (match := re.search(ex, val)) and (match1:= re.search(ex, w[idx+1])):
#         stuff[val] = w[idx+1]
#     elif not (match := re.search(ex, val)) and not (match1:= re.search(ex, w[idx+1])):
#         stuff[val] = []

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


def play():
    pdfs = [read(i) for i in PDF_PATHS]
    pdf = pdfs[1]
    print(pdf.pages)


# delete pages (combine excluding the pages to be deleted)
# rearrange pages (combine with the given order of pages)
# compress pdf


if __name__ == "__main__":
    given_dict = {
        PDF_PATHS[0]: [],
        PDF_PATHS[1]: [2],
    }
    combine(pdfs_pages=given_dict)
