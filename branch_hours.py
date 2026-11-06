"""Extract labeled branch operating hours from archived Markdown."""

import re

LABEL = re.compile(
    r"\*\*\s*(Lobby|Drive[\s-]?up)\s*\*\*",
    re.I,
)

DAY = re.compile(
    r"\b(?:Monday|Tuesday|Wednesday|Thursday|Friday|"
    r"Saturday|Sunday|Mon|Tue|Wed|Thu|Fri|Sat|Sun)\b",
    re.I,
)

END = re.compile(
    r"\*\*\s*ABOUT DUPACO\b|^#{1,6}\s",
    re.I | re.M,
)


def extract_branch_hours(markdown):
    """Return separate lobby and drive-up schedules."""
    results = []
    labels = list(LABEL.finditer(markdown))

    for i, match in enumerate(labels):
        start = match.end()
        end = (
            labels[i + 1].start()
            if i + 1 < len(labels)
            else len(markdown)
        )

        section = markdown[start:end]

        boundary = END.search(section)
        if boundary:
            section = section[:boundary.start()]

        lines = [
            line.strip()
            for line in section.splitlines()
            if DAY.search(line)
        ]

        if not lines:
            continue

        service = (
            "drive-up"
            if match.group(1).lower().startswith("drive")
            else "lobby"
        )

        results.append({
            "service": service,
            "schedule": " ".join(lines[:8]),
        })

    return results
