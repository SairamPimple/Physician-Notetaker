"""Configuration: patterns and lexicon for slim pipline."""

# Entry ruler patterns
ENTITY_PATTERNS = [
    # Core symptom phrases
    {"label": "SYMPTOM", "pattern": [{"LOWER": "neck"}, {"LOWER": "pain"}]},
    {"label": "SYMPTOM", "pattern": [{"LOWER": "back"}, {"LOWER": "pain"}]},
    {"label": "SYMPTOM", "pattern": [{"LOWER": "neck"}, {"LOWER": "and"}, {"LOWER": "back"}, {"LOWER": "pain"}]},
    {"label": "SYMPTOM", "pattern": [{"LOWER": "backache"}]},
    {"label": "SYMPTOM", "pattern": [{"LOWER": "backaches"}]},
    {"label": "SYMPTOM", "pattern": [{"LOWER": "trouble"}, {"LOWER": "sleeping"}]},
    {"label": "SYMPTOM", "pattern": [{"LOWER": "sleep"}, {"LOWER": "difficulty"}]},
    {"label": "SYMPTOM", "pattern": [{"LOWER": "sleep"}, {"LOWER": "trouble"}]},
    {"label": "SYMPTOM", "pattern": [{"LOWER": "hit"}, {"LOWER": "my"}, {"LOWER": "head"}]},
    {"label": "SYMPTOM", "pattern": [{"LOWER": "head"}, {"LOWER": "injury"}]},
    # Treatments
    {"label": "TREATMENT", "pattern": [{"LOWER": "physiotherapy"}]},
    {"label": "TREATMENT", "pattern": [{"LOWER": "physio"}]},
    {"label": "TREATMENT", "pattern": [{"LOWER": "painkillers"}]},
    {"label": "TREATMENT", "pattern": [{"LOWER": "analgesics"}]},
    # Diagnosis
    {"label": "DIAGNOSIS", "pattern": [{"LOWER": "whiplash"}, {"LOWER": "injury"}]},
    {"label": "DIAGNOSIS", "pattern": [{"LOWER": "lumbar"}, {"LOWER": "strain"}]},
    {"label": "DIAGNOSIS", "pattern": [{"LOWER": "cervical"}, {"LOWER": "strain"}]},
    # Prognosis (phrases)
    {"label": "PROGNOSIS", "pattern": [{"LOWER": "full"}, {"LOWER": "recovery"}]},
]

# Symptom normalization
SYMPTOM_NORMALIZATION = {
    "backaches": "Back pain (intermittent)",
    "backache": "Back Pain",
    "neck and back pain": "Neck and back pain",
    "trouble sleeping": "Sleeping distrubance",
    "sleep difficulty": "Sleeping disturbance",
    "sleep trouble": "Sleep disturbance",
    "hit my head": "Head impact",
    "head injury": "Head impact"
}

# Lexicons for sentiment / status inference
ANXIOUS_TERMS = {"worried","concerned","nervous","anxious","uneasy","worry","still","discomfort"}
REASSURED_TERMS = {"relief","relieved","better","improving","improved","great","on track","good to hear"}
REPORT_SYMPTOM_VERBS = {"hurt", "hurts", "aching", "ache", "pain", "stiffness"}

IMPROVEMENT_MARKERS = {"better", "improving", "improved", "nothing like before"}
RESIDUAL_MARKERS = {"occasional", "intermittent", "still", "only", "mild"}

PROGNOSIS_WINDOW_PATTERNS = [r"full recovery (?:expected )?(?:within|in)\s+(?P<num>\w+)\s+months?"]

NUMBER_WORDS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five":5,
    "six":6, "seven":7, "eight":8, "nine":9, "ten":10,
    "eleven":11, "twelve":12
}

INTENT_PRIORITY = [
    "Seeking reassurance",
    "Reporting symptoms",
    "Expressing concern",
    "Functional impact",
    "Treatment response",
    "Describing event",
    "Clarifying prognosis",
    "Denying symptoms",
    "Gratitude / Closing",
]