from myshell import Button, Render, AtomicState, Input, Automata
import json


def test_render():

    render = Render()
    render.add_text("Hello World! Welcome to this demo. Click 'Start' to chat!")

    btn = Button(content="Start", description="Click to Start.", on_click="start_demo")
    render.add_button(btn)

    print(json.dumps(render.to_dict(), indent=4))


def test_atomic_state():
    state = AtomicState(name="home_page_state")
    state.transit(action="start_demo", new_state="home_page_state")

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
            type="text",
            user_input=True,
            default_value="Hi, this is your Pro Config Tutorial Bot",
        )
        self._state.input(intro_message)

        tts_widget_url = Input(
            name="tts_widget_url",
            type="text",
            user_input=True,
            default_value="https://app.myshell.ai/widget/mEjUNr",
        )
        self._state.input(tts_widget_url)
        
    def __add_outputs(self):
        self._state.output(name='intro_message',value='intro_message',store_context=False)
        self._state.output(name='voice_id',value='tts_widget_url',store_context=False)
        
    def __render(self):
        render = Render()
        render.add_text("Hello World! Welcome to this demo. Click 'Start' to chat!")

        btn = Button(content="Start", description="Click to Start.", on_click="start_demo")
        render.add_button(btn)
        
        self._state.render(render)
        
    def __add_transitions(self):
        self._state.transit(action='start_demo',new_state='home_page_state')
        
    def run(self):
        """ inputs -> tasks -> outputs -> render
        """
        self.__add_inputs()
        self.__add_outputs()
        self.__render()
        self.__add_transitions()
        
        automata = Automata(name='hello_demo')
        automata.add_state(self._state,initial=True)
        
        automata.compile('temp.json')


if __name__ == "__main__":
    # test_render()
    # test_atomic_state()
    TestAtomicState1().run()
