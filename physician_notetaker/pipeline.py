from typing import Dict, Any
from .preprocessing import parse_transcript
from .ner import extract_entities
from .sentiment_intent import summarize_patient_sentiment_intent
from .summarizer import generate_medical_summary
from .soap import generate_soap

def process_transcript(raw: str) -> Dict[str, Any]:
    parsed = parse_transcript(raw)
    full_text = " ".join(p['text'] for p in parsed)
    entities = extract_entities(full_text)
    medical_summary = generate_medical_summary(parsed, entities, full_text)
    sentiment_intent = summarize_patient_sentiment_intent(parsed)
    patient_lines = [u for u in parsed if "patient" in u["speaker"]]
    doctor_lines = [u for u in parsed if "doctor" in u["speaker"] or "physician" in u["speaker"]]
    soap_note = generate_soap(patient_lines, doctor_lines, medical_summary)
    return {
        "medical_summary": medical_summary,
        "sentiment_intent": sentiment_intent,
        "soap_note": soap_note
    }