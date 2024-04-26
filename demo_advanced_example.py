# https://docs.myshell.ai/product-manual/create/pro-config-mode-beta/tutorial/an-advanced-example

from myshell import *
from enum import Enum


class States(Enum):
    home_page_state = 1
    quiz_page_state = 2
    analyze_answer_state = 3
    correct_answer_state = 4
    wrong_answer_state = 5
    continue_state = 6
    finish_state = 7
    review_state = 8
    chat_page_state = 9


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


class QuizPageState:
    def __init__(self) -> None:
        self._state = AtomicState(name=States.quiz_page_state)

    def build(self):
        # --------- render
        render = Render()
        render.add_text(
            "{{context.question_idx + 1}}. {{context.questions[context.question_idx]['question']}}"
        )

        for option in ["A", "B", "C", "D"]:
            event = Event(event="check_answer", payload={"chosen_answer": f"{option}"})
            render.add_button(
                Button(content=f"{option}.", description=f"Choose {option}.", on_click=event)
            )
            
        self._state.render(render)
        # --------- end render
        
        target = TransitTarget(target = )

        
        
