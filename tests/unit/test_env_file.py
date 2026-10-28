"""@file test_env_file.py
@brief The env file reader parses KEY=VALUE lines (dummy values in tmp_path only).
"""

from pathlib import Path

from snack_and_lift.infrastructure.env_file import read_env_file


def _read(tmp_path: Path, text: str) -> dict[str, str]:
    path = tmp_path / "accounts.env"
    path.write_text(text, encoding="utf-8")
    return read_env_file(path)


def test_read_env_file_returns_empty_when_file_is_missing(tmp_path: Path) -> None:
    assert read_env_file(tmp_path / "absent.env") == {}


def test_read_env_file_reads_pairs(tmp_path: Path) -> None:
    assert _read(tmp_path, "A=1\nB=two\n") == {"A": "1", "B": "two"}


def test_read_env_file_skips_blank_lines_comments_and_lines_without_equals(
    tmp_path: Path,
) -> None:
    text = "\n# comment\n   # indented comment\nnot a pair\nA=1\n"

    assert _read(tmp_path, text) == {"A": "1"}


def test_read_env_file_accepts_export_prefix(tmp_path: Path) -> None:
    assert _read(tmp_path, "export A=1\n") == {"A": "1"}


def test_read_env_file_strips_whitespace_around_key(tmp_path: Path) -> None:
    assert _read(tmp_path, "  A  =1\n") == {"A": "1"}


def test_read_env_file_strips_one_pair_of_quotes(tmp_path: Path) -> None:
    text = "A=\"dummy one\"\nB='dummy two'\nC=\"'both'\"\n"

    assert _read(tmp_path, text) == {"A": "dummy one", "B": "dummy two", "C": "'both'"}


def test_read_env_file_keeps_unmatched_quotes_and_lone_quote(tmp_path: Path) -> None:
    assert _read(tmp_path, 'A="dummy\'\nB="\n') == {"A": "\"dummy'", "B": '"'}


def test_read_env_file_keeps_equals_and_hash_inside_value(tmp_path: Path) -> None:
    assert _read(tmp_path, "A=x=y#z\n") == {"A": "x=y#z"}


def test_read_env_file_ignores_empty_key(tmp_path: Path) -> None:
    assert _read(tmp_path, "=value\n") == {}


def test_read_env_file_keeps_empty_value(tmp_path: Path) -> None:
    assert _read(tmp_path, "A=\n") == {"A": ""}
