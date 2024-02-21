from utils import (
    combine,
    delete,
    rearrange,
    compress,
    img_compress,
    parse_input_for_edit,
    parse_input_for_reduce)
import click

HANDLE_PDF = {
    'combine': combine,
    'delete': delete,
    'rearrange': rearrange,
    'compress': compress,
    'image-compress': img_compress
}


@click.command()
@click.argument('pdf_op')
@click.argument('pdf_data')
# @click.option('--level', help='compression level between 0 & 9 (max)', default=5, show_default=True)
# @click.option('--quality', type=click.IntRange(0, 100, clamp=True),
#               help='image quality between 0 & 100 (max)', default=50, show_default=True)
def handler(pdf_op: str, pdf_data: str, *args, **kwargs):
    match pdf_op := pdf_op.strip().lower():
        case 'compress':
            level = click.prompt("Required compression level (0-9 (max)): ",
                                 type=click.IntRange(0, 9, clamp=True))
            parsed_pdf_data = parse_input_for_reduce(input_str=pdf_data)
            HANDLE_PDF[pdf_op](parsed_pdf_data, level)

        case 'image-compress':
            quality = click.prompt("Required image quality level (0-100 (max)): ",
                                   type=click.IntRange(0, 100, clamp=True))
            parsed_pdf_data = parse_input_for_reduce(input_str=pdf_data)
            HANDLE_PDF[pdf_op](parsed_pdf_data, quality)

        case 'combine' | 'delete' | 'rearrange':
            parsed_pdf_data = parse_input_for_edit(input_str=pdf_data)
            HANDLE_PDF[pdf_op](parsed_pdf_data)


if __name__ == '__main__':
    handler()
