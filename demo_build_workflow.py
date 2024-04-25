
# https://docs.myshell.ai/product-manual/create/pro-config-mode-beta/tutorial/building-workflow

from myshell import Button, Render, AtomicState, Input, Automata

class Builder:
    def __init__(self) -> None:
        self._automata = Automata(name='chat_demo')