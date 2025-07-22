import spacy
from spacy.pipeline import EntityRuler
from typing import List, Dict
from .config import ENTITY_PATTERNS

#Keep parser for basic sentence segmentation 
_nlp = spacy.load("en_core_web_sm", disable=["lemmatizer"])

if "entity_ruler" not in _nlp.pipe_names:
    ruler = _nlp.add_pipe("entity_ruler", before="ner")
    ruler.add_patterns(ENTITY_PATTERNS)

def extract_entities(text: str) -> List[Dict]:
    doc = _nlp(text)
    out = []
    for ent in doc.ents:
        out.append({
            "text": ent.text,
            "label": ent.label_,
            "start": ent.start_char,
            "end": ent.end_char,
        })
    return out