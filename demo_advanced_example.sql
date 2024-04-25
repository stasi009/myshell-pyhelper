# https://docs.myshell.ai/product-manual/create/pro-config-mode-beta/tutorial/an-advanced-example

from myshell import *   

class HomepageState:
    def __init__(self) -> None:
        self._state = AtomicState(name=States.home_page_state)

    def __add_inputs(self):
        self._state.add_input(
            Input(
                name="intro_message",
                type=InputType.text,
                user_input=True,
                default_value="Hi, this is your Pro Config Tutorial Bot, how can I assist you today",
            )
        )

        self._state.add_input(
            Input(
                name="tts_widget_id",
                type=InputType.text,
                user_input=True,
                default_value="1743159010695057408",
            )
        )

    def build(self):
        self.__add_inputs()

        for name in ["intro_message", "tts_widget_id"]:
            self._state.add_output(name=name, value=name, store_context=True)

        render = Render()
        render.add_text("Welcome to this demo. Click 'Start' to chat!")
        render.add_button(
            Button(content="Start Chat", description="Click to Start Chatting.", on_click="start_chat")
        )
        self._state.render(render)

        self._state.transit(action="start_chat", new_state=States.intro_message_state)
        return self._state