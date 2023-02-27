"""Meltano Matatika extension."""
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

try:
    from importlib.resources import files as ir_files
except ImportError:
    from importlib_resources import files as ir_files

COMPOSE_FILE: Path = ir_files("files_matatika_ext").joinpath("docker-compose.yml")

log = structlog.get_logger()


class SubcommandInvoker(Invoker):
    """Invoker to set an alternate subcommand entrypoint."""

    def __init__(self, bin: str, *subcommands: str, env: dict[str, Any] = None):
        super().__init__(bin, env=env)
        self.subcommands = subcommands

    def run(self, *args, **kwargs):
        args = self.subcommands + args
        return super().run(*args, **kwargs)

    def run_and_log(self, sub_command: str | None = None, *args, **kwargs):
        args = self.subcommands + args
        return super().run_and_log(sub_command, *args, **kwargs)


class Matatika(ExtensionBase):
    """Extension implementing the ExtensionBase interface."""

    def __init__(self) -> None:
        """Initialize the extension."""
        env = {
            "COMPOSE_FILE": COMPOSE_FILE,
            "COMPOSE_PROJECT_NAME": Path.cwd().name,
            **os.environ,
        }

        # prefer Compose V2
        self.matatika_invoker = SubcommandInvoker("docker", "compose", env=env)

        try:
            self.matatika_invoker.run("version")
        except subprocess.CalledProcessError:
            self.matatika_invoker = Invoker("docker-compose", env=env)

    def invoke(self, command_name: str | None, *command_args: Any) -> None:
        """Invoke the underlying cli, that is being wrapped by this extension.

        Args:
            command_name: The name of the command to invoke.
            command_args: The arguments to pass to the command.
        """
        try:
            self.matatika_invoker.run_and_log(command_name, *command_args)
        except subprocess.CalledProcessError as err:
            log_subprocess_error(
                f"matatika {command_name}", err, "Matatika invocation failed"
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
                    name="matatika_extension", description="extension commands"
                ),
                models.InvokerCommand(
                    name="matatika_invoker", description="pass through invoker"
                ),
            ]
        )
