```python
import re

STOPWORDS = {
    "what", "is", "are", "the", "a", "an", "how", "do", "i",
    "can", "to", "for", "of", "in", "on", "my", "please",
    "tell", "me", "about", "and", "or", "university",
    "available", "does", "your"
}

def tokens(text):
    return [
        word
        for word in re.findall(r"[a-z0-9]+", (text or "").lower())
        if word not in STOPWORDS and len(word) > 1
    ]


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
            faqs = []

    if not faqs:
        faqs = fallback_faqs

    question_tokens = set(tokens(question))

    if not question_tokens:
        return (
            "Please enter a question about admissions, courses, "
            "fees, scholarships, examinations, or student services.",
            source
        )

    scored = []

    for faq in faqs:
        faq_question = faq.get("question", "")
        keywords = faq.get("keywords", [])

        if isinstance(keywords, str):
            keywords = [keywords]

        searchable_text = faq_question + " " + " ".join(keywords)
        faq_tokens = set(tokens(searchable_text))

        if not faq_tokens:
            continue

        overlap = len(question_tokens & faq_tokens)
        score = overlap / len(question_tokens)

        # Exact question match gets highest priority.
        if question.strip().lower() == faq_question.strip().lower():
            score = 2.0

        # Prefer a FAQ that matches the question more closely.
        if overlap > 0:
            scored.append((score, faq))

    if scored:
        scored.sort(key=lambda item: item[0], reverse=True)
        best_score, best_faq = scored[0]

        if best_score >= 0.5:
            return best_faq["answer"], source

    return (
        "I couldn't find a sufficiently matching answer in the FAQ database. "
        "Please try another question or contact the university office.",
        source
    )
```
