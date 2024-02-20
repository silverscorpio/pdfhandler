from utils import combine, delete, rearrange, compress, img_compress, parse_input
import click


@click.command()
@click.argument('operation')
@click.argument('pdf_data')
def main(operation, pdf_data):
    click.echo(operation)
    click.echo(pdf_data)


if __name__ == '__main__':
    main()
