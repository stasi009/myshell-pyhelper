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


@dataclass
class Input:
    name: str
    # 'text': user will be prompted to input data
    # 'IM' : user needs to type in the chat to provide an input.
    type: str
    # If user_input is false, user will not be prompted to input via a form,
    # a new variable with the value of default_value will be automatically generated
    user_input: bool
    default_value: str

    def __post_init__(self):
        if self.type not in ("text", "IM"):
            raise ValueError("input type can only be text or IM")

    def value_dict(self) -> dict[str, Any]:
        d = asdict(self)
        del d["name"]
        return d


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

    @property
    def name(self) -> str:
        return self.__name

    def transit(self, action, new_state):
        self.__transitions[action] = new_state

    def input(self, input: Input) -> None:
        self.__inputs[input.name] = input.value_dict()

    def output(self, name: str, value: str, store_context: bool) -> None:
        if store_context:
            name = "context." + name
        self.__outputs[name] = "{{" + value + "}}"

    def to_dict(self) -> dict[str, Any]:
        """ inputs -> tasks -> outputs -> render
        """
        return {
            "inputs": self.__inputs,
            "tasks": self.__tasks,
            "outputs": self.__outputs,
            "render": self.__render.to_dict(),
            "transitions": self.__transitions,
        }
