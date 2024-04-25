"""
https://docs.myshell.ai/product-manual/create/pro-config-mode-beta/tutorial/transitions
"""

from myshell import *  

class HomepageState:
    def __init__(self) -> None:
        self._state = AtomicState(name='home_page_state')
        
    def build(self):
        render = Render()
        render.add_text("Click 'Start' to chat!")
        render.add_button(Button(
            content="Start Chat",
            description="Click to Start Chatting.",
            on_click="start_chat"
        ))
        self._state.render(render)
        
        self._state.transit(action="start_chat",new_state='intro_message_state')
        
class IntroMessageState:
    def __init__(self) -> None:
        self._state = AtomicState(name='intro_message_state')
        
    def build(self):
        render = Render()
        render.add_text("Hi, welcome to the Pro Config tutorial. How can I assist you today?")
        render.add_button(Button(
            content= "Home",
            description="Click to Go Back to Home.",
            on_click="go_home"
        ))
        self._state.render(render)
        
        self._state.transit(action="start_chat",new_state='intro_message_state')
        