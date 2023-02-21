"""Meltano MatatikaLab extension."""
from __future__ import annotations

import os
import pkgutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import structlog
from meltano.edk import models
from meltano.edk.extension import ExtensionBase
from meltano.edk.process import Invoker, log_subprocess_error

log = structlog.get_logger()


class MatatikaLab(ExtensionBase):
    """Extension implementing the ExtensionBase interface."""

    def __init__(self) -> None:
        """Initialize the extension."""
        self.matatika_lab_invoker = Invoker("docker")

    def invoke(self, command_name: str | None, *command_args: Any) -> None:
        """Invoke the underlying cli, that is being wrapped by this extension.

        Args:
            command_name: The name of the command to invoke.
            command_args: The arguments to pass to the command.
        """
        try:
            self.matatika_lab_invoker.run_and_log(command_name, *command_args)
        except subprocess.CalledProcessError as err:
            log_subprocess_error(
                f"matatika-lab {command_name}", err, "MatatikaLab invocation failed"
            )
            sys.exit(err.returncode)

    def describe(self) -> models.Describe:
        """Describe the extension.

        Returns:
            The extension description
        """
        # TODO: could we auto-generate all or portions of this from typer instead?
        return models.Describe(
            commands=[
                models.ExtensionCommand(
                    name="matatika-lab_extension", description="extension commands"
                ),
                models.InvokerCommand(
                    name="matatika-lab_invoker", description="pass through invoker"
                ),
            ]
        )
