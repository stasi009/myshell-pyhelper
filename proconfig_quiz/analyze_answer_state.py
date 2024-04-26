# https://docs.myshell.ai/product-manual/create/pro-config-mode-beta/tutorial/an-advanced-example

from myshell import *
from proconfig_quiz.constants import States

class AnalyzeAnswerState:
    def __init__(self) -> None:
        self._state = AtomicState(States.analyze_answer_state)
        
    def build(self):
        self._state.add_input(Input(
            name="chosen_answer",# set in quiz_state
            type=InputType.text,
            user_input=False
        ))
        
        self._state.add_output(name='chosen_answer',value="chosen_answer",store_context=True)
        self._state.add_output(name='is_correct',value="{{chosen_answer == context.correct_answer}}",store_context=True)
        
        render = Render()
        render.add_text("Check answer state.")
        self._state.render(render)
        
        conditions = ConditionTransit()
        conditions.append(target=States.correct_answer_state,condition="{{context.is_correct}}")
        conditions.append(target=States.wrong_answer_state,condition="{{true}}")# if not correct, this second condition will always match
        # ALWAYS: triggered when an AtomicState has finished. Usually used to connect two consecutive states.
        self._state.transit(trigger=Trigger.ALWAYS,new_state=conditions)
        
        return self._state
        