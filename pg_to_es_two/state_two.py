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

class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: Optional[str]=None):
        self.__state_path = file_path if file_path else 'state.json'

    def save_state(self, state: dict) ->None:
        with open(self.__state_path, 'w') as json_file:
            json.dump(state, json_file)

    def retrieve_state(self) ->dict:
        try:
            with open(self.__state_path) as json_file:
                state = json.load(json_file)
        except:
            state = {}

        return state

class State:
    def __init__(self, storage: JsonFileStorage):
        self.storage = storage

    def set_state(self, index, value)->None:
        state = self.storage.retrieve_state()
        state[index]= value
        self.storage.save_state(state)

    def get_state(self) ->dict:
        state = self.storage.retrieve_state()
        return state


example = State(JsonFileStorage())
print(example.get_state())





