from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from functionalpy import Seq


@dataclass(frozen=True)
class Line:
    line_content: str
    filepath: Path
    line_number: int

    def create_project_import_str(self, monorepo_root: Path) -> str:
        return str(self.filepath.relative_to(monorepo_root)).replace("/", ".")


## Validation
def is_from_import_line(line: str) -> bool:
    return line.startswith("from ")


def import_from_str(line_content: str, from_str: str) -> bool:
    return line_content.startswith(f"from {from_str}")


def line_is_from_subdir(line: Line, subdir: Path) -> bool:
    try:
        line.filepath.relative_to(subdir)
        return True
    except ValueError:
        return False


def line_is_from_project(line: Line, project_dir: Path) -> bool:
    return line_is_from_subdir(line, project_dir)


def line_is_from_library(line: Line, library_dir: Path) -> bool:
    return line_is_from_subdir(line, library_dir)


def line_imports_from_own_project(line: Line, project_import_str: str) -> bool:
    return import_from_str(line.line_content, project_import_str)


def line_contains_local_import(
    line: Line,
    project_import_strs: Iterable[str],
    library_import_str: str,
) -> bool:
    # Check whether the line contents contain any of the project dirs or the library dir
    return any(
        (
            import_from_str(line.line_content, library_import_str),
            any(
                import_from_str(line.line_content, from_str=project_import_str)
                for project_import_str in project_import_strs
            ),
        ),
    )


def import_from_another_project(
    line: Line,
    current_project_dir: Path,
    library_dir: Path,
) -> bool:
    return line_contains_local_import and not any(
        (
            line_is_from_project(line, project_dir=current_project_dir),
            line_is_from_library(line, library_dir=library_dir),
        ),
    )


def create_project_import_in_lib_error(line: Line) -> str:
    return f"{line.filepath}:{line.line_number}: MIMP1, {line.line_content} is from a project, but is imported in a library"


## File handling
def get_files_in_dir(dirpath: Path):
    yield from dirpath.glob("**/*.py")


def get_lines_from_file(filepath: Path) -> list[Line]:
    lines = []
    with filepath.open() as f:
        for line_number, line_content in enumerate(f):
            lines.append(
                Line(
                    filepath=filepath,
                    line_number=line_number,
                    line_content=line_content.strip(),
                ),
            )

    return lines


if __name__ == "__main__":
    monorepo_root = Path(__file__).parent.parent.parent.parent

    import_lines = (
        Seq(get_files_in_dir(Path(__file__).parent.parent.parent / "common"))
        .map(lambda f: get_lines_from_file(f))
        .flatten()
        .filter(lambda line: is_from_import_line(line.line_content))
    )

    project_dir = [Path(__file__).parent.parent.parent / "projects"]
    # Get all top-level-directories in project_dir
    project_dirs = (
        Seq(project_dir).map(lambda dirpath: list(dirpath.glob("*"))).flatten()
    )

    local_imports_from_project = (
        import_lines.filter(
            lambda line: line_is_from_project(
                line,
                Path(__file__).parent.parent.parent,
            ),
        )
        .filter(
            lambda line: line_contains_local_import(
                line,
                project_import_strs=["psycop.projects"],
                library_import_str="psycop.common",
            ),
        )
        .filter(lambda line: not line_imports_from_own_project(line, "psycop.projects"))
    )

    val2 = 2
