from modules.utils import (
    parser,
    combine,
    delete_pages,
    rearrange,
    compress,
    pdf_img_compress,
    prompt_compress_level,

)
import click

HANDLE_PDF = {
    "combine": combine,
    "delete": delete_pages,
    "rearrange": rearrange,
    "compress": compress,
    "image-compress": pdf_img_compress,
}


@click.command()
@click.argument("pdf_operation")
@click.argument("data", type=click.Path(dir_okay=False), nargs=-1)
def handler(pdf_operation: str, data):
    # click.echo(pdf_operation)
    # click.echo(data)
    match pdf_operation:
        case "compress":
            compression_level = prompt_compress_level(
                "Required pdf compression level [0-9 (max)], default=5: ",
                0,
                9)

            given_pdf = data.strip().lower()
            HANDLE_PDF[pdf_operation](given_pdf, compression_level)

        case "image-compress":
            image_quality = prompt_compress_level(
                "Required image quality level [0-100 (max)], default=50: ",
                0,
                100)

            given_pdf = data.strip().lower()
            HANDLE_PDF[pdf_operation](given_pdf, image_quality)

        case "combine" | "delete" | "rearrange":
            HANDLE_PDF[pdf_operation](raw_data=data)

        case _:
            raise click.BadParameter(
                f"Unknown PDF operation: '{pdf_operation}'"
            )


if __name__ == "__main__":
    handler()
