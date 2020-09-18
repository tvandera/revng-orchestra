import os.path
import subprocess
from glob import glob

from loguru import logger

from ..model.configuration import Configuration


def install_subcommand(sub_argparser):
    cmd_parser = sub_argparser.add_parser("update", handler=handle_update)


def handle_update(args, config: Configuration):
    logger.info("Updating binary archives")
    os.makedirs(config.binary_archives_dir, exist_ok=True)
    for name, url in config.binary_archives_remotes.items():
        binary_archive_path = os.path.join(config.binary_archives_dir, name)
        if os.path.exists(binary_archive_path):
            pull_binary_archive(name, config)
        else:
            clone_binary_archive(name, url, config)

    logger.info("Updating repositories")
    for git_repo in glob(os.path.join(config.sources_dir, "**/.git"), recursive=True):
        git_repo = os.path.dirname(git_repo)
        logger.info(f"Pulling {git_repo}")
        result = git_pull(git_repo)
        if result.returncode:
            logger.error(f"Could not pull repository {git_repo}")


def pull_binary_archive(name, config):
    binary_archive_path = os.path.join(config.binary_archives_dir, name)
    logger.info(f"Pulling binary archive {binary_archive_path}")
    result = git_pull(binary_archive_path)
    if result.returncode:
        logger.error(f"Could not pull binary archive {binary_archive_path}")


def clone_binary_archive(name, url, config):
    logger.info(f"Trying to clone binary archive from remote {name} ({url})")
    binary_archive_path = os.path.join(config.binary_archives_dir, name)
    env = os.environ
    env["GIT_LFS_SKIP_SMUDGE"] = "1"
    result = subprocess.run(["git", "clone", url, binary_archive_path], env=env)
    if result.returncode:
        logger.info(f"Could not clone binary archive from remote {name}!")


def git_pull(directory):
    env = os.environ
    env["GIT_LFS_SKIP_SMUDGE"] = "1"
    return subprocess.run(["git", "-C", directory, "pull", "--ff-only"], env=env)