import random

embeddings_storage = []
_id_counter = 1

class CRUDEmbedding:
    def generate_for_ad(self, ad_id: int):
        global _id_counter
        # Here we will call an AI
        new_emb = {
            "id": _id_counter,
            "ad_id": ad_id,
            "vector": [random.uniform(-1, 1) for _ in range(6)]
        }
        embeddings_storage.append(new_emb)
        _id_counter += 1
        return new_emb

    def get_by_ad(self, ad_id: int):
        return next((e for e in embeddings_storage if e["ad_id"] == ad_id), None)

embedding_service = CRUDEmbedding()