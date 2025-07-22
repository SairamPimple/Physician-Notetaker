# Physician Notetaker

Project Overview

Physician Notetaker is a lightweight NLP pipeline that converts raw physician–patient transcripts into three structured JSON artifacts:
	1.	medical_summary – key clinical facts (symptoms, diagnosis, treatment, prognosis, status)
	2.	sentiment_intent – patient’s dominant sentiment and primary conversational intent
	3.	soap_note – a synthesized SOAP (Subjective, Objective, Assessment, Plan) note

The design favors transparency and deterministic behavior: most logic is rule/regex driven, with only a small pretrained sentiment model for fallback classification.

⸻

Architecture Diagram

Option A – Mermaid (copy into GitHub/VS Code/mermaid.live):

flowchart LR
    A[Input Transcript (text from ASR or manual)] --> B[Preprocessing\nparse_transcript()]
    B -->|patient lines| B1[Patient Utterances]
    B -->|doctor lines| B2[Doctor/Physician Utterances]
    B --> C[Full Text Join]

    C --> D[NER\nextract_entities()\nspaCy + EntityRuler]
    D --> E[Medical Summary\ngenerate_medical_summary()]
    C --> E

    B1 --> F[Sentiment & Intent\nsummarize_patient_sentiment_intent()]
    E --> H[SOAP Note\ngenerate_soap()]
    B1 --> H
    B2 --> H

    E --> I[medical_summary JSON]
    F --> J[sentiment_intent JSON]
    H --> K[soap_note JSON]

    subgraph Config & Rules
        CFG[config.py:\nENTITY_PATTERNS, lexicons, normalization]
    end

    CFG -.-> D
    CFG -.-> E
    CFG -.-> F

Option B – PNG
Place the exported PNG (e.g., docs/architecture.png) and reference it here:

![Physician Notetaker Architecture](docs/architecture.png)


⸻

Features
	•	Transcript Parsing: Robust speaker-aware parsing that merges continuation lines.
	•	Custom NER: spaCy EntityRuler patterns for SYMPTOM, TREATMENT, DIAGNOSIS, PROGNOSIS.
	•	Medical Summary Generation: Entity merging, normalization, prognosis window extraction, current status inference.
	•	Sentiment & Intent Detection: Lexicon-first heuristics with fallback to HuggingFace distilbert-base-uncased-finetuned-sst-2-english.
	•	SOAP Note Builder: Automatic S/O/A/P sections generated from parsed lines and the summary JSON.
	•	Single-call Pipeline: process_transcript(raw_text) returns all three JSON objects.
	•	Slim & Explainable: Minimal dependencies, rule-driven logic for easy auditing.

⸻

Tools & Technologies
	•	Language: Python 3.8+
	•	NLP Libraries:
	•	spaCy (en_core_web_sm model + EntityRuler)
	•	HuggingFace Transformers sentiment pipeline
	•	Regex & Rule Systems: Python re, custom lexicons & normalization maps
	•	Utilities: pprint for demo output

⸻

Setup & Usage

1. Clone & create environment

git clone <repo-url>
cd Physician\ Notetaker
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

2. Install dependencies

pip install -r requirements.txt
python -m spacy download en_core_web_sm

3. Run the demo script

python demo.py

You should see three printed sections: medical_summary, sentiment_intent, and soap_note.

4. Use as a library

from physician_notetaker.pipeline import process_transcript

with open("/path/to/transcript.txt") as f:
    raw = f.read()

outputs = process_transcript(raw)
print(outputs["soap_note"])  # or any other key

5. (Optional) Export Diagram
	•	Import the provided .drawio XML (see docs/physician_notetaker_arch.drawio) into diagrams.net and export as PNG/SVG.

⸻

Contributing
	1.	Fork & Branch:
	•	Fork the repo, create a feature branch: feat/<short-description>
	2.	Code Style:
	•	Follow PEP 8, type-hint functions, keep functions small & testable.
	3.	Tests:
	•	Add/extend unit tests for new rules, regexes, or model behavior.
	4.	Patterns & Lexicons:
	•	Update config.py for new entities/lexicons; keep names consistent and normalized.
	5.	PR Review:
	•	Open a PR with a clear description, sample transcript, and before/after JSON diffs.

⸻

Got questions or need enhancements (CLI, REST API, UI)? Open an issue or start a discussion!s
