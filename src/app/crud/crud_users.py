from src.app.schemas.user import UserCreate


users_storage = []
_id_counter = 1


class CRUDUsers:
    def get_all(self):
        return users_storage

    def get_by_id(self, user_id: int):
        return next((user for user in users_storage if user["id"] == user_id), None)

    def create(self, obj_in: UserCreate):
        global _id_counter
        # Modeling DB behavior
        new_user = {**obj_in.model_dump(), "id": _id_counter}
        users_storage.append(new_user)
        _id_counter += 1
        return new_user

user_service = CRUDUsers()