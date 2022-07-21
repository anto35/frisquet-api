"""Command-line interface."""
import errno
from typing import Any, Dict
import click
import logging
import os
from datetime import datetime
from click.core import Context

import aiohttp

from . import helpers


_WARNING_DEBUG_ENABLED = (
    "Debug output enabled. Logs may contain personally identifiable "
    "information and account credentials! Be sure to sanitise these logs "
    "before sending them to a third party or posting them online."
)


def _check_for_debug(debug: bool, log: bool) -> None:
    if debug or log:
        frisquet_log = logging.getLogger("frisquet_api")
        frisquet_log.setLevel(logging.DEBUG)

        if log:
            # create directory
            try:
                os.makedirs("logs")
            except OSError as e:  # pragma: no cover
                if e.errno != errno.EEXIST:
                    raise

            # create formatter and add it to the handlers
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )

            # create file handler which logs even debug messages
            fh = logging.FileHandler(f"logs/{datetime.today():%Y-%m-%d}.log")
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(formatter)

            # And enable our own debug logging
            frisquet_log.addHandler(fh)

        if debug:
            logging.basicConfig()

        frisquet_log.warning(_WARNING_DEBUG_ENABLED)


@click.command()
@click.option("--debug", is_flag=True, help="Display debug traces.")
@click.option("--log", is_flag=True, help="Log debug traces to file.")
@click.version_option()
@click.pass_context
def main(ctx: Context,
    *,
    debug: bool,
    log: bool,) -> None:
    """Frisquet Api."""
    _check_for_debug(debug, log)

if __name__ == "__main__":
    main(prog_name="frisquet-api")  # pragma: no cover

@main.command()
@click.option("--user", prompt=True)
@click.option("--password", prompt=True, hide_input=True)
@click.pass_obj
@helpers.coro_with_websession
async def login(
    ctx_data: Dict[str, Any],
    *,
    user: str,
    password: str,
    websession: aiohttp.ClientSession,
) -> None:
    """Login to Renault."""
    await frisquet_client.login(websession, ctx_data, user, password)