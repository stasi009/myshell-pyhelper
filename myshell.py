
from dataclasses import dataclass,asdict
from typing import Any


@dataclass
class Button:
    content:str 
    description:str 
    on_click:str
    
    
class Render:
    def __init__(self) -> None:
        self._renders = {}
        
    def add_text(self,text:str):
        self._renders['text'] = text
        
    def add_button(self,btn: Button): 
        btn_list = None
        if "buttons" not in self._renders:
            btn_list = []
            self._renders['buttons'] = btn_list
        else:
            btn_list = self._renders['buttons']
        btn_list.append(asdict(btn))
        
    def to_dict(self):
        return self._renders

@dataclass
class State:
    name:str 
    inputs: dict[str,Any]
    outputs: dict[str,Any]
    tasks: list[Any]
    render: dict[str,Any]
    transitions:dict[str,str]
    

    
    

