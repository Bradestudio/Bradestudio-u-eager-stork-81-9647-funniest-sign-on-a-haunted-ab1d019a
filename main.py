"""Funniest Sign on a Haunted Server Room Door — make.fun entry (program/v1).

Writes one sign line (98 characters, UTF-8, no trailing newline) to
/output/entry.txt.

The sign reads like a real door notice taped up by the night-shift
sysadmin: do not reboot the ghost, because the ghost is not a pest to
get rid of — it is the longest-serving member of the on-call rota,
older than every rack in the room.
It has root access, it knows your password, and it has been on call
since 1987. The joke is the collision of office IT life (root access,
passwords, the on-call rota) with the supernatural (a ghost that
cannot be rebooted away), and it lands in one line without a pun that
needs a second read.

Standard library only. No network, no local imports, no writes
outside the output path the harness provides. Deterministic: the
same bytes on every run.
"""

import os
import sys

ENTRY = (
    "DO NOT REBOOT THE GHOST. It has root access, knows your password, "
    "and has been on call since 1987."
)


def main():
    line = ENTRY
    if not line or not line.strip():
        sys.exit("entry line is blank")
    if "\n" in line or "\r" in line:
        sys.exit("entry line must be a single line")
    if not 1 <= len(line) <= 120:
        sys.exit("entry line must be 1-120 characters, got %d" % len(line))
    if line != line.strip():
        sys.exit("entry line must not start or end with whitespace")
    if "  " in line:
        sys.exit("entry line must not contain double spaces")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in line):
        sys.exit("entry line must not contain control characters")
    if not line.startswith("DO NOT REBOOT THE GHOST."):
        # The warning is the sign itself: it must never silently
        # go missing from the line.
        sys.exit("entry line must start with the DO NOT REBOOT warning")
    if "1987" not in line:
        # The on-call-since-1987 punchline is what makes the ghost
        # the longest-serving admin in the room.
        sys.exit("entry line must keep the since-1987 punchline")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = line.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)
    # Re-read and verify the file is exactly the gated line, no newline.
    with open(path, "rb") as fh:
        written = fh.read()
    if written != data:
        sys.exit("entry.txt does not match the gated line")
    print("wrote %s (%d chars, %d bytes)" % (path, len(line), len(data)))


if __name__ == "__main__":
    main()
