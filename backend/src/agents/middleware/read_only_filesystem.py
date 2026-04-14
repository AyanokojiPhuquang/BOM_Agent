"""Read-only filesystem middleware.

Subclass of FilesystemMiddleware that only exposes read tools:
ls, read_file, glob, grep. Write/edit/execute tools are excluded.
"""

from deepagents.middleware.filesystem import FilesystemMiddleware


class ReadOnlyFilesystemMiddleware(FilesystemMiddleware):
    """Filesystem middleware restricted to read-only tools."""

    READ_ONLY_TOOLS = frozenset({"ls", "read_file", "glob", "grep"})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tools = [t for t in self.tools if t.name in self.READ_ONLY_TOOLS]
