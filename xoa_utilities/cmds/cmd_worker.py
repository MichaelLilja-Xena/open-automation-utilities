from __future__ import annotations
from asyncclick.shell_completion import ShellComplete, CompletionItem
from asyncclick import BaseCommand
import typing as t
from ..clicks import xoa_utils
from ..clicks import cmd_main
from ..hub import HubManager
from ..clis import ReadConfig, run_coroutine_as_sync, format_error
import asyncssh as ah
import asyncclick as ac
import os
from .cmd_context import CmdContext

if t.TYPE_CHECKING:
    from asyncssh.process import SSHServerProcess
    from asyncssh.editor import SSHLineEditorChannel


class AutoCompleter(ShellComplete):
    """
    Extends ShellComplete. https://click.palletsprojects.com/en/8.1.x/shell-completion/
    """

    def __init__(
        self,
        cli: BaseCommand,
        ctx_args: dict[str, t.Any],
        prog_name: str,
        complete_var: str,
        args_raw: list[str],
    ) -> None:
        super().__init__(cli, ctx_args, prog_name, complete_var)
        self.args_raw = args_raw

    def get_completion_args(self) -> tuple[list[str], str]:
        """Use the self.args to return a tuple of ``args, incomplete``."""
        args = self.args_raw[:-1] if self.args_raw else []
        incomplete = str(self.args_raw[-1]) if self.args_raw else ""
        return args, incomplete

    def format_completion(self, item: CompletionItem) -> str:
        """Format a completion item into the form recognized by the
        shell script.

        :param item: Completion item to format.
        """
        return f"{item.value}"

    async def complete(self) -> str:
        """Produce the completion data to send back to the shell.

        By default this calls :meth:`get_completion_args`, gets the
        completions, then calls :meth:`format_completion` for each
        completion.
        """
        args, incomplete = self.get_completion_args()
        completions = await self.get_completions(args, incomplete)
        out = [self.format_completion(item) for item in completions]
        return "\t".join(out)


async def shell_complete(cli: BaseCommand, args_raw: list[str]) -> str:
    """Perform shell completion for the given CLI program.
    Mimic of :func: asyncclick.shell_completion.shell_complete.

    :param cli: Command being called.

    :return: String after completion
    """
    prog_name = "xoa_utils"
    ctx_args = {}
    completer = AutoCompleter(cli, ctx_args, prog_name, "", args_raw)
    completed = await completer.complete()
    return completed


class CmdWorker:
    def __init__(
        self,
        process: "SSHServerProcess",
        base_prompt: str = "xoa_util",
    ) -> None:
        self.process: "SSHServerProcess" = process
        self.base_prompt: str = base_prompt
        self.channel: "SSHLineEditorChannel" = self.process.channel  # type: ignore
        self.hub_manager: t.Optional["HubManager"] = None
        self.hub_enable: bool = False
        self.hub_msg_list: list = []
        self.context = CmdContext()
        self.register_keys()

    def autocomplete(self, line: str, pos: int) -> t.Tuple[str, int]:
        if not line:
            return line, pos
        args_raw = line.split()
        coro = shell_complete(xoa_utils, args_raw)
        completed = str(run_coroutine_as_sync(coro))
        if not completed:
            pass
        elif completed.startswith("-"):
            self.write(f"{line}\n{completed}\n\n{self.make_prompt()}")
        elif args_raw and completed.startswith(args_raw[-1]):
            new_l = args_raw[:-1] + [completed]
            line = " ".join(new_l)
        else:
            line = completed
        pos = len(line)
        return line, pos

    def register_keys(self) -> None:
        self.channel.register_key("\t", self.autocomplete)

    def finish(self) -> None:
        self.process.exit(0)

    def write(self, msg: str) -> None:
        self.process.stdout.write(msg)

    def put_hub_record(self, request: str, response: str, success: bool) -> None:
        if self.hub_enable and self.hub_manager:
            self.hub_msg_list.append((os.getpid(), request, response, success))  # type: ignore

    def make_prompt(self) -> str:
        return self.context.prompt(self.base_prompt)

    async def run(self) -> None:
        self.connect_hub()
        self.write(f"\n{self.make_prompt()}")
        while not self.process.stdin.at_eof():
            response = None
            success = False
            try:
                request = (await self.process.stdin.readline()).strip()
                response = await self.dispatch(request)
                success = True
                if isinstance(response, int):
                    response = self.context.get_error()
                    success = False
            except ah.TerminalSizeChanged:
                pass
            except ah.BreakReceived:
                self.finish()
            except ac.UsageError as error:
                response = format_error(error)
                success = False
            except Exception as e:
                response = f"{type(e).__name__}: {e}\n"
                success = False
            if response is not None:
                self.write(f"{response}\n{self.make_prompt()}")
                self.put_hub_record(request, response, success)

    def connect_hub(self) -> None:
        config = ReadConfig()
        self.hub_enable = config.hub_enabled
        if config.hub_enabled:
            self.hub_manager = HubManager(
                address=(config.hub_host, config.hub_port), authkey=b""
            )
            self.hub_manager.connect()
            self.hub_msg_list = self.hub_manager.get_list()  # type: ignore

    async def dispatch(self, msg: str) -> str:
        if not msg:
            return ""
        if msg.lower() == "exit":
            await cmd_main(self.context, msg)
            self.finish()
            return ""
        return await cmd_main(self.context, msg)
