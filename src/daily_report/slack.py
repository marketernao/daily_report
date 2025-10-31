"""Slack webhook integration."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Optional


class SlackError(RuntimeError):
    """Raised when a Slack API call fails."""


@dataclass(slots=True)
class SlackWebhookClient:
    """Simple client for posting Markdown reports to Slack via webhooks."""

    webhook_url: str

    @classmethod
    def from_env_or_value(cls, value: Optional[str] = None) -> "SlackWebhookClient":
        webhook = value or os.environ.get("SLACK_WEBHOOK_URL")
        if not webhook:
            raise SlackError(
                "Slack webhook URL must be provided via --webhook-url or SLACK_WEBHOOK_URL"
            )
        return cls(webhook_url=webhook)

    def post_markdown(self, markdown: str) -> None:
        payload = json.dumps({"text": markdown, "mrkdwn": True}).encode("utf-8")
        request = urllib.request.Request(
            self.webhook_url,
            data=payload,
            headers={"Content-Type": "application/json; charset=utf-8"},
        )
        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                if response.status >= 400:
                    body = response.read().decode("utf-8", errors="replace")
                    raise SlackError(
                        f"Slack webhook request failed with status {response.status}: {body}"
                    )
        except urllib.error.URLError as exc:  # pragma: no cover - network failure branch
            raise SlackError(f"Slack webhook request failed: {exc}") from exc
