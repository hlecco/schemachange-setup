"""Tool used to deploy SQL scripts with appropriate names."""
from pathlib import Path
import argparse
import datetime
import logging
import shutil
import os
import re


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def deploy_scripts(issue):
    all_scripts = [
        (directory, filename)
        for (directory, _, filenames) in os.walk("scripts")
        for filename in filenames
    ]

    script_matches = []
    for (directory, filename) in all_scripts:
        match_ = re.match(
            r"JIRA-" + str(issue) + r"-(R|A|V)-(.+\.sql)",
            filename
        )
        if match_:
            script_matches.append((directory, match_))

    if not script_matches:
        raise FileNotFoundError(f"No file exists for issue {issue}")

    versioned_file_counter = 0
    versioned_file_time =  datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S")
    for (directory, match_) in script_matches:
        original_file = os.path.join(directory, match_.group())
        script_prefix = match_.group(1)
        script_name = match_.group(2)

        if script_prefix == 'V':
            script_prefix = '_'.join([
                "V",
                versioned_file_time,
                str(versioned_file_counter)
            ])
            versioned_file_counter += 1

        new_file = f"deploy/{script_prefix}__{script_name}"

        shutil.copy(
            original_file,
            new_file
        )
        logger.info(f"Deployed {original_file} as {new_file}.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("issue",
                        type=int,
                        help="Issue number to deploy scripts from.")

    args = parser.parse_args(argv)

    deploy_scripts(args.issue)
    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    raise SystemExit(main())
