import os
import json
import numpy as np
import faiss

from src.vectorstore.embedder import get_embedding


# ============================================================
# PATHS
# ============================================================

INDEX_PATH = "vectorstore/jobs.index"

METADATA_PATH = "vectorstore/jobs_metadata.json"


# ============================================================
# LOAD JOB INDEX
# ============================================================

def load_job_data():

    if not os.path.exists(INDEX_PATH):

        raise FileNotFoundError(
            "Job index not found. "
            "Run: python -m src.search.build_job_index"
        )


    if not os.path.exists(METADATA_PATH):

        raise FileNotFoundError(
            "Job metadata not found. "
            "Run: python -m src.search.build_job_index"
        )


    index = faiss.read_index(
        INDEX_PATH
    )


    with open(
        METADATA_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        metadata = json.load(
            file
        )


    return index, metadata


# ============================================================
# SEARCH JOBS
# ============================================================

def search_jobs(
    resume_text,
    k=3
):

    # Load dataset vector index

    index, job_metadata = load_job_data()


    # Prevent searching for more jobs than available

    k = min(
        k,
        index.ntotal
    )


    # Convert resume into embedding

    query_embedding = get_embedding(
        resume_text
    )


    query_embedding = np.array(
        [query_embedding],
        dtype="float32"
    )


    # Semantic FAISS search

    distances, indices = index.search(
        query_embedding,
        k
    )


    results = []


    # ========================================================
    # BUILD RESULTS
    # ========================================================

    for distance, idx in zip(
        distances[0],
        indices[0]
    ):

        if idx < 0:

            continue


        job = job_metadata[idx]


        results.append(
            {
                "job": job.get(
                    "job_title",
                    "Unknown Job"
                ),

                "company": job.get(
                    "company_name",
                    "Unknown Company"
                ),

                "city": job.get(
                    "city",
                    ""
                ),

                "state": job.get(
                    "state",
                    ""
                ),

                "country": job.get(
                    "country",
                    ""
                ),

                "job_type": job.get(
                    "job_type",
                    ""
                ),

                "category": job.get(
                    "category",
                    ""
                ),

                "description": job.get(
                    "job_description",
                    ""
                ),

                "url": job.get(
                    "url",
                    ""
                ),

                "distance": float(
                    distance
                )
            }
        )


    return results