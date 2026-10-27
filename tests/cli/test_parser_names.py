"""The names argparse prints for a typo in a command or verb.

Each subparser's `dest` is an internal field (`group`, `addon_verb`, ...), and
argparse uses it in `argument <dest>: invalid choice` unless a metavar says
otherwise. A person typing `kraft vew list` should be told about the command,
not about a field they never named.
"""

from __future__ import annotations

import pytest

from kraft import cli

GROUPS = ("item", "view", "repo", "admin")


def test_a_mistyped_command_names_the_command(capsys):
    with pytest.raises(SystemExit) as caught:
        cli.main(["vew", "list"])
    assert caught.value.code == 2
    err = capsys.readouterr().err
    assert "argument command: invalid choice: 'vew'" in err
    assert "argument group:" not in err


@pytest.mark.parametrize(
    "argv",
    [
        ["view", "lits"],
        ["admin", "addon", "lits"],
        ["admin", "addon", "collection", "lits"],
        ["admin", "templates", "lints"],
        ["admin", "worker", "ad"],
    ],
)
def test_a_mistyped_verb_names_the_verb(argv, capsys):
    with pytest.raises(SystemExit) as caught:
        cli.main(argv)
    assert caught.value.code == 2
    err = capsys.readouterr().err
    assert f"argument verb: invalid choice: '{argv[-1]}'" in err


def test_help_still_lists_every_group(capsys):
    with pytest.raises(SystemExit) as caught:
        cli.main(["--help"])
    assert caught.value.code == 0
    out = capsys.readouterr().out
    assert "command ..." in out
    for group in GROUPS:
        assert group in out
