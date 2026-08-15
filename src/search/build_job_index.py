import os
import json
import pandas as pd
import numpy as np
import faiss

from src.vectorstore.embedder import get_embedding


# ============================================================
# PATHS
# ============================================================

DATASET_PATH = "data/jobs/naukri_jobs.ldjson"

INDEX_PATH = "vectorstore/jobs.index"

METADATA_PATH = "vectorstore/jobs_metadata.json"


# ============================================================
# LOAD DATASET
# ============================================================

print("Loading Naukri job dataset...")

df = pd.read_json(
    DATASET_PATH,
    lines=True
)

print(f"Total jobs loaded: {len(df)}")


# ============================================================
# SELECT REQUIRED COLUMNS
# ============================================================

required_columns = [
    "job_title",
    "company_name",
    "city",
    "state",
    "country",
    "job_description",
    "job_type",
    "category",
    "url"
]

for column in required_columns:

    if column not in df.columns:

        raise ValueError(
            f"Required column not found: {column}"
        )


df = df[required_columns].copy()


# ============================================================
# CLEAN DATA
# ============================================================

df = df.fillna("")


# Remove jobs without title

df = df[
    df["job_title"].astype(str).str.strip() != ""
]


# Remove jobs without description

df = df[
    df["job_description"].astype(str).str.strip() != ""
]


# Remove duplicate jobs

df = df.drop_duplicates(
    subset=[
        "job_title",
        "company_name",
        "job_description"
    ]
)


df = df.reset_index(
    drop=True
)


print(f"Usable jobs after cleaning: {len(df)}")


# ============================================================
# CREATE JOB TEXT FOR EMBEDDING
# ============================================================

texts = []

metadata = []


for _, row in df.iterrows():

    job_title = str(row["job_title"])

    company_name = str(row["company_name"])

    city = str(row["city"])

    state = str(row["state"])

    country = str(row["country"])

    job_description = str(
        row["job_description"]
    )

    job_type = str(row["job_type"])

    category = str(row["category"])

    url = str(row["url"])


    # This complete text is converted into an embedding.
    # Including title + category + description improves
    # semantic matching with the resume.

    job_text = f"""
Job Title: {job_title}
Company: {company_name}
Category: {category}
Job Type: {job_type}
Location: {city}, {state}, {country}

Job Description:
{job_description}
""".strip()


    texts.append(
        job_text
    )


    # Metadata is stored separately and shown later in Streamlit.

    metadata.append(
        {
            "job_title": job_title,
            "company_name": company_name,
            "city": city,
            "state": state,
            "country": country,
            "job_type": job_type,
            "category": category,
            "job_description": job_description,
            "url": url
        }
    )


# ============================================================
# CREATE EMBEDDINGS
# ============================================================

print()
print("Creating job embeddings...")
print("This may take some time for the first run.")


embeddings = []


for i, text in enumerate(texts):

    if i % 100 == 0 or i == len(texts) - 1:

        print(
            f"Processing job "
            f"{i + 1}/{len(texts)}"
        )


    embedding = get_embedding(
        text
    )


    embeddings.append(
        embedding
    )


# ============================================================
# CONVERT TO NUMPY ARRAY
# ============================================================

embeddings = np.array(
    embeddings,
    dtype="float32"
)


print()
print(
    f"Embedding shape: {embeddings.shape}"
)


# ============================================================
# CREATE FAISS INDEX
# ============================================================

dimension = embeddings.shape[1]


index = faiss.IndexFlatL2(
    dimension
)


index.add(
    embeddings
)


# ============================================================
# CREATE VECTORSTORE FOLDER
# ============================================================

os.makedirs(
    "vectorstore",
    exist_ok=True
)


# ============================================================
# SAVE FAISS INDEX
# ============================================================

faiss.write_index(
    index,
    INDEX_PATH
)


# ============================================================
# SAVE JOB METADATA
# ============================================================

with open(
    METADATA_PATH,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        metadata,
        file,
        ensure_ascii=False,
        indent=2
    )


# ============================================================
# SUCCESS MESSAGE
# ============================================================

print()
print("=" * 60)

print(
    "JOB VECTOR INDEX CREATED SUCCESSFULLY!"
)

print("=" * 60)

print(
    f"Total indexed jobs: {len(metadata)}"
)

print(
    f"Embedding dimension: {dimension}"
)

print(
    f"FAISS index saved to: {INDEX_PATH}"
)

print(
    f"Metadata saved to: {METADATA_PATH}"
)