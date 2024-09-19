from typing import Mapping

from app.domain.entities.messages import Chat, Message


def convert_messages_to_document(message: Message) -> dict:
    return {
        'oid': message.oid,
        'text': message.text.as_generic_type(),
        'created_at': message.created_at,
    }


def convert_entity_to_document(chat: Chat) -> dict:
    return {
        'oid': chat.oid,
        'title': chat.title.as_generic_type(),
        'created_at': chat.created_at,
        'messages': [convert_messages_to_document(message) for message in chat.messages],
    }


def convert_chat_document_to_entity(chat_document: Mapping) -> Chat:
    ...
