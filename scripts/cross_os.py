#!/usr/bin/env bash

"""
    To execute the pre commit checks based on operating system
"""
from subprocess import SubprocessError, call
from sys import platform
from typing import Dict

operations: Dict = {
    "linux": {
        "format_lint": {
            "isort_single_line_fix": ["isort", "--force-single-line-imports", "app"],
            "auto_flake_fix": [
                "autoflake",
                "--remove-all-unused-imports",
                "--recursive",
                "--remove-unused-variables",
                "--in-place",
                "app",
                "--exclude=__init__.py",
            ],
            "black_fix": ["black", "app"],
            "isort_fix": ["isort", "app"],
            "black_check": ["black", "app", "--check"],
            "isort_check": ["isort", "--check-only", "app"],
        },
        "test": {
            "coverage": [
                "python3",
                "-m",
                "pytest",
                "--cov-report",
                "term-missing",
                "--cov=app",
            ]
        },
    },
}


def execute_cmd_from_ops() -> None:
    try:
        current_platform: str = "linux"
        if platform.startswith("win"):
            # Windows os
            current_platform = "windows"
        cmd_execution_results: Dict = {}
        # Executing operations based on os
        for cmd_args in operations[current_platform].values():
            # get list of commands
            for cmd in cmd_args.values():
                try:
                    # execute the command
                    cmd_execution_results[" ".join(cmd)] = call(cmd)
                except SubprocessError as e:
                    print(str(e.output, "utf-8"))
                    exit(1)
        # check for which command worked and which didn't
        for cmd, result in cmd_execution_results.items():
            print(f"{'success' if result == 0 else 'error'}: {cmd}")
    except Exception as err:
        print(err)
        exit(1)


execute_cmd_from_ops()
