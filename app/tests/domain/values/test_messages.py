from datetime import datetime

import pytest
from faker import Faker

from app.domain.entities.messages import Message, Chat
from app.domain.events.messages import NewMessageReceivedEvent
from app.domain.exceptions.messages import TitleTooLongException
from app.domain.values.messages import Text, Title

fake = Faker()


@pytest.fixture
def valid_message():
    some_text = fake.text(max_nb_chars=200)
    text = Text(value=some_text)
    return Message(text=text)


def test_create_message_success(valid_message):
    message = valid_message

    assert isinstance(message.text.value, str)
    assert len(message.text.value) > 0
    assert message.created_at.date() == datetime.today().date()


def test_create_chat_success():
    title = Title(fake.text(max_nb_chars=100))
    chat = Chat(title=title)

    assert isinstance(chat.title.value, str)
    assert chat.title == title
    assert chat.created_at.date() == datetime.today().date()
    assert not chat.messages


def test_create_chat_too_long():
    with pytest.raises(TitleTooLongException):
        Title(fake.text(max_nb_chars=500))


def test_add_message_to_chat_success():
    text = Text(value=fake.text(max_nb_chars=200))
    message = Message(text=text)

    title = Title(fake.text(max_nb_chars=100))
    chat = Chat(title=title)

    chat.add_message(message)

    assert message in chat.messages


def test_new_message_events():
    text = Text(value=fake.text(max_nb_chars=10))
    message = Message(text=text)

    title = Title(fake.text(max_nb_chars=10))
    chat = Chat(title=title)

    chat.add_message(message)

    pulled_events = chat.pull_events()
    event = pulled_events[0]

    assert len(pulled_events) == 1, pulled_events
    assert isinstance(event, NewMessageReceivedEvent), event
    assert event.message_oid == message.oid
    assert event.message_text == message.text.as_generic_type()
    assert event.chat_oid == chat.oid

