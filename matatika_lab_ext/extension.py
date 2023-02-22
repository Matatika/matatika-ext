"""Meltano MatatikaLab extension."""
from __future__ import annotations

import os
import pkgutil
import shutil
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

    def initialize(self, force: bool = False) -> None:
        def validate_for_copy(src: Path, dst: Path) -> tuple[bool, str]:
            # __pycache__ specified here for editable install only, otherwise covered
            # by exclude in pyproject.toml
            if src.name in ("__pycache__", "__init__.py"):
                return False, "blacklisted file name"

            if not force and dst.is_file():
                return False, "file already exists"

            return True, "forced update" if force and dst.exists() else ""

        def copy(src: Path, dst=Path(".")):
            for file in src.iterdir():
                dst_file = dst / file.name
                copyable, reason = validate_for_copy(file, dst_file)

                if not copyable:
                    log.debug(f"Skipping {dst_file} ({reason})")
                    continue

                if file.is_file():
                    dst.mkdir(parents=True, exist_ok=True)
                    shutil.copy(file, dst_file)

                    log.info(f"Copied {dst_file}{f' ({reason})' if reason else ''}")
                else:
                    copy(file, dst_file)

        copy(ir_files("files_matatika_lab_ext"))
