# https://docs.myshell.ai/product-manual/create/pro-config-mode-beta/tutorial/an-advanced-example

from myshell import *
from proconfig_quiz.constants import States


class QuizPageState:
    def __init__(self) -> None:
        self._state = AtomicState(name=States.quiz_page_state)

    def build(self):
        self._state.add_output(name='correct_answer',
                               value="{{context.questions[context.question_idx]['answer']}}",
                               store_context=True)
        
        # --------- render
        render = Render()
        render.add_text(
            "{{context.question_idx + 1}}. {{context.questions[context.question_idx]['question']}}"
        )

        for option in ["A", "B", "C", "D"]:
            event = Event(event="check_answer", payload={"chosen_answer": f"{option}"})
            render.add_button(Button(content=f"{option}.", description=f"Choose {option}.", on_click=event))

        self._state.render(render)
        # --------- end render

        target = TransitTarget(
            target=States.analyze_answer_state, target_inputs={"chosen_answer": "{{payload.chosen_answer}}"}
        )
        self._state.transit(trigger="check_answer", new_state=target)
        
        return self._state
