from myshell import *
from chat_with_notion.constants import States
from myshell import Render


class ChatNotionState(StateBuilderBase):
    def __init__(self) -> None:
        super().__init__(States.chat_notion)

    def _add_inputs(self):
        self._state.add_input(Input(name="user_message", type=InputType.IM, user_input=True))

    def _add_tasks(self):
        system_prompt = "You are given an address book which is in JSON format. Its content is as follow: \n{{context.notion_content}}.\n Please answer questions based on the content in this address book."

        task = Module(
            name="generate_reply",
            module_type=ModuleType.AnyWidgetModule,
            module_config={
                "widget_id": "1744214024104448000",  # GPT-3.5
                "system_prompt": system_prompt,
                "user_prompt": "{{user_message}}",
                "memory": "{{context.memory}}",
                "output_name": "reply",
            },
        )
        
        self._state.add_task(task)

    def _add_outputs(self):
        self._state.add_output(
            name="memory",
            value="{{[...context.memory, {'user': user_message}, {'assistant': reply}]}}",
            store_context=True,
        )

    def _render(self, render: Render):
        render.add_text("{{reply}}")
        
    def _add_transitions(self):
        self._state.transit(trigger=Trigger.CHAT, new_state=States.chat_notion)
