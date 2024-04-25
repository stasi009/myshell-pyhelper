from myshell import Button, Render
import json


def test_render():

    render = Render()
    render.add_text("Hello World! Welcome to this demo. Click 'Start' to chat!")

    btn = Button(content="Start", description="Click to Start.", on_click="start_demo")
    render.add_button(btn)

    print(json.dumps(render.to_dict(),indent=4))


if __name__ == "__main__":
    test_render()
