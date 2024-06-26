from myshell import *
from proconfig_quiz.constants import States


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

    def __add_outputs(self):
        # no tasks here, just define these outputs for initialization
        self._state.add_output(name="intro_message", value="intro_message", store_context=True)
        self._state.add_output(name="tts_widget_id", value="tts_widget_id", store_context=True)
        self._state.add_output(
            name="questions", value="JSON.parse(context.questions_string)", store_context=True
        )
        self._state.add_output(name="question_idx", value="0", store_context=True)
        self._state.add_output(name="correct_count", value="0", store_context=True)

    def build(self):
        self.__add_inputs()
        self.__add_outputs()

        render = Render()
        render.add_text("Welcome to this Pro Config tutorial bot. Let's start a quiz!")
        render.add_button(Button(content="Quiz", description="get_quiz", on_click="get_quiz"))
        self._state.render(render)

        return self._state
