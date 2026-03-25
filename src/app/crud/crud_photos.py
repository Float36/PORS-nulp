photos_storage = []
_id_counter = 1

class CRUDPhoto:
    def create_for_ad(self, ad_id: int):
        global _id_counter
        new_photo = {
            "id": _id_counter,
            "ad_id": ad_id,
            "url": f"https://storage.lostfound.com/ads/{ad_id}/photo_{_id_counter}.jpg"
        }
        photos_storage.append(new_photo)
        _id_counter += 1
        return new_photo

    def get_by_ad(self, ad_id: int):
        return [p for p in photos_storage if p["ad_id"] == ad_id]

photo_service = CRUDPhoto()