from fastapi import FastAPI, Query
import requests
from config import settings

app = FastAPI()

ADZUNA_BASE_URL = "https://api.adzuna.com/v1/api/jobs/gb/search"

@app.get("/api/jobs/search")
def search_jobs(
    title: str = Query(..., description="Job title"),
    location: str = Query(None, description="Job location"),
    results_per_page: int = Query(20, ge=1, le=50),
    days_posted: int = Query(None, ge=0, description="Jobs posted within last X days")
):
    page = 1  # starting page
    params = {
        "app_id": settings.adzuna_app_id,
        "app_key": settings.adzuna_app_key,
        "what": title,
        "where": location,
        "results_per_page": results_per_page
    }
    if days_posted:
        params["max_days_old"] = days_posted

    response = requests.get(f"{ADZUNA_BASE_URL}/{page}", params=params)
    if response.status_code != 200:
        return {"error": "Failed to fetch jobs from Adzuna"}

    data = response.json()
    results = data.get("results", [])

    # Normalize the fields for frontend
    normalized_jobs = []
    for job in results:
        normalized_jobs.append({
            "id": job.get("id"),
            "title": job.get("title"),
            "company": job.get("company", {}).get("display_name"),
            "location": job.get("location", {}).get("display_name"),
            "salary_min": job.get("salary_min"),
            "salary_max": job.get("salary_max"),
            "posted_date": job.get("created"),
            "description_snippet": job.get("description")[:200]  # optional
        })

    return {"jobs": normalized_jobs, "count": data.get("count")}
