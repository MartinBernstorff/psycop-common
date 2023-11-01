from pathlib import Path, PosixPath

import pytest

from .implib import (
    Line,
    import_from_str,
    is_from_import_line,
    line_contains_local_import,
    line_is_from_project,
)


def line_with_content(line_content: str) -> Line:
    return Line(line_content=line_content, filepath=Path(), line_number=0)


def line_with_path(path: Path) -> Line:
    return Line(line_content="", filepath=path, line_number=0)


@pytest.mark.parametrize(
    ("line", "is_from_import"),
    [
        ("from psycop.fjdiao import fjdiao", True),
        ("I am from", False),
    ],
)
def test_is_import_line(line: str, is_from_import: bool):
    assert is_from_import_line(line) == is_from_import


@pytest.mark.parametrize(
    ("line", "value"),
    [
        ("from library", True),
        ("from lol.library", False),
    ],
)
def test_is_library_import(line: str, value: bool):
    assert import_from_str(line, "psycop.common") == value


@pytest.mark.parametrize(
    ("line", "value"),
    [
        (
            Line(
                line_content="",
                filepath=PosixPath("/project/file.py"),
                line_number=0,
            ),
            True,
        ),
        (
            Line(
                line_content="",
                filepath=PosixPath("/library/file.py"),
                line_number=0,
            ),
            False,
        ),
    ],
)
def test_line_is_from_project(line: Line, value: bool):
    assert line_is_from_project(line, Path("/project")) == value


@pytest.mark.parametrize(
    ("line", "val"),
    [
        (line_with_content(line_content="from common."), True),
        (line_with_content(line_content="from project."), True),
        (line_with_content(line_content="from external_library"), False),
    ],
)
def test_line_contains_local_import(line: Line, val: bool):
    assert (
        line_contains_local_import(
            line=line,
            project_import_strs=["project"],
            library_import_str="common",
        )
        == val
    )


def test_create_project_import_str():
    assert (
        line_with_path(path=Path("/project/file.py")).create_project_import_str(
            monorepo_root=Path("/"),
        )
        == "project"
    )
