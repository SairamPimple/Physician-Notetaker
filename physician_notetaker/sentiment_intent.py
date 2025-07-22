from transformers import pipeline
from typing import List, Dict
import re
from .config import (
    ANXIOUS_TERMS,
    REASSURED_TERMS,
    REPORT_SYMPTOM_VERBS,
    INTENT_PRIORITY,
    RESIDUAL_MARKERS,
    IMPROVEMENT_MARKERS,
)

_sentiment_pipe = pipeline(
    "sentiment-analysis",
    model = "distilbert-base-uncased-finetuned-sst-2-english"
)

def classify_sentiment(text: str) -> str:
    low = text.lower()
    has_anx = any(w in low for w in ANXIOUS_TERMS)
    has_reassure = any(w in low for w in REASSURED_TERMS)
    has_residual = any(w in low for w in RESIDUAL_MARKERS)
    has_improve = any(w in low for w in IMPROVEMENT_MARKERS)
    contrast = any(c in low for c in ("but", "however", "though"))

    if has_anx and not has_reassure:
        return "Anxious"
    if has_anx and has_reassure:
        return "Neutral"
    if has_reassure:
        if has_residual and contrast:
            return "Neutral"
        return "Reassured"
    if has_improve and has_residual:
        return "Neutral"
    
    pred = _sentiment_pipe(text)[0]["label"]
    if pred == "NEGATIVE":
        return "Anxious"
    if pred == "POSSITIVE":
        return "Reassured"
    return "Neutral"

def detect_intent(text: str) -> List[str]:
    low = text.lower()
    intents = set()
    if re.search(r"(worried|concerned|should i|do i need to|affecting me)", low):
        intents.add("Seeking reassurance")
    if any(v in low for v in REPORT_SYMPTOM_VERBS) or re.search(r"(occasional|intermittent|still .* pain)", low):
        intents.add("Reporting symptoms")
    if re.search(r"(hit me|rear|collision|accident|pushed my car)", low):
        intents.add("Describing event")
    if re.search(r"(week off|work|rutine|activities)", low):
        intents.add("Functional impact")
    if re.search(r"(physio|therapy|sessions?|painkillers|medication|analgesic)", low):
        intents.add("Treatment response")
    if re.search(r"(full recovery|long[- ]term|future)", low):
        intents.add("Clarifying prognosis")
    if re.search(r"\bno\b.*(anxiety|issues|emotional|nervous)", low):
        intents.add("Denying symptoms")
    if re.search(r"\b(thanks|thank you|appreciate|relief)\b", low):
        intents.add("Gratitude / Closing")
    
    if not intents:
        return []
    ordered = [i for i in INTENT_PRIORITY if i in intents]
    return ordered or list(intents)

def summarize_patient_sentiment_intent(parsed) -> Dict:
    patient_utts = [u for u in parsed if "patient" in u["speaker"]]
    if not patient_utts:
        return {"Sentiment": None, "Intent": None}
    
    best = None
    best_rank = -1
    for u in patient_utts:
        txt = u["text"].lower()
        rank = 0
        if any(w in txt for w in ANXIOUS_TERMS): rank += 3
        if "?" in txt: rank += 1
        if "worried" in txt or "concern" in txt: rank += 5
        if rank > best_rank:
            best_rank = rank
            best = u
    target = best or patient_utts[-1]
    sentiment = classify_sentiment(target["text"])
    intents = detect_intent(target["text"])
    intent = intents[0] if intents else None
    return {"Sentiment": sentiment, "Intent": intent}