from typing import (
    Any,
    Mapping,
)

from app.domain.entities.messages import (
    Chat,
    Message,
)


def convert_messages_to_document(message: Message) -> dict:
    return {
        'oid': message.oid,
        'text': message.text.as_generic_type(),
        'created_at': message.created_at,
    }


def convert_chat_to_document(chat: Chat) -> dict:
    return {
        'oid': chat.oid,
        'title': chat.title.as_generic_type(),
        'created_at': chat.created_at,
        'messages': [convert_messages_to_document(message) for message in chat.messages],
    }


def convert_message_document_to_entity(message_document: Mapping[str, Any]) -> Message:
    return Message(
        oid=message_document['oid'],
        text=message_document['text'],
        created_at=message_document['created_at'],
    )


def convert_chat_document_to_entity(chat_document: Mapping[str, Any]) -> Chat:
    return Chat(
        oid=chat_document['oid'],
        title=chat_document['title'],
        created_at=chat_document['created_at'],
        messages={
            convert_message_document_to_entity(message)
            for message in chat_document['messages']
        },
    )
