import re
from collections import Counter

STOPWORDS = {"what","is","are","the","a","an","how","do","i","can","to","for","of","in","on","my","please","tell","me","about","and","or","university"}

def tokens(text):
    return [w for w in re.findall(r"[a-z0-9]+", (text or "").lower()) if w not in STOPWORDS and len(w) > 1]

def find_answer(question, db, fallback_faqs):
    faqs = []
    source = "Demo FAQ knowledge base"
    if db is not None:
        try:
            docs = db.collection("faqs").stream()
            for doc in docs:
                row = doc.to_dict() or {}
                if row.get("question") and row.get("answer"):
                    faqs.append(row)
            if faqs:
                source = "Cloud Firestore"
        except Exception:
            pass
    if not faqs:
        faqs = fallback_faqs

    q_tokens = set(tokens(question))
    if not q_tokens:
        return "Please enter a question about admissions, courses, fees, examinations, scholarships, or student services.", source

    scored = []
    for faq in faqs:
        combined = set(tokens(faq.get("question", "") + " " + " ".join(faq.get("keywords", []))))
        overlap = len(q_tokens & combined)
        score = overlap / max(1, len(q_tokens))
        if score:
            scored.append((score, faq))
    if scored:
        scored.sort(key=lambda x: x[0], reverse=True)
        score, best = scored[0]
        if score >= 0.25 or len(q_tokens) == 1:
            return best["answer"], source
    return ("I couldn't find a verified answer for that question in the current FAQ database. "
            "Please try different keywords or contact the university office. Add verified university FAQs to the Cloud Firestore `faqs` collection to improve coverage."), source
