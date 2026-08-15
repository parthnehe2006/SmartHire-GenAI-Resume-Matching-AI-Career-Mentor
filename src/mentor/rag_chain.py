import os
from pathlib import Path

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import faiss


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CAREER_NOTES_DIR = PROJECT_ROOT / "data" / "career_notes"

VECTORSTORE_DIR = PROJECT_ROOT / "vectorstore"

CAREER_INDEX_PATH = VECTORSTORE_DIR / "career_notes.index"

CAREER_FILES_PATH = VECTORSTORE_DIR / "career_notes_files.txt"


# --------------------------------------------------
# Embedding Model
# --------------------------------------------------

MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


# --------------------------------------------------
# Load Career Notes
# --------------------------------------------------

def load_career_notes():

    documents = []
    filenames = []

    if not CAREER_NOTES_DIR.exists():

        return documents, filenames

    for file_path in CAREER_NOTES_DIR.glob("*.md"):

        try:

            text = file_path.read_text(
                encoding="utf-8"
            )

            if text.strip():

                documents.append(text)
                filenames.append(file_path.name)

        except Exception as e:

            print(
                f"Could not read {file_path.name}: {e}"
            )

    return documents, filenames


# --------------------------------------------------
# Build Career Notes FAISS Index
# --------------------------------------------------

def build_career_notes_index():

    documents, filenames = load_career_notes()

    if not documents:

        print("No career notes found.")

        return False

    embeddings = model.encode(
        documents,
        convert_to_numpy=True
    ).astype("float32")

    index = faiss.IndexFlatL2(
        embeddings.shape[1]
    )

    index.add(embeddings)

    VECTORSTORE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    faiss.write_index(
        index,
        str(CAREER_INDEX_PATH)
    )

    with open(
        CAREER_FILES_PATH,
        "w",
        encoding="utf-8"
    ) as f:

        for filename in filenames:

            f.write(
                filename + "\n"
            )

    print(
        f"Career notes index created successfully!"
    )

    print(
        f"Total career notes: {len(documents)}"
    )

    return True


# --------------------------------------------------
# Load Existing Career Notes Index
# --------------------------------------------------

def load_career_notes_index():

    if not CAREER_INDEX_PATH.exists():

        print(
            "Career notes index not found."
        )

        print(
            "Building the index..."
        )

        success = build_career_notes_index()

        if not success:

            return None, []

    index = faiss.read_index(
        str(CAREER_INDEX_PATH)
    )

    filenames = []

    if CAREER_FILES_PATH.exists():

        with open(
            CAREER_FILES_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            filenames = [
                line.strip()
                for line in f
                if line.strip()
            ]

    return index, filenames


# --------------------------------------------------
# Retrieve Career Notes
# --------------------------------------------------

def retrieve_career_notes(
    query,
    k=3
):

    index, filenames = load_career_notes_index()

    if index is None:

        return []

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    ).astype("float32")

    k = min(
        k,
        index.ntotal
    )

    distances, indices = index.search(
        query_embedding,
        k
    )

    results = []

    for distance, idx in zip(
        distances[0],
        indices[0]
    ):

        if idx < 0:

            continue

        if idx >= len(filenames):

            continue

        filename = filenames[idx]

        file_path = (
            CAREER_NOTES_DIR / filename
        )

        try:

            content = file_path.read_text(
                encoding="utf-8"
            )

        except Exception:

            content = ""

        results.append(
            {
                "source": filename,
                "content": content,
                "distance": float(distance)
            }
        )

    return results


# --------------------------------------------------
# Test
# --------------------------------------------------

if __name__ == "__main__":

    print(
        "Testing Career Notes Retrieval..."
    )

    results = retrieve_career_notes(
        "How can I become a machine learning engineer?",
        k=3
    )

    if not results:

        print(
            "No career notes retrieved."
        )

    else:

        print(
            "\nTop Career Notes:\n"
        )

        for result in results:

            print(
                f"Source: {result['source']}"
            )

            print(
                f"Distance: {result['distance']:.4f}"
            )

            print(
                result["content"][:500]
            )

            print(
                "\n" + "-" * 60 + "\n"
            )