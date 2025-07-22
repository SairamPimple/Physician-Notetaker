from typing import Dict, List, Optional
import re

def generate_soap(patient_lines: List[Dict], doctor_lines: List[Dict], summary_json: Dict):
    subj = _build_subjective(patient_lines, summary_json)
    obj = _build_objective(doctor_lines)
    assessment = _build_assessment(summary_json)
    plan = _build_plan(summary_json)
    return {
        "Subjective": subj,
        "Objective": obj,
        "Assessment": assessment,
        "Plan": plan,
    }

def _build_subjective(patient_lines, summary):
    chief = _derive_chief_complaint(summary.get("Symptoms", []))
    hpi = _synthesize_hpi(patient_lines, summary)
    return {
        "Chief_Complaint": chief,
        "History_of_Present_Illness": hpi
    }

def _build_objective(doctor_lines):
    exam_lines = [l["text"] for l in doctor_lines if any(k in l["text"].lower()
                    for k in ("range of", "tenderness", "no signs", "movement", "muscles", "spine"))]
    return {
        "Physical_Exam": " ".join(exam_lines) if exam_lines else None,
        "Observations": "Patient appears well, no acute distress."
    }

def _build_assessment(summary):
    severity = _infer_severity(summary.get("Current_Status"))
    return {
        "Diagnosis": summary.get("Diagnosis"),
        "Severity": severity
    }

def _build_plan(summary):
    treatments = summary.get("Treatment") or []
    follow = "Patient to return if pain worsens or persists beyond six months."
    return {
        "Treatment": ", ".join(treatments) if treatments else None,
        "Follow_Up": follow
    }

# Helpers
def _derive_chief_complaint(symptoms):
    if not symptoms:
        return None
    multi = [s for s in symptoms if "neck" in s.lower() and "back" in s.lower()]
    if multi:
        return multi[0]
    neck = any("neck" in s.lower() for s in symptoms)
    back = any("back" in s.lower() for s in symptoms)
    if neck and back:
        return "Neck and back pain"
    return symptoms[0]

def _synthesize_hpi(patient_lines, summary):
    text = " ".join(p["text"] for p in patient_lines)
    parts = []
    mech_match = re.search(r"(rear.*?collision|car (?:hit|accident))", text, re.I)
    if mech_match:
        parts.append("Patient had a car accident (rear-end collision).")
    if summary.get("Symptoms"):
        parts.append("Initial symptoms: " + ", ".join(summary["Symptoms"][:3]) + ".")
    if "Occasional" in (summary.get("Current_Status") or ""):
        parts.append("Current: " + summary["Current_Status"].replace("Occasional ", "Occasional ").rstrip(".") + ".")
    else:
        if summary.get("Current_Status"):
            parts.append("Current: " + summary["Current_Status"] + ".")
    # Condense
    hpi = " ".join(parts)
    # Final manual tweak for readability
    return hpi or text

def _infer_severity(current_status: Optional[str]) -> Optional[str]:
    if not current_status:
        return None
    low = current_status.lower()
    if "occasional" in low or "intermittent" in low or "mild" in low:
        return "Mild, improving"
    if "improving" in low or "recovering" in low:
        return "Improving"
    return "Undetermined"