# pip install google-generativeai faiss-cpu

import google.generativeai as genai
import faiss
import os
import numpy as np
from typing import List
from dotenv import load_dotenv

load_dotenv()


genai.configure(api_key=os.getenv("GEMINIKEY"))

embedding_model = "models/embedding-001"
embedding_dim = 768


class VectorDB:
    def __init__(self):
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.id_map = []

    def get_embedding(self, text: str) -> List[float]:
        response = genai.embed_content(
            model=embedding_model,
            content=text,
            task_type="RETRIEVAL_QUERY"
        )
        return response["embedding"]


    def add_profile(self, profile_id: str, text: str):
        embedding = self.get_embedding(text)
        self.index.add(np.array([embedding]).astype('float32'))
        self.id_map.append(profile_id)

    def search(self, query: str, top_k=5):
        query_embedding = self.get_embedding(query)
        D, I = self.index.search(np.array([query_embedding]).astype('float32'), top_k)
        return [(self.id_map[i], float(D[0][j])) for j, i in enumerate(I[0]) if i < len(self.id_map)]


if __name__ == "__main__":
    db = VectorDB()

    db.add_profile("sonu", "Video editor for YouTube doctors, 5 years experience, edited 100+ videos.")
    db.add_profile("dellin", "Collaborated with social media creators on personal cinema and YouTube content.")

    results = db.search("YouTube video editor for medical content")
    for pid, score in results:
        print(f"Match: {pid} (Score: {score:.2f})")
