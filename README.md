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
4. [Tools & Technologies](#tools--technologies)
5. [File Structure](#file-structure)
6. [Setup & Usage](#setup--usage)

---

## Architecture Diagram
![Architecture Diagram](https://github.com/SairamPimple/Physician-Notetaker/blob/main/images/A_flowchart-style_diagram_titled_%22Physician_Noteta.png)

---

## Features
- Transcript Parsing: Robust speaker-aware parsing that merges continuation lines.
- Custom NER: spaCy EntityRuler patterns for SYMPTOM, TREATMENT, DIAGNOSIS, PROGNOSIS.
- Medical Summary Generation: Entity merging, normalization, prognosis window extraction, current status inference.
- Sentiment & Intent Detection: Lexicon-first heuristics with fallback to HuggingFace distilbert-base-uncased-finetuned-sst-2-english.
- SOAP Note Builder: Automatic S/O/A/P sections generated from parsed lines and the summary JSON.
- Single-call Pipeline: process_transcript(raw_text) returns all three JSON objects.
- Slim & Explainable: Minimal dependencies, rule-driven logic for easy auditing.

---

## Tools & Technologies
- Language: Python 3.8+
- NLP Libraries:
	- spaCy (en_core_web_sm model + EntityRuler)
	- HuggingFace Transformers sentiment pipeline
	- Regex & Rule Systems: Python re, custom lexicons & normalization maps
- Utilities: pprint for demo output

---

## File Structure
physician-notetaker/  
├── README.md   
├── requirements.txt  
├── demo.py  
└── physician_notetaker  
    - ├── config.py  
    - ├── preprocessing.py  
    - ├── ner.py  
    - ├── sentiment_intent.py  
    - ├── summarizer.py  
    - ├── soap.py  
    - └── pipeline.py  

---

## Setup & Usage
1. Clone & create environment
	'''python
	git clone <repo-url>
	cd Physician\ Notetaker
	conda create -n physician-notetaker python=3.10 -y # create env
	conda activate physician-notetaker # activate env
    

2. Install dependencies
	'''python
	pip install -r requirements.txt
	python -m spacy download en_core_web_sm

3. Run the demo script
	'''python
	python demo.py

---
