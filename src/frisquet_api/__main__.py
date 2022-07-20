"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Frisquet Api."""


if __name__ == "__main__":
    main(prog_name="frisquet-api")  # pragma: no cover
