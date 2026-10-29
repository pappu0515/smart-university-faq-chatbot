import re

STOPWORDS = {
    "what", "is", "are", "the", "a", "an", "how", "do", "i",
    "can", "to", "for", "of", "in", "on", "my", "please",
    "tell", "me", "about", "and", "or", "university",
    "available", "does", "your", "which", "list", "give",
    "show", "me", "much"
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
            for doc in db.collection("faqs").stream():
                row = doc.to_dict() or {}

                if row.get("question") and row.get("answer"):
                    faqs.append(row)

            if faqs:
                source = "Cloud Firestore"

        except Exception as error:
            print("Firestore read error:", error)

    if not faqs:
        faqs = fallback_faqs

    normalized_question = (question or "").strip().lower()
    question_tokens = set(tokens(normalized_question))

    if not question_tokens:
        return (
            "Please ask a question about admissions, courses, fees, "
            "scholarships, examinations, or student services.",
            source
        )

    best_faq = None
    best_score = 0

    for faq in faqs:
        faq_question = faq.get("question", "")
        keywords = faq.get("keywords", [])

        if isinstance(keywords, str):
            keywords = [keywords]

        searchable_text = faq_question + " " + " ".join(keywords)
        faq_tokens = set(tokens(searchable_text))

        if normalized_question == faq_question.strip().lower():
            return faq["answer"], source

        if not faq_tokens:
            continue

        overlap = len(question_tokens & faq_tokens)
        score = overlap / len(question_tokens)

        if score > best_score:
            best_score = score
            best_faq = faq

    if best_faq and best_score >= 0.5:
        return best_faq["answer"], source

    return (
        "I couldn't find a matching answer in the FAQ database. "
        "Please try asking with different keywords or contact the university office.",
        source
    )
