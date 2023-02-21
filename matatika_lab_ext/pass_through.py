"""Passthrough shim for MatatikaLab extension."""
import sys

import structlog
from meltano.edk.logging import pass_through_logging_config
from matatika_lab_ext.extension import MatatikaLab


def pass_through_cli() -> None:
    """Pass through CLI entry point."""
    pass_through_logging_config()
    ext = MatatikaLab()
    ext.pass_through_invoker(
        structlog.getLogger("matatika-lab_invoker"),
        *sys.argv[1:] if len(sys.argv) > 1 else []
    )
