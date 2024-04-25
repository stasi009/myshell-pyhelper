# https://docs.myshell.ai/product-manual/create/pro-config-mode-beta/tutorial/building-workflow

from myshell import Button, Render, AtomicState, Input, InputType, Automata, Module, ModuleType, Action


class Builder:
    def __init__(self) -> None:
        self._automata = Automata(name="chat_demo")
        self._state = AtomicState(name="chat_page_state")

    def __add_inputs(self):
        # IM: allows the bot to take input in the form of messages sent to the bot
        input = Input(name="user_message", type=InputType.IM, user_input=True)
        self._state.add_input(input)

    def __add_tasks(self):
        self._state.add_task(
            Module(
                name="generate_reply",
                module_type=ModuleType.AnyWidgetModule,
                module_config={
                    "widget_id": "1744214024104448000",
                    "system_prompt": "You are a teacher teaching Pro Config.",
                    "user_prompt": "{{user_message}}",
                    "output_name": "reply",
                },
            )
        )

        self._state.add_task(
            Module(
                name="generate_voice",
                module_type=ModuleType.AnyWidgetModule,
                module_config={
                    "content": "{{reply}}",
                    "widget_id": "1743159010695057408",
                    "output_name": "reply_voice",
                },
            )
        )

    def __add_render(self):
        render = Render()
        render.add_text("{{reply}}")
        render.add_audio("{{reply_voice}}")
        self._state.render(render)

    def __add_transitions(self):
        # CHAT: when a user sends a message, automata will jump into  chat_page_state and execute that state
        self._state.transit(Action.CHAT, "chat_page_state")

    def run(self):
        self.__add_inputs()
        self.__add_tasks()
        self.__add_render()
        self.__add_transitions()

        self._automata.add_state(self._state, initial=True)
        self._automata.compile("temp.json")


if __name__ == "__main__":
    Builder().run()
