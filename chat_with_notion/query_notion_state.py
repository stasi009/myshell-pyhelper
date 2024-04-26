from myshell import *
from chat_with_notion.constants import States
from myshell import Render


class QueryNotionState(StateBuilderBase):
    def __init__(self) -> None:
        super().__init__(States.query_notion)

    def _add_inputs(self):
        _input = Input(
            name="notion_url",
            type=InputType.text,
            user_input=False,
            default_value="https://myshellai.notion.site/7f0dc468d15a4810ac9a1caa7799da7a?v=a8830827ab584b70b939015d9e76bbb2&pvs=4",
        )
        self._state.add_input(_input)

    def _add_tasks(self):
        self._state.add_task(
            Module(
                name="query_notion",
                module_type=ModuleType.AnyWidgetModule,
                module_config={
                    "widget_id": "1782389035948912640",
                    "url": "{{notion_url}}",
                    "action": "query_all",
                    "output_name": "notion_content",
                },
            )
        )

    def _add_outputs(self):
        self._state.add_output(
            name="notion_content", value="{{JSON.stringify(notion_content)}}", store_context=True
        )

    def _render(self, render: Render):
        render.add_text("{{JSON.stringify(notion_content)}}")
        render.add_button(Button(content="Chat", description="", on_click="chat"))

    def _add_transitions(self):
        self._state.transit(trigger="chat", new_state=States.chat_notion)
