"""ANSI color codes for CLI terminal output.

Auto-disables when stdout is not a TTY.
"""

import sys


class C:
    """ANSI color codes for terminal output."""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # Foreground
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    RED = "\033[31m"
    GRAY = "\033[90m"

    # Styled labels
    AGENT = "\033[1;32m"  # bold green
    TOOL_CALL = "\033[1;33m"  # bold yellow
    TOOL_RESULT = "\033[36m"  # cyan
    USAGE = "\033[90m"  # gray
    BANNER = "\033[1;34m"  # bold blue
    ERROR = "\033[1;31m"  # bold red
    THINKING = "\033[2;35m"  # dim magenta

    @classmethod
    def disable(cls):
        """Clear all color codes (for non-TTY output)."""
        for attr in dir(cls):
            if attr.isupper() and not attr.startswith("_"):
                setattr(cls, attr, "")

    @classmethod
    def init(cls):
        """Disable colors if stdout is not a TTY."""
        if not sys.stdout.isatty():
            cls.disable()


C.init()
