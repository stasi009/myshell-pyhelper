from myshell import *
from chat_with_notion.query_notion_state import QueryNotionState
from chat_with_notion.constants import States


def main():
    automata = Automata("chat_with_notion")


    for state_cls in [
        QueryNotionState
    ]:
        automata.add_state(state=state_cls().build(), initial=state_cls is QueryNotionState)

    automata.compile(Path(__file__).with_suffix(".json"))


if __name__ == "__main__":
    main()
