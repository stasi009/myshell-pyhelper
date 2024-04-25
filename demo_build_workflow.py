# https://docs.myshell.ai/product-manual/create/pro-config-mode-beta/tutorial/building-workflow

from myshell import Button, Render, AtomicState, Input, Automata, Module, ModuleType,Action


class Builder:
    def __init__(self) -> None:
        self._automata = Automata(name="chat_demo")
        self._state = AtomicState(name="chat_page_state")

    def __add_inputs(self):
        input = Input(name="user_message", type="IM", user_input=True)
        self._state.add_input(input)

    def __add_tasks(self):
        self._state.add_task(
            Module(
                name="generate_reply",
                module_type=ModuleType.AnyWidget,
                module_config={
                    "widget_id": "1744214024104448000",
                    "system_prompt": "You are a teacher teaching Pro Config.",
                    "user_prompt": "{{user_message}}",
                    "output_name": "reply",
                }
            )
        )

        self._state.add_task(
            Module(
                name="generate_voice",
                module_type=ModuleType.AnyWidget,
                module_config={
                    "content": "{{reply}}",
                    "widget_id": "1743159010695057408",
                    "output_name": "reply_voice",
                }
            )
        )
        
    def __add_render(self):
        render = Render()
        render.add_text("{{reply}}")
        render.add_audio("{{reply_voice}}")
        self._state.render(render)
        
    def __add_transition(self):
        self._state.transit(Action.CHAT,"chat_page_state")
