from myshell import Button, Render, AtomicState
import json


def test_render():

    render = Render()
    render.add_text("Hello World! Welcome to this demo. Click 'Start' to chat!")

    btn = Button(content="Start", description="Click to Start.", on_click="start_demo")
    render.add_button(btn)

    print(json.dumps(render.to_dict(),indent=4))
    
def test_atomic_state():
    state = AtomicState(name='home_page_state')
    state.transit(action='start_demo',new_state='home_page_state')
    
    # ------- create render
    render = Render()
    render.add_text("Hello World! Welcome to this demo. Click 'Start' to chat!")

    btn = Button(content="Start", description="Click to Start.", on_click="start_demo")
    render.add_button(btn)
    # ------- END create render
    
    state.render(render)
    
    print(json.dumps(state.to_dict(),indent=4))

    
    


if __name__ == "__main__":
    # test_render()
    test_atomic_state()
