from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CommandResult:
    action: str
    command: list[str]
    returncode: int
    stdout: str
    stderr: str


class CommandNotAllowedError(ValueError):
    pass


class CommandExecutionError(RuntimeError):
    pass


class SafeSubprocessRunner:
    def __init__(self, project_root: Path, allowed_actions: dict[str, list[str]]) -> None:
        self.project_root = project_root.resolve()
        self.allowed_actions = allowed_actions

    def run(self, action: str, timeout_seconds: int = 600) -> CommandResult:
        if action not in self.allowed_actions:
            raise CommandNotAllowedError(f"Action not allowed: {action}")

        command = self.allowed_actions[action]

        if not command:
            raise CommandNotAllowedError(f"Empty command for action: {action}")

        if any(part.strip() == "" for part in command):
            raise CommandNotAllowedError(f"Invalid empty command part for action: {action}")

        if any(";" in part or "&&" in part or "|" in part for part in command):
            raise CommandNotAllowedError(f"Shell control operators are not allowed: {action}")

        result = subprocess.run(
            command,
            cwd=self.project_root,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )

        command_result = CommandResult(
            action=action,
            command=command,
            returncode=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
        )

        if result.returncode != 0:
            raise CommandExecutionError(
                f"Command failed for action={action}, returncode={result.returncode}\n"
                f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
            )

        return command_result
