from myshell import *   
from chat_with_notion.constants import States
from myshell import Render

class QueryNotionState(StateBuilderBase):
    def __init__(self) -> None:
        super().__init__(States.QueryNotion)
        
    def _add_inputs(self):
        _input = Input(
            name='notion_url',
            type=InputType.text,
            user_input=False,
            default_value="https://myshellai.notion.site/7f0dc468d15a4810ac9a1caa7799da7a?v=a8830827ab584b70b939015d9e76bbb2&pvs=4"
        )
        self._state.add_input(_input)
        
    def _render(render: Render):
        render.add_text("{{notion_url}}")