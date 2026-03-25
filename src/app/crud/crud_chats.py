from datetime import datetime

chats_storage = []
messages_storage = []
_chat_id_gen = 1
_msg_id_gen = 1

class CRUDChat:
    def create_chat(self, ad_id: int, initiator_id: int):
        global _chat_id_gen
        new_chat = {
            "id": _chat_id_gen,
            "ad_id": ad_id,
            "initiator_id": initiator_id,
            "created_at": datetime.now()
        }
        chats_storage.append(new_chat)
        _chat_id_gen += 1
        return new_chat

    def add_message(self, chat_id: int, sender_id: int, content: str):
        global _msg_id_gen
        new_msg = {
            "id": _msg_id_gen,
            "chat_id": chat_id,
            "sender_id": sender_id,
            "content": content,
            "timestamp": datetime.now()
        }
        messages_storage.append(new_msg)
        _msg_id_gen += 1
        return new_msg

    def get_chat_history(self, chat_id: int):
        chat = next((c for c in chats_storage if c["id"] == chat_id), None)
        if chat:
            chat_copy = chat.copy()
            chat_copy["messages"] = [m for m in messages_storage if m["chat_id"] == chat_id]
            return chat_copy
        return None

chat_service = CRUDChat()