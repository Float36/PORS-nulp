from datetime import datetime
from src.app.schemas.ad import AdCreate
from src.app.crud.crud_photos import photo_service
from src.app.crud.crud_embeddings import embedding_service

ads_storage = []
_id_counter = 1


class CRUDAd:
    def get_all(self):
        return [self._enrich_ad(ad) for ad in ads_storage]

    def get_by_id(self, ad_id: int):
        ad = next((ad for ad in ads_storage if ad["id"] == ad_id), None)
        return self._enrich_ad(ad) if ad else None

    def create(self, obj_in: AdCreate):
        global _id_counter
        new_ad = {
            **obj_in.model_dump(),
            "id": _id_counter,
            "created_at": datetime.now()
        }
        ads_storage.append(new_ad)

        photo_service.create_for_ad(_id_counter)
        embedding_service.generate_for_ad(_id_counter)

        _id_counter += 1
        return self._enrich_ad(new_ad)

    def _enrich_ad(self, ad: dict):
        ad_copy = ad.copy()
        ad_copy["photos"] = photo_service.get_by_ad(ad["id"])
        ad_copy["embedding"] = embedding_service.get_by_ad(ad["id"])
        return ad_copy


ad_service = CRUDAd()