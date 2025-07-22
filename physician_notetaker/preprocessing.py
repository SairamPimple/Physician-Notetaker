import re
from typing import List, Dict

SPEAKER_RE = re.compile(r"^(Doctor|Physician|Patient|Dr\.?|Pt\.?):\s*", re.I)

def parse_transcript(raw: str) -> List[Dict]:
    """Returns list of {id, speaker, text} dicts"""
    lines = []
    uid = 0
    for line in raw.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        m = SPEAKER_RE.match(line)
        if not m:
            # Treat as continuation of previous line
            if lines:
                lines[-1]["text"] += " " + line
            continue
        speaker = m.group(1).lower()
        text = SPEAKER_RE.sub("", line).strip()
        uid += 1
        lines.append({"id":uid, "speaker": speaker, "text": text})
    return lines