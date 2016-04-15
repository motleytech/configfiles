#!/usr/bin/env python2.7
"""
Git pre-commit hook to check if tests have been added
or modified for staged python files.

It must be places in .git/hooks folder of your repo
and renamed to 'pre-commit' (remove the trailing '.py').

__author__ = "Motleytech http://github.com/motleytech"
"""
# pylint: disable=C0103

import subprocess
import os

from colorama import Fore, Style

def run_command_and_get_output(command):
    """
    As the name describes, this function runs a command
    and returns its output back to the caller as a string.
    """
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    (stdoutdata, _) = proc.communicate()
    return stdoutdata

def check_for_tests():
    """
    Checks whether test files have been modified for any
    modified and staged python files.
    """
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    os.chdir(root_dir)
    result = run_command_and_get_output("git diff --name-only --cached")

    tests_updated = True

    changed_files = [res.strip() for res in result.split("\n")]
    for fpath in changed_files:
        if not fpath.endswith('.py'):
            continue

        fpath = fpath.strip()
        dirpath, fname = os.path.split(fpath)
        if fname.startswith('test_'):
            continue

        testdir = os.path.join(dirpath, 'tests')
        testfilepath = os.path.join(testdir, 'test_' + fname)

        if testfilepath not in changed_files:
            if tests_updated is True:
                tests_updated = False
                print Fore.RED + 'Error: pre-commit check failed.' + Style.RESET_ALL

                print 'Tests for following files missing (or not updated)...'
            print fpath


    if not tests_updated:
        exit(1)

    exit(0)

if __name__ == '__main__':
    check_for_tests()
