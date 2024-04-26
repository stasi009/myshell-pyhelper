from myshell import *
from proconfig_quiz.analyze_answer_state import *
from proconfig_quiz.chat_state import *
from proconfig_quiz.home_state import *
from proconfig_quiz.quiz_state import *


def main():
    automata = Automata("advanced_example_demo_rebuild")

    global_vars = {
        "questions_string": '[{"question": "Which of the following statements is not correct? \\n A. The execution of an Automata starts from the `initial` state. \\n B. An Automata can contain multiple AtomicStates. \\n C. Each AtomicState must define both inputs and outputs. \\n D. We can define transitions in either Automata or AtomicState.", "answer": "C", "explanation": "Both inputs and outputs in an AtomicState are optional."}, {"question": "You are building an AutomicState, please choose the correct order of execution: \\n A. inputs -> tasks -> outputs -> render \\n B. render -> inputs -> tasks -> outputs. \\n C. tasks -> inputs -> outputs -> render.  \\n D. render -> tasks -> inputs -> outputs", "answer": "A", "explanation": "The correct order is `inputs -> tasks -> outputs -> render`. Please refer to `Expressions and Variables`"}, {"question": "Which of the following expressions is not correct (assume all the variables exist)? \\n A. context.variable \\n B. variable \\n C. variable1 + variable2 \\n D. np.array(variable)", "answer": "D", "explanation": "Our expression supports JavaScript grammar."}]',
        "questions": "",
        "question_idx": "",
        "chosen_answer": "",
        "correct_answer": "",
        "correct_count": "",
        "memory": "{{[]}}",
        "is_correct": "{{false}}",
        "intro_message": "",
        "tts_widget_id": "",
    }
    for k, v in global_vars.items():
        automata.declare_global_var(k, v)

    # If defined in the Automata, it will handle the actions in all its states
    automata.transit("go_home", States.home_page_state)
    automata.transit("get_quiz", States.quiz_page_state)
    automata.transit("continue", States.continue_state)

    for state_cls in [
        HomepageState,
        QuizPageState,
        AnalyzeAnswerState,
        CorrectAnswerState,
        WrongAnswerState,
        ContinueState,
        FinishState,
        ReviewState,
        ChatPageState,
    ]:

        automata.add_state(state=state_cls().build(), initial=state_cls is HomepageState)

    automata.compile(Path(__file__).with_suffix(".json"))


if __name__ == "__main__":
    main()
