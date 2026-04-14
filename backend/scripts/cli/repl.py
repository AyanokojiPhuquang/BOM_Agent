"""Shared REPL helpers for the Starlink agent CLI.

Provides read_user_input, handle_command, and print_banner.
"""

import os

from scripts.cli.colors import C


def read_user_input() -> str | None:
    """Prompt and read one line; returns None on EOF/Ctrl-C."""
    try:
        return input("You: ")
    except (EOFError, KeyboardInterrupt):
        return None


def handle_command(command: str, state: dict) -> bool:
    """Process slash commands. Returns True if the input was a command."""
    parts = command.strip().split(maxsplit=1)
    cmd = parts[0].lower()

    if cmd in ("/exit", "/quit"):
        state["running"] = False
        return True

    if cmd == "/help":
        _print_help()
        return True

    if cmd == "/new":
        on_new = state.get("on_new_session")
        if on_new:
            on_new(state)
        return True

    if cmd == "/clear":
        os.system("clear" if os.name != "nt" else "cls")
        return True

    return False


def print_banner(
    title: str,
    streaming: bool,
    extra_lines: list[str] | None = None,
) -> None:
    """Print the startup banner."""
    b, r, d = C.BANNER, C.RESET, C.DIM
    print()
    print(f"{b}{'=' * 60}{r}")
    print(f"{b}  {title}{r}")
    print(f"{b}{'=' * 60}{r}")
    for line in extra_lines or []:
        print(line)
    print(f"  Agent:       {C.GREEN}bom_assistant{r}")
    print(f"  Streaming:   {_on_off(streaming)}")
    print()
    print(f"  {d}Commands:{r}")
    print(f"  {d}  /help  /new  /clear  /exit{r}")
    print(f"{b}{'=' * 60}{r}")
    print()


# -- Private helpers ----------------------------------------------------------


def _on_off(flag: bool) -> str:
    color = C.GREEN if flag else C.YELLOW
    return f"{color}{'ON' if flag else 'OFF'}{C.RESET}"


def _print_help() -> None:
    print()
    print("  Commands:")
    print("    /help          Show this help")
    print("    /new           Reset conversation history")
    print("    /clear         Clear terminal")
    print("    /exit          Exit CLI")
    print()
