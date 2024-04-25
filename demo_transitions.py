"""
https://docs.myshell.ai/product-manual/create/pro-config-mode-beta/tutorial/transitions
"""

from enum import Enum
from myshell import *


class States(Enum):
    home_page_state = 1
    intro_message_state = 2
    chat_page_state = 3


class HomepageState:
    def __init__(self) -> None:
        self._state = AtomicState(name=States.home_page_state)

    def build(self):
        render = Render()
        render.add_text("Click 'Start' to chat!")
        render.add_button(
            Button(content="Start Chat", description="Click to Start Chatting.", on_click="start_chat")
        )
        self._state.render(render)

        self._state.transit(action="start_chat", new_state=States.intro_message_state)
        return self._state


class IntroMessageState:
    def __init__(self) -> None:
        self._state = AtomicState(States.intro_message_state)

    def build(self):
        render = Render()
        render.add_text("Hi, welcome to the Pro Config tutorial. How can I assist you today?")
        render.add_button(
            # transition for 'go_home' is defined in automata
            Button(content="Home", description="Click to Go Back to Home.", on_click="go_home")
        )
        self._state.render(render)

        self._state.transit(action=Action.CHAT, new_state=States.chat_page_state)
        return self._state


class ChatPageState:
    def __init__(self) -> None:
        self._state = AtomicState(States.chat_page_state)

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

    def __render(self):
        render = Render()
        render.add_text("{{reply}}")
        render.add_audio("{{reply_voice}}")
        render.add_button(
            # transition for 'go_home' is defined in automata
            Button(content="Home", description="Click to Go Back to Home.", on_click="go_home")
        )
        self._state.render(render)

    def build(self):
        self._state.add_input(Input(name="user_message", type=InputType.IM, user_input=True))
        self.__add_tasks()
        self.__render()
        self._state.transit(action=Action.CHAT, new_state=States.chat_page_state)
        return self._state


def main():
    automata = Automata("transition_demo")

    automata.add_state(HomepageState().build(), initial=True)
    automata.add_state(IntroMessageState().build(), initial=False)
    automata.add_state(ChatPageState().build(), initial=False)

    # Transition defined in the Automata, it will handle the actions in all its states
    automata.transit(action="go_home", new_state=States.home_page_state)

    automata.compile("temp.json")

if __name__ == "__main__":
    main()