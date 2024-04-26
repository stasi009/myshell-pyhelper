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


class Trigger(Enum):
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
class Event:
    event: str
    payload: dict[str, str]


@dataclass
class Button:
    content: str
    description: str = ""
    on_click: str | Event


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


class ConditionTransit:
    def __init__(self) -> None:
        # each condition is checked sequentially, so it must be a list
        self._transits = []

    def append(self, target, condition):
        _target = None
        match target:
            case str():
                _target = target
            case Enum():
                _target = target.name
            case _:
                raise TypeError("Unsupported Target Type")
        self._transits.append({"target": _target, "condition": condition})

    @property
    def transition(self):
        return self._transits


@dataclass
class TransitTarget:
    target: str | Enum
    target_inputs: dict[str, str]

    def __post_init__(self):
        if isinstance(self.target, Enum):
            self.target = self.target.name


class StateMachineBase:
    def __init__(self, name: str) -> None:
        self._name = name
        self._inputs = {}
        self._outputs = {}

        # If defined in an AtomicState, it will only handle the action triggered in that AtomicState
        # If defined in the Automata, it will handle the actions in all its states
        self._transitions = {}

    @property
    def name(self) -> str:
        return self._name

    def add_input(self, input: Input) -> None:
        self._inputs[input.name] = input.value_dict()

    def add_output(self, name: str, value: str, store_context: bool) -> None:
        """
        - Referring to a variable defined within an AutomicState:we can directly use variable name to refer to that variable
        - Passing a variable across different AutomicStates: must set store_context to be True
        """
        if store_context:
            name = "context." + name

        if not value.startswith("{{"):
            value = "{{" + value + "}}"

        self._outputs[name] = value

    def transit(self, trigger, new_state: str | Enum | ConditionTransit | TransitTarget) -> None:
        if isinstance(trigger, Trigger):
            trigger = trigger.name

        _new_state = None
        match new_state:
            case str():
                _new_state = new_state
            case Enum():
                _new_state = new_state.name
            case ConditionTransit():
                _new_state = new_state.transition
            case TransitTarget():
                _new_state = asdict(new_state)
            case _:
                raise TypeError("Unknown State Type")
        self._transitions[trigger] = _new_state


class AtomicState(StateMachineBase):
    def __init__(self, name: str | Enum) -> None:
        super().__init__(name.name if isinstance(name, Enum) else name)
        self.__tasks = []  # Tasks contain multiple modules that execute sequentially
        self.__render: Render = None

    def add_task(self, module: Module):
        """Tasks contain multiple modules that execute sequentially"""
        self.__tasks.append(module.to_dict())

    def render(self, render: Render) -> None:
        self.__render = render

    def to_dict(self) -> dict[str, Any]:
        """inputs -> tasks -> outputs -> render"""
        d = {
            "inputs": self._inputs,
            "tasks": self.__tasks,
            "outputs": self._outputs,
            "transitions": self._transitions,
        }

        if self.__render is not None:
            d["render"] = self.__render.to_dict()

        return d


class StateBuilderBase:
    def __init__(self, name: str | Enum) -> None:
        self._state = AtomicState(name)

    def _add_inputs(self):
        pass

    def _add_tasks(self):
        pass
    
    def _add_outputs(self):
        pass 
    
    def _render(self,render:Render):
        pass 
    
    def _add_transitions(self):
        pass

    def build(self):
        self._add_inputs()
        self._add_tasks()
        self._add_outputs()
        
        render = Render()
        self._render(render)
        self._state.render(render)
        
        self._add_transitions()
        
        return self._state


class Automata(StateMachineBase):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.__states = {}
        self.__context = {}

    def declare_global_var(self, name, value=""):
        self.__context[name] = value

    def add_state(self, state: AtomicState, initial: bool) -> None:
        self.__states[state.name] = state.to_dict()
        if initial:
            self.__init_state = state.name

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "automata",
            "id": self._name,
            "initial": self.__init_state,
            "inputs": self._inputs,
            "outputs": self._outputs,
            "context": self.__context,
            "transitions": self._transitions,
            "states": self.__states,
        }

    def compile(self, outfname: str | Path) -> None:
        with open(outfname, mode="wt") as fout:
            json.dump(self.to_dict(), fout, indent=2)
