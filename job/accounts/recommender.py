from .models import Job

def get_recommended_jobs(user):
    try:
        user_profile = user.profile
        user_skills = user_profile.skills or ""
    except:
        return []  # Return empty list if user has no profile

    # Filter out jobs posted by the current user and make sure descriptions exist
    jobs = Job.objects.exclude(posted_by=user)
    job_descriptions = [job.description.strip() for job in jobs if job.description and job.description.strip()]

    # Return nothing if descriptions or user skills are empty
    if not job_descriptions or not user_skills.strip():
        return []

    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    # TF-IDF calculation
    documents = [user_skills.strip()] + job_descriptions
    tfidf = TfidfVectorizer(stop_words='english')

    try:
        tfidf_matrix = tfidf.fit_transform(documents)
    except ValueError:
        return []  # Handles edge case: no valid vocabulary

    # Compute similarity scores
    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # Match scores to jobs
    valid_jobs = [job for job in jobs if job.description and job.description.strip()]
    scored_jobs = sorted(zip(valid_jobs, similarity_scores), key=lambda x: x[1], reverse=True)

    # Top 5 recommended jobs
    recommended_jobs = [job for job, score in scored_jobs if score > 0][:5]

    return recommended_jobs
