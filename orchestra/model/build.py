import os.path

from ..actions import CloneAction
from ..actions import ConfigureAction
from ..actions import InstallAction
from . import component
from ..actions.util import run_script


class Build:
    def __init__(
            self,
            name: str,
            comp: component.Component,
            ndebug=True,
            test=False,
    ):
        self.name = name
        self.component = comp
        self.self_hash = None
        self.recursive_hash = None

        self.configure: ConfigureAction = None
        self.install: InstallAction = None

        self.ndebug = ndebug
        self.test = test

    @property
    def qualified_name(self):
        return f"{self.component.name}@{self.name}"

    @property
    def safe_name(self):
        return self.qualified_name.replace("@", "_").replace("/", "_")

    @property
    def binary_archive_dir(self):
        """Returns the relative dirname where the binary archives should be created/found."""
        return os.path.join(self.component.name, self.name)

    @property
    def binary_archive_filename(self):
        """Returns the filename of the binary archive. Remember to os.path.join it with binary_archive_dir!"""
        component_commit = self.component.commit() or "none"
        return f'{component_commit}_{self.recursive_hash}.tar.gz'

    def __str__(self):
        return f"Build {self.component.name}@{self.name}"

    def __repr__(self):
        return f"Build {self.component.name}@{self.name}"
