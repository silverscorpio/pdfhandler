## PDF Handler

_Allows local handling of PDF files_

---

- CLI utility
- Born out of necessity after facing issues with personal documents when no net access was available
- Most used PDF operations were given priority
    - combine/merge
    - delete page
    - rearrange based on the given order of pages
    - compress pdf (compression level can be adjusted)
    - image compression in pdf (compression level can be controlled)
- Stack - Python, pypdf, Click, poetry, ruff
- Plan to expand further - integration with another Django project