import argparse
import os
import shlex
from textwrap import dedent

from loguru import logger
from orchestra.util import export_environment

from . import SubCommandParser
from ..actions.util import get_script_output
from ..actions.util.impl import _run_script
from ..model.configuration import Configuration


def install_subcommand(sub_argparser: SubCommandParser):
    cmd_parser = sub_argparser.add_subcmd(
        "shell",
        handler=handle_shell,
        help="Open a shell with orchestra environment (experimental).",
    )
    cmd_parser.add_argument(
        "--component",
        "-c",
        help="Execute in the context of this component. "
        "The shell will start in the component build directory, if it exists. "
        "Otherwise, the CWD will not be changed.",
    )
    cmd_parser.add_argument("command", nargs=argparse.REMAINDER)

    cmd_parser = sub_argparser.add_subcmd(
        "env",
        handler=handle_env,
        help="Print environment variables needed to execute a command for component.",
    )
    cmd_parser.add_argument(
        "--component",
        "-c",
        help="Component name",
    )

def get_script_and_env(args):
    config = Configuration(use_config_cache=args.config_cache)

    if not args.component:
        env = config.global_env()
        ps1_prefix = "(orchestra) "
        cd_to = os.getcwd()
    else:
        build = config.get_build(args.component)
        if not build:
            suggested_component_name = config.get_suggested_component_name(args.component)
            logger.error(f"Component {args.component} not found! Did you mean {suggested_component_name}?")
            return 1

        env = build.install.environment
        ps1_prefix = f"(orchestra - {build.qualified_name}) "
        if os.path.exists(build.install.environment["BUILD_DIR"]):
            cd_to = build.install.environment["BUILD_DIR"]
        else:
            cd_to = os.getcwd()

    return env, cd_to

def handle_shell(args):
    env, cd_to = get_script_and_env(args)

    command = args.command
    if command:
        script_to_run = " ".join(shlex.quote(c) for c in command)
    else:
        user_shell = get_script_output("getent passwd $(whoami) | cut -d: -f7").strip()

        env["OLD_HOME"] = os.environ["HOME"]
        env["HOME"] = os.path.join(os.path.dirname(__file__), "..", "support", "shell-home")
        env["PS1_PREFIX"] = ps1_prefix
        script_to_run = dedent(f"exec {user_shell}")

    result = _run_script(script_to_run, environment=env, loglevel="DEBUG", cwd=cd_to)
    return result.returncode

def handle_env(args):
    env, _ = get_script_and_env(args)
    print(export_environment(env))
    return 0