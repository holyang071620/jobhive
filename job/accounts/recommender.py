from .models import Job

def get_recommended_jobs(user):
    try:
        user_profile = user.profile
        user_skills = user_profile.skills or ""
    except:
        return []  # Return empty list if user has no profile

    jobs = Job.objects.all()
    job_descriptions = [job.description or "" for job in jobs]

    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    documents = [user_skills] + job_descriptions
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(documents)
    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # Pair jobs with similarity scores and sort them
    scored_jobs = sorted(zip(jobs, similarity_scores), key=lambda x: x[1], reverse=True)

    # Get top 5 recommended jobs with a positive score
    recommended_jobs = [job for job, score in scored_jobs if score > 0][:5]

    return recommended_jobs
