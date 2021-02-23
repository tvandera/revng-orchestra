import argparse

from . import CustomArgumentParser
from . import clean
from . import clone
from . import components
from . import configure
from . import dumpconfig
from . import environment
from . import fix_binary_archives_symlinks
from . import graph
from . import install
from . import ls
from . import shell
from . import uninstall
from . import update
from . import upgrade
from . import binary_archives


main_parser = argparse.ArgumentParser()
logging_group = main_parser.add_argument_group(title="Logging options")
logging_group.add_argument("--loglevel", "-v", default="INFO",
                           choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])

config_group = main_parser.add_argument_group(title="Configuration options")
config_group.add_argument("--no-config-cache", dest="config_cache", default=True, action="store_false",
                          help="Do not cache generated yaml configuration")

main_subparsers = main_parser.add_subparsers(
    description="Available subcommands. Use <subcommand> --help",
    dest="command_name",
    parser_class=CustomArgumentParser,
    metavar="<subcommand>"
)

subcommands = [
    components,
    environment,
    clone,
    configure,
    install,
    uninstall,
    clean,
    update,
    upgrade,
    graph,
    shell,
    ls,
    fix_binary_archives_symlinks,
    dumpconfig,
    binary_archives
]

for cmd in subcommands:
    cmd.install_subcommand(main_subparsers)
