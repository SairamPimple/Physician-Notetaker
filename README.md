# Physician Notetaker

## Project Overview
**Physician Notetaker** is a lightweight NLP pipeline that converts raw physician–patient transcripts into three structured JSON artifacts:

1. **`medical_summary`** – key clinical facts (symptoms, diagnosis, treatment, prognosis, status)  
2. **`sentiment_intent`** – patient’s dominant sentiment and primary conversational intent  
3. **`soap_note`** – a synthesized SOAP (Subjective, Objective, Assessment, Plan) note

The design favors transparency and deterministic behavior: most logic is rule/regex driven, with only a small pretrained sentiment model for fallback classification.
---

## Table of Content
1. [Project Overview](#project-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Features](#features)
4. [Tools & Technologies]

---

## Architecture Diagram

	(https://github.com/SairamPimple Hospital_Management_System_SQL_Project/blob/main/ER%20Diagram.png)

---

## Features
	•	Transcript Parsing: Robust speaker-aware parsing that merges continuation lines.
	•	Custom NER: spaCy EntityRuler patterns for SYMPTOM, TREATMENT, DIAGNOSIS, PROGNOSIS.
	•	Medical Summary Generation: Entity merging, normalization, prognosis window extraction, current status inference.
	•	Sentiment & Intent Detection: Lexicon-first heuristics with fallback to HuggingFace distilbert-base-uncased-finetuned-sst-2-english.
	•	SOAP Note Builder: Automatic S/O/A/P sections generated from parsed lines and the summary JSON.
	•	Single-call Pipeline: process_transcript(raw_text) returns all three JSON objects.
	•	Slim & Explainable: Minimal dependencies, rule-driven logic for easy auditing.

---

## Tools & Technologies
	•	Language: Python 3.8+
	•	NLP Libraries:
	•	spaCy (en_core_web_sm model + EntityRuler)
	•	HuggingFace Transformers sentiment pipeline
	•	Regex & Rule Systems: Python re, custom lexicons & normalization maps
	•	Utilities: pprint for demo output

---

## File Structure
├── Hospital_DB_Tables.sql            
├── Hospital_DB_Data.sql       
├── triggers_and_views.sql     
└── Questions.sql            

---

## Setup & Usage

1. Clone & create environment
git clone <repo-url>
cd Physician\ Notetaker
python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows
# .venv\Scripts\activate

2. Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

3. Run the demo script
python demo.py

---

Contributing
	1.	Fork & Branch
	•	Fork the repo, create a feature branch: feat/<short-description>
	2.	Code Style
	•	Follow PEP 8, type-hint functions, keep functions small & testable.
	3.	Tests
	•	Add/extend unit tests for new rules, regexes, or model behavior.
	4.	Patterns & Lexicons
	•	Update config.py for new entities/lexicons; keep names consistent and normalized.
	5.	PR Review
	•	Open a PR with a clear description, sample transcript, and before/after JSON diffs.

---
