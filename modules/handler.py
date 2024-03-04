from utils import (
    combine,
    delete,
    rearrange,
    compress,
    img_compress,
)
import click

HANDLE_PDF = {
    "combine": combine,
    "delete": delete,
    "rearrange": rearrange,
    "compress": compress,
    "image-compress": img_compress,
}


# TODO individual pdfs with pages - change parsers, range of pages, check if file exists

@click.command()
@click.argument("pdf_operation")
@click.argument("pdf_data", type=click.Path(dir_okay=False), nargs=-1)
def handler(pdf_operation: str, pdf_data):
    click.echo(pdf_operation)
    click.echo(pdf_data)
    # match pdf_operation := pdf_operation.strip().lower():
    #     case "compress":
    #         parsed_pdf_data = parse_input_for_reduce(input_str=pdf_data)
    #         compression_level = click.prompt(
    #             "Required compression level [0-9 (max)]: ",
    #             type=click.IntRange(0, 9, clamp=True),
    #         )
    #         HANDLE_PDF[pdf_operation](parsed_pdf_data, compression_level)
    #
    #     case "image-compress":
    #         parsed_pdf_data = parse_input_for_reduce(input_str=pdf_data)
    #         image_quality = click.prompt(
    #             "Required image quality level [0-100 (max)]: ",
    #             type=click.IntRange(0, 100, clamp=True),
    #         )
    #
    #         HANDLE_PDF[pdf_operation](parsed_pdf_data, image_quality)
    #
    #     case "combine" | "delete" | "rearrange":
    #         parsed_pdf_data = parse_input_for_edit(input_str=pdf_data)
    #         HANDLE_PDF[pdf_operation](parsed_pdf_data)
    #
    #     case _:
    #         raise click.BadParameter(
    #             f"Unknown PDF operation: '{pdf_operation}'"
    #         )


if __name__ == "__main__":
    handler()
