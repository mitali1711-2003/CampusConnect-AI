"""
NLP Engine — handles language detection, semantic search, and response generation.
Uses sentence-transformers for similarity matching and langdetect for language detection.
CONFIGURED FOR JSPM WAGHOLI CAMPUS ONLY.
"""

import json
import os
import random
import numpy as np
from langdetect import detect
from sentence_transformers import SentenceTransformer, util

# Load model once globally (lazy initialization)
_model = None
_faq_embeddings = None
_faq_data = None
_mindmate_data = None


def get_model():
    """Lazy-load the sentence transformer model."""
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model


def detect_language(text):
    """Detect language of input text. Returns 'en', 'hi', or 'mr'."""
    try:
        lang = detect(text)
        if lang == 'hi':
            return 'hi'
        elif lang == 'mr':
            return 'mr'
        else:
            return 'en'
    except Exception:
        return 'en'


def load_faqs_from_db():
    """Load Wagholi-only FAQs from database and compute embeddings."""
    global _faq_embeddings, _faq_data
    from models.database import get_db

    conn = get_db()
    cursor = conn.cursor()
    # Load ONLY Wagholi campus FAQs
    cursor.execute("SELECT * FROM faqs WHERE is_active = 1")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return

    _faq_data = [dict(row) for row in rows]
    model = get_model()

    # Build combined question text for each FAQ (all languages for better matching)
    questions = []
    for faq in _faq_data:
        combined = f"{faq['question_en']} {faq.get('question_hi', '')} {faq.get('question_mr', '')}"
        questions.append(combined)

    _faq_embeddings = model.encode(questions, convert_to_tensor=True)


def get_campus_response(user_message, language='en', campus='JSPM Wagholi'):
    """
    Find the best FAQ match for a JSPM Wagholi campus query.
    Improved ranking: uses top-3 candidates and picks best by language match.
    """
    global _faq_embeddings, _faq_data

    if _faq_data is None or _faq_embeddings is None:
        load_faqs_from_db()

    if _faq_data is None or len(_faq_data) == 0:
        fallback = _wagholi_fallback(language)
        return {
            'answer': fallback,
            'confidence': 0.0,
            'faq_id': None,
            'category': 'unknown'
        }

    model = get_model()
    query_embedding = model.encode(user_message, convert_to_tensor=True)

    # Compute cosine similarity
    scores = util.cos_sim(query_embedding, _faq_embeddings)[0]

    # Get top 3 candidates for better ranking
    top_k = min(3, len(_faq_data))
    top_indices = scores.argsort(descending=True)[:top_k]

    best_idx = int(top_indices[0])
    best_score = float(scores[best_idx])

    # Confidence threshold — 0.38 balances accuracy vs coverage
    if best_score < 0.38:
        fallback = _wagholi_fallback(language)
        return {
            'answer': fallback,
            'confidence': best_score,
            'faq_id': None,
            'category': 'unknown'
        }

    # Among top candidates, prefer one with a non-empty answer in user's language
    chosen_idx = best_idx
    for idx in top_indices:
        idx = int(idx)
        faq = _faq_data[idx]
        answer_key = f'answer_{language}'
        if faq.get(answer_key) and float(scores[idx]) > best_score * 0.85:
            chosen_idx = idx
            break

    faq = _faq_data[chosen_idx]
    answer_key = f'answer_{language}'
    answer = faq.get(answer_key) or faq.get('answer_en', '')

    return {
        'answer': answer,
        'confidence': float(scores[chosen_idx]),
        'faq_id': faq.get('id'),
        'category': faq.get('category', 'general')
    }


def _wagholi_fallback(language):
    """Wagholi-specific fallback for unknown queries."""
    fallbacks = {
        'en': "I'm sorry, I don't have that information for JSPM Wagholi Campus. I can help with admissions, courses, fees, hostel, placements, library, facilities, exams, transportation, and contact details — all for JSPM Wagholi only. Try asking about one of these topics!",
        'hi': "क्षमा करें, मेरे पास JSPM वाघोली कैंपस के लिए यह जानकारी नहीं है। मैं प्रवेश, पाठ्यक्रम, शुल्क, छात्रावास, प्लेसमेंट, पुस्तकालय, सुविधाएं, परीक्षा, परिवहन और संपर्क विवरण में मदद कर सकता हूं — केवल JSPM वाघोली के लिए। इनमें से किसी विषय के बारे में पूछें!",
        'mr': "क्षमस्व, माझ्याकडे JSPM वाघोली कॅम्पससाठी ही माहिती नाही. मी प्रवेश, अभ्यासक्रम, शुल्क, वसतिगृह, प्लेसमेंट, ग्रंथालय, सुविधा, परीक्षा, वाहतूक आणि संपर्क तपशील — फक्त JSPM वाघोलीसाठी मदत करू शकतो. यापैकी एखाद्या विषयाबद्दल विचारा!"
    }
    return fallbacks.get(language, fallbacks['en'])


def get_mindmate_response(user_message, language='en', username='friend'):
    """
    Generate empathetic MindMate AI response.
    Personalizes responses with the user's name.
    """
    global _mindmate_data

    # Always reload from file to pick up changes (file is small, ~20KB)
    mindmate_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'database', 'mindmate_responses.json'
    )
    with open(mindmate_path, 'r', encoding='utf-8') as f:
        _mindmate_data = json.load(f)

    categories = _mindmate_data.get('categories', {})
    # Normalize: lowercase, strip punctuation for matching
    message_lower = user_message.lower()
    # Also create a clean version without apostrophes/punctuation for matching
    import re
    message_clean = re.sub(r"[''`]", "'", message_lower)  # normalize quotes
    message_nopunc = re.sub(r"[^\w\s]", " ", message_lower)  # remove all punctuation
    message_nopunc = ' '.join(message_nopunc.split())  # collapse spaces

    # Check each category's keywords — weighted matching
    # Priority: crisis > multi-word phrases > single-word exact > substring
    best_category = 'default'
    max_score = 0

    # Crisis check FIRST (highest priority — safety critical)
    crisis_data = categories.get('crisis', {})
    for kw in crisis_data.get('keywords', []):
        if kw.lower() in message_lower or kw.lower() in message_nopunc:
            best_category = 'crisis'
            max_score = 999
            break

    if max_score < 999:
        for cat_name, cat_data in categories.items():
            if cat_name in ('default', 'crisis'):
                continue
            keywords = cat_data.get('keywords', [])
            score = 0
            for kw in keywords:
                kw_lower = kw.lower()
                kw_nopunc = re.sub(r"[^\w\s]", " ", kw_lower).strip()
                # Multi-word phrases get much higher weight
                is_phrase = ' ' in kw_lower
                # Check against both original and cleaned message
                matched = (kw_lower in message_lower or
                          kw_nopunc in message_nopunc or
                          kw_lower in message_clean)
                if matched:
                    if is_phrase:
                        score += 5  # Multi-word phrases are strong signals
                    elif f' {kw_lower} ' in f' {message_nopunc} ':
                        score += 3  # Exact whole-word match
                    else:
                        score += 1  # Substring match
            if score > max_score:
                max_score = score
                best_category = cat_name

    responses = categories.get(best_category, categories['default']).get('responses', [])
    chosen = random.choice(responses) if responses else "I'm here for you, {name}. Tell me more about how you're feeling. 💛"

    # Replace {name} placeholder with actual username
    display_name = username.capitalize() if username and username != 'friend' else 'friend'
    chosen = chosen.replace('{name}', display_name)

    disclaimer = _mindmate_data.get('disclaimer', '')

    return {
        'answer': chosen,
        'category': best_category,
        'disclaimer': disclaimer
    }


def get_suggested_questions(language='en', limit=5):
    """Get random suggested FAQ questions for display."""
    global _faq_data

    if _faq_data is None:
        load_faqs_from_db()

    if not _faq_data:
        return []

    sample = random.sample(_faq_data, min(limit, len(_faq_data)))
    key = f'question_{language}'
    return [faq.get(key) or faq.get('question_en', '') for faq in sample]


def reload_faqs():
    """Force reload FAQs (after admin edits)."""
    global _faq_embeddings, _faq_data, _mindmate_data
    _faq_embeddings = None
    _faq_data = None
    _mindmate_data = None  # Also reload MindMate responses
    load_faqs_from_db()
