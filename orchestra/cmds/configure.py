from ..model.configuration import Configuration
from ..executor import Executor


def install_subcommand(sub_argparser):
    cmd_parser = sub_argparser.add_parser("configure", handler=handle_configure, help="Run configure script")
    cmd_parser.add_argument("component")
    cmd_parser.add_argument("--force", "-f", action="store_true", help="Force execution of the root action")


def handle_configure(args, config: Configuration):
    build = config.get_build(args.component)
    executor = Executor(args)
    executor.run(build.configure, force=args.force)
