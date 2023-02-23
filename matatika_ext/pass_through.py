"""Passthrough shim for Matatika extension."""
import sys

import structlog
from matatika_ext.extension import Matatika
from meltano.edk.logging import pass_through_logging_config


def pass_through_cli() -> None:
    """Pass through CLI entry point."""
    pass_through_logging_config()
    ext = Matatika()
    ext.pass_through_invoker(
        structlog.getLogger("matatika_invoker"),
        *sys.argv[1:] if len(sys.argv) > 1 else []
    )
