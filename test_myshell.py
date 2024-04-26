from myshell import *
import json
from proconfig_quiz import home_state,quiz_state,analyze_answer_state


def test_render():

    render = Render()
    render.add_text("Hello World! Welcome to this demo. Click 'Start' to chat!")

    btn1 = Button(content="Start", description="Click to Start.", on_click="start_demo")
    render.add_button(btn1)

    event = Event(event="check_answer", payload={"chosen_answer": "B"})
    btn2 = Button(content="B", description="Choose B", on_click=event)
    render.add_button(btn2)

    print(json.dumps(render.to_dict(), indent=4))


def test_atomic_state():
    state = AtomicState(name="home_page_state")
    state.transit(trigger="start_demo", new_state="home_page_state")

    # ------- create render
    render = Render()
    render.add_text("Hello World! Welcome to this demo. Click 'Start' to chat!")

    btn = Button(content="Start", description="Click to Start.", on_click="start_demo")
    render.add_button(btn)
    # ------- END create render

    state.render(render)

    print(json.dumps(state.to_dict(), indent=4))


class TestAtomicState1:
    def __init__(self) -> None:
        self._state = AtomicState(name="home_page_state")

    def __add_inputs(self):
        intro_message = Input(
            name="intro_message",
            type=InputType.text,
            user_input=True,
            default_value="Hi, this is your Pro Config Tutorial Bot",
        )
        self._state.add_input(intro_message)

        tts_widget_url = Input(
            name="tts_widget_url",
            type=InputType.text,
            user_input=True,
            default_value="https://app.myshell.ai/widget/mEjUNr",
        )
        self._state.add_input(tts_widget_url)

    def __add_outputs(self):
        self._state.add_output(name="intro_message", value="intro_message", store_context=False)
        self._state.add_output(name="voice_id", value="tts_widget_url", store_context=False)

    def __render(self):
        render = Render()
        render.add_text("Hello World! Welcome to this demo. Click 'Start' to chat!")

        btn = Button(content="Start", description="Click to Start.", on_click="start_demo")
        render.add_button(btn)

        self._state.render(render)

    def __add_transitions(self):
        self._state.transit(trigger="start_demo", new_state="home_page_state")

    def run(self):
        """inputs -> tasks -> outputs -> render"""
        self.__add_inputs()
        self.__add_outputs()
        self.__render()
        self.__add_transitions()

        automata = Automata(name="hello_demo")
        automata.add_state(self._state, initial=True)

        automata.compile("temp.json")


class States(Enum):
    state1 = 1
    state2 = 2
    state3 = 3


def test_transition():
    state = AtomicState(States.state1)

    state.transit(trigger="x1", new_state="yyy")
    state.transit(trigger="x2", new_state=States.state3)

    condition = ConditionTransit()
    condition.append(target="c1", condition="c2")
    condition.append(target="c3", condition="c4")
    state.transit(trigger="x3", new_state=condition)

    target = TransitTarget(target="tt", target_inputs={"a": "b"})
    state.transit(trigger="x8", new_state=target)

    print(json.dumps(state.to_dict(), indent=2))


def test_proconfig_quize_states():
    # builder = home_state.HomepageState()
    # builder = quiz_state.QuizPageState()
    builder = analyze_answer_state.ContinueState()

    state = builder.build()
    print(json.dumps(state.to_dict(), indent=2))


if __name__ == "__main__":
    # test_render()
    # test_transition()
    # test_atomic_state()
    # TestAtomicState1().run()
    test_proconfig_quize_states()
