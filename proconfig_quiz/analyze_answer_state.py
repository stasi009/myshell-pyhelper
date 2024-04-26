# https://docs.myshell.ai/product-manual/create/pro-config-mode-beta/tutorial/an-advanced-example

from myshell import *
from proconfig_quiz.constants import States


class AnalyzeAnswerState:
    def __init__(self) -> None:
        self._state = AtomicState(States.analyze_answer_state)

    def build(self):
        self._state.add_input(
            Input(name="chosen_answer", type=InputType.text, user_input=False)  # set in quiz_state
        )

        self._state.add_output(name="chosen_answer", value="chosen_answer", store_context=True)
        self._state.add_output(
            name="is_correct", value="{{chosen_answer == context.correct_answer}}", store_context=True
        )

        render = Render()
        render.add_text("Check answer state.")
        self._state.render(render)

        conditions = ConditionTransit()
        conditions.append(target=States.correct_answer_state, condition="{{context.is_correct}}")
        conditions.append(
            target=States.wrong_answer_state, condition="{{true}}"
        )  # if not correct, this second condition will always match
        # ALWAYS: triggered when an AtomicState has finished. Usually used to connect two consecutive states.
        self._state.transit(trigger=Trigger.ALWAYS, new_state=conditions)

        return self._state


class CorrectAnswerState:
    def __init__(self) -> None:
        self._state = AtomicState(States.correct_answer_state)

    def build(self):
        self._state.add_output(
            name="question_idx",
            value="{{(context.question_idx + 1) % context.questions.length}}",
            store_context=True,
        )
        self._state.add_output(
            name="correct_count", value="{{context.correct_count + 1}}", store_context=True
        )

        render = Render()
        render.add_text("Congratulations! You have chosen the correct answer {{context.correct_answer}}")
        render.add_button(Button(content="Continue", description="continue", on_click="continue"))
        
        return self._state


class WrongAnswerState:
    def __init__(self) -> None:
        self._state = AtomicState(States.wrong_answer_state)

    def build(self):
        self._state.add_output(
            name="question_idx",
            value="{{(context.question_idx + 1) % context.questions.length}}",
            store_context=True,
        )

        render = Render()
        render.add_text("Oh No! The chosen answer is {{context.chosen_answer}}, while the correct one is {{context.correct_answer}}.",)
        render.add_button(Button(content="Continue", description="continue", on_click="continue"))
        
        return self._state