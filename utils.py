from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PyPDF2 import PdfReader


def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def calculate_match(resume_text, job_desc):
    texts = [resume_text, job_desc]

    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform(texts)

    similarity = cosine_similarity(vectors[0:1], vectors[1:2])
    return round(similarity[0][0] * 100, 2)


def get_missing_keywords(resume_text, job_desc, top_n=10):
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([job_desc])

    feature_names = vectorizer.get_feature_names_out()
    scores = vectors.toarray()[0]

    # Get top keywords from job description
    keywords_scores = list(zip(feature_names, scores))
    sorted_keywords = sorted(keywords_scores, key=lambda x: x[1], reverse=True)

    top_keywords = [word for word, score in sorted_keywords[:top_n]]

    resume_words = set(resume_text.lower().split())

    missing = [word for word in top_keywords if word.lower() not in resume_words]

    return missing