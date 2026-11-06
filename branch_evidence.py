"""Extract dated branch-count claims from archived website pages."""

import re
from datetime import datetime

DATE_PATTERN = re.compile(
    r"\b("
    r"(?:January|February|March|April|May|June|July|August|"
    r"September|October|November|December)\s+\d{1,2},?\s+\d{4}"
    r")\b",
    re.I,
)

COUNT_PATTERN = re.compile(
    r"\b(\d+)\s+branch office locations\b",
    re.I,
)


def extract_publication_date(markdown):
    """Read an article's publication date, not its crawl date."""
    for line in markdown.splitlines()[:20]:
        match = DATE_PATTERN.search(line)
        if not match:
            continue

        value = match.group(1).replace(",", "")
        try:
            return datetime.strptime(value, "%B %d %Y").date()
        except ValueError:
            continue

    return None


def branch_count_candidates(pages):
    """Collect sourced branch-count statements from a snapshot."""
    candidates = []

    for url, markdown in pages.items():
        published = extract_publication_date(markdown)

        for line in markdown.splitlines():
            match = COUNT_PATTERN.search(line)
            if not match:
                continue

            candidates.append({
                "count": int(match.group(1)),
                "published": published,
                "url": url,
                "quote": line.strip()[:350],
            })

    return candidates


def select_branch_count(pages, as_of=None):
    """Choose the latest dated claim; retain its source."""
    candidates = branch_count_candidates(pages)

    if as_of:
        candidates = [
            c for c in candidates
            if c["published"] is not None
            and c["published"].isoformat() <= as_of[:10]
        ]

    dated = [c for c in candidates if c["published"] is not None]

    if not dated:
        return None

    dated.sort(
        key=lambda c: (c["published"], c["url"]),
        reverse=True,
    )

    return dated[0]
