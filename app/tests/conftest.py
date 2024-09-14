from pytest import fixture

from punq import Container

from app.infra.repositories.messages import BaseChatRepository
from app.logic import Mediator
from app.tests.fixtures import init_dummy_container


@fixture(scope='function')
def container() -> Container:
    return init_dummy_container()


@fixture(scope='function')
def mediator(container: Container) -> Mediator:
    return container.resolve(Mediator)


@fixture(scope='function')
def chat_repository(container: Container) -> BaseChatRepository:
    return container.resolve(BaseChatRepository)
