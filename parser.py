import re


def parse_instruction(text):
    """
    Turn free-form natural language test instructions into a list of
    structured step dicts: {"type": ..., "label": ..., "detail": ...}
    """
    steps = []
    lines = text.lower().split("\n")

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue

        if "open" in line:
            match = re.search(r"open\s+(.+)", line)
            target = match.group(1).strip() if match else "page"
            steps.append({"type": "open", "label": "OPEN PAGE", "detail": target})

        elif "username" in line:
            match = re.search(r"username\s*[:\-]?\s*(.+)", line)
            detail = match.group(1).strip() if match and match.group(1).strip() else ""
            steps.append({"type": "username", "label": "ENTER USERNAME", "detail": detail})

        elif "password" in line:
            steps.append({"type": "password", "label": "ENTER PASSWORD", "detail": "••••••••"})

        elif "click" in line:
            match = re.search(r"click\s+(?:on\s+)?(.+)", line)
            detail = match.group(1).strip() if match else ""
            steps.append({"type": "click", "label": "CLICK BUTTON", "detail": detail})

        else:
            steps.append({"type": "unknown", "label": "UNRECOGNIZED STEP", "detail": line})

    return steps
