## PDF Modules brief comparison (analysis) (Python)

* Desktop app
* function-based
* common functionality
* modules (popular) - pypdf (pdfly for CLI apps), pymupdf, pdfminer

### Functions

- pdfhandler (prio based on use-cases)
    - convert to pdf (word. txt)
    - pages delete (edit pdf) (2)
    - rearrange pages (edit pdf) (3)
    - combine pdfs (1)
    - compress pdfs (4)
    - unlock pdf
    - read pdf (extract contents)

#### primary (rest later)

- combine pdfs (1)
- pages delete (edit pdf) (2)
- rearrange pages (edit pdf) (3)
- compress pdfs (4)

### Detailed info for each function

#### combine pdfs (many)

- pages
    - end-to-end
    - some specific individual pages (eg. 1,6,8)
    - page range (3-6, 9-10)
- two files or even more
- before combining, show the starting few words
- confirm and perform
- summary

#### delete pages from pdf (one)

- pages
    - some specific individual pages (eg. 1,6,8)
    - page range (3-6, 9-10)
- before deleting, show the starting few words
- confirm and perform
- summary
-

#### rearrange pages of pdf (one)

- pages
    - array of page numbers
- before finalizing, show the starting few words
- confirm and perform
- summary
-

#### compress pdfs (many)

- take in as many files
- compress (_maybe different algos?_)
- summary

### Common utils

* summary of operation/report generation
* show confirmatory starting content of each page and confirm
* saving as pdf/writing to a pdf file (after rearranging, deleting, combining, compressing)
