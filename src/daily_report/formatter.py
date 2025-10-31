"""Utilities for formatting Markdown daily reports."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timezone
from typing import Iterable, List


@dataclass(slots=True)
class DailyReport:
    """Structured data representing a Markdown daily report."""

    report_date: date
    activities: List[str]
    learnings: List[str]
    todos: List[str]

    def to_markdown(self) -> str:
        """Return the Markdown rendering of the report."""

        heading = self.report_date.strftime("%Y-%m-%d")
        sections = [
            ("作業内容", self.activities),
            ("気づき", self.learnings),
            ("明日のTODO", self.todos),
        ]

        lines: List[str] = [f"## 日報 ({heading})"]
        for title, items in sections:
            lines.append(f"\n### {title}")
            if items:
                lines.extend(f"- {item}" for item in items)
            else:
                lines.append("- (なし)")
        return "\n".join(lines)


def _split_lines(block: str) -> List[str]:
    """Split a block of text into bullet items.

    Empty lines and surrounding whitespace are discarded. Each remaining line
    becomes one bullet item.
    """

    return [line.strip() for line in block.splitlines() if line.strip()]


def generate_report(
    activities_text: str,
    learnings_text: str,
    todos_text: str,
    report_date: date | None = None,
) -> DailyReport:
    """Create a :class:`DailyReport` instance from raw text inputs."""

    if report_date is None:
        report_date = datetime.now(timezone.utc).astimezone().date()

    report = DailyReport(
        report_date=report_date,
        activities=_split_lines(activities_text),
        learnings=_split_lines(learnings_text),
        todos=_split_lines(todos_text),
    )
    return report


def format_markdown(
    activities: Iterable[str],
    learnings: Iterable[str],
    todos: Iterable[str],
    report_date: date | None = None,
) -> str:
    """Convenience wrapper for creating Markdown directly."""

    report = generate_report(
        "\n".join(activities), "\n".join(learnings), "\n".join(todos), report_date
    )
    return report.to_markdown()
