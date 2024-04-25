from dataclasses import dataclass, asdict
from typing import Any
from pathlib import Path
import json
from enum import Enum


class ModuleType(Enum):
    AnyWidgetModule = 1
    LLMModule = 2
    LLMFunctionModule = 3
    TtsModule = 4
    GoogleSearchModule = 5


class Action(Enum):
    # triggered when the user sends a message
    CHAT = 1
    # triggered when an AtomicState has finished. Usually used to connect two consecutive states.
    ALWAYS = 2
    # triggered when an Automata is finished
    DONE = 3


class InputType(Enum):
    text = 1  # user will be prompted to input data
    IM = 2  # This allows the bot to take input in the form of messages sent to the bot.


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

    def add_audio(self, text: str):
        self._renders["audio"] = text

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
    type: InputType
    # If user_input is false, user will not be prompted to input via a form,
    # a new variable with the value of default_value will be automatically generated
    user_input: bool
    default_value: str = None

    def value_dict(self) -> dict[str, Any]:
        d = {
            "type": self.type.name,
            "user_input": self.user_input,
        }
        if self.default_value is not None:
            d["default_value"] = self.default_value
        return d


@dataclass
class Module:
    name: str
    module_type: ModuleType
    module_config: dict[str, str]

    def to_dict(self):
        return {
            "name": self.name,
            "module_type": self.module_type.name,
            "module_config": self.module_config,
        }


class ConditionTransition:
    def __init__(self) -> None:
        self._transits = []

    def append(self, target, condition):
        self._transits.append({"target": target, "condition": condition})

    @property
    def transition(self):
        return self._transits


class AtomicState:
    def __init__(self, name: str) -> None:
        self.__name = name
        self.__inputs = {}
        self.__outputs = {}
        self.__tasks = []  # Tasks contain multiple modules that execute sequentially
        self.__render: Render = None
        self.__transitions = {}

    @property
    def name(self) -> str:
        return self.__name

    def add_input(self, input: Input) -> None:
        self.__inputs[input.name] = input.value_dict()

    def add_task(self, module: Module):
        """Tasks contain multiple modules that execute sequentially"""
        self.__tasks.append(module.to_dict())

    def add_output(self, name: str, value: str, store_context: bool) -> None:
        if store_context:
            name = "context." + name
        self.__outputs[name] = "{{" + value + "}}"

    def render(self, render: Render) -> None:
        self.__render = render

    def transit(self, action, new_state):
        if isinstance(action, Action):
            action = action.name
        self.__transitions[action] = new_state

    def to_dict(self) -> dict[str, Any]:
        """inputs -> tasks -> outputs -> render"""
        return {
            "inputs": self.__inputs,
            "tasks": self.__tasks,
            "outputs": self.__outputs,
            "render": self.__render.to_dict(),
            "transitions": self.__transitions,
        }


class Automata:
    def __init__(self, name) -> None:
        self.__name = name
        self.__inputs = {}
        self.__outputs = {}
        self.__transitions = {}
        self.__states = {}

    def add_state(self, state: AtomicState, initial: bool) -> None:
        self.__states[state.name] = state.to_dict()
        if initial:
            self.__init_state = state.name

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "automata",
            "id": self.__name,
            "initial": self.__init_state,
            "inputs": {},
            "outputs": {},
            "transitions": {},
            "states": self.__states,
        }

    def compile(self, outfname: str | Path) -> None:
        with open(outfname, mode="wt") as fout:
            json.dump(self.to_dict(), fout, indent=2)
