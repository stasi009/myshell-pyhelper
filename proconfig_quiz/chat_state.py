from myshell import *
from proconfig_quiz.constants import States


class ChatPageState:
    def __init__(self) -> None:
        self._state = AtomicState(States.chat_page_state)

    def __add_tasks(self):
        self._state.add_task(
            Module(
                name="generate_reply",
                module_type=ModuleType.AnyWidgetModule,
                module_config={
                    "widget_id": "1744214024104448000",  # GPT-3.5
                    "system_prompt": "You are a teacher teaching Pro Config. Pro Config is a powerful tool to build AI native applications. Here are some questions and answers about basic concepts of Pro Config: {{context.questions_string}}",
                    "user_prompt": "{{user_message}}",
                    "memory": "{{context.memory}}",
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
                    "widget_id": "{{context.tts_widget_id}}",
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
        
        self._state.add_output(
            name="memory",
            value="{{[...context.memory, {'user': user_message}, {'assistant': reply}]}}",
            store_context=True,
        )

        self.__render()

        self._state.transit(trigger=Trigger.CHAT, new_state=States.chat_page_state)
        return self._state
