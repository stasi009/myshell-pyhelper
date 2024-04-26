from enum import Enum


class States(Enum):
    home_page_state = 1
    quiz_page_state = 2
    analyze_answer_state = 3
    correct_answer_state = 4
    wrong_answer_state = 5
    continue_state = 6
    finish_state = 7
    review_state = 8
    chat_page_state = 9