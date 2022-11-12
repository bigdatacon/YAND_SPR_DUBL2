import abc
import json
from typing import Any, Optional

class BaseStorage:
    """получить состояние """
    @abc.abstractmethod
    def save_state(self, state : dict)->None:
        pass

    """установить состояние"""
    @abc.abstractmethod
    def retrieve_state(self) ->dict:
        pass

class JsonFileStorage():
    def __init__(self, file_path: Optional[str]= None):
        self.__file_path = file_path if file_path else 'state.json'

    def save_state(self, state : dict) ->None:
        with open(self.__file_path, 'w') as json_file:
            json.dump(state, json_file)

    def retrieve_state(self):
        try:
            with open(self.__file_path) as json_file:
                state = json.load(json_file)
        except:
            state = {}
        return state

class State:
    def __init__(self, storage=JsonFileStorage):
        self.__storage = storage

    def get_state(self, index) -> dict:
        return self.__storage.retrieve_state().get(index)

    def set_state(self, index:str, value:Any)->None:
        state = self.__storage.retrieve_state()
        state[index] = value
        self.__storage.save_state(state)


if __name__ == '__main__':
    example = State(JsonFileStorage())
    print(example.get_state('movies'))
    # print(example.set_state('movies', 7))






