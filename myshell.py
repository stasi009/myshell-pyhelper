from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class Button:
    content: str
    description: str
    on_click: str


class Render:
    def __init__(self) -> None:
        self._renders = {}

    def add_text(self, text: str):
        self._renders["text"] = text

    def add_button(self, btn: Button):
        btn_list = None
        if "buttons" not in self._renders:
            btn_list = []
            self._renders["buttons"] = btn_list
        else:
            btn_list = self._renders["buttons"]
        btn_list.append(asdict(btn))

    def to_dict(self) -> dict[str, Any]:
        return self._renders


class AtomicState:
    def __init__(self, name: str) -> None:
        self.__name = name
        self.__inputs = {}
        self.__outputs = {}
        self.__tasks = []
        self.__render: Render = None
        self.__transitions = {}

    def render(self, render: Render) -> None:
        self.__render = render
        
    def name(self)->str: 
        return self.__name
    
    def transit(self,action, new_state):
        self.__transitions[action] = new_state

    def to_dict(self) -> dict[str, Any]:
        return {
            "inputs": self.__inputs,
            "outputs": self.__outputs,
            "tasks": self.__tasks,
            "render": self.__render.to_dict(),
            "transitions": self.__transitions,
        }
