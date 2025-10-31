from datetime import date

from daily_report.formatter import DailyReport, generate_report


def test_generate_report_trims_and_splits_lines():
    report = generate_report(
        "タスクA\n\nタスクB\n",
        "気づき1\n気づき2",
        "TODO1\n\nTODO2\n",
        report_date=date(2024, 1, 1),
    )

    assert report == DailyReport(
        report_date=date(2024, 1, 1),
        activities=["タスクA", "タスクB"],
        learnings=["気づき1", "気づき2"],
        todos=["TODO1", "TODO2"],
    )


def test_to_markdown_renders_expected_format():
    report = DailyReport(
        report_date=date(2024, 4, 1),
        activities=["実装A"],
        learnings=["レビューからの学び"],
        todos=[],
    )

    markdown = report.to_markdown()
    assert (
        "## 日報 (2024-04-01)\n\n"
        "### 作業内容\n- 実装A\n\n"
        "### 気づき\n- レビューからの学び\n\n"
        "### 明日のTODO\n- (なし)"
    ) == markdown
