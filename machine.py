from transitions.core import Machine
from fsm import TocMachine
def create_machine():
    machine = TocMachine(
    states=["init","fsm_graph","choose_information","choose_city","weather","choose_news_numbers","news","sport","global","breaknews","society"
    ,"show_1_news","show_3_news","show_5_news","return"],
    transitions=[
        {
            "trigger": "advance",
            "source": "init",
            "dest": "fsm_graph",
            "conditions": "is_going_to_fsm_graph",
        },
        {
            "trigger": "advance",
            "source": "init",
            "dest": "choose_information",
            "conditions": "is_going_to_choose_information",
        },
        {
            "trigger": "advance",
            "source": "choose_information",
            "dest": "news",
            "conditions": "is_going_to_news",
        },
        {
            "trigger": "advance",
            "source": "choose_information",
            "dest": "choose_city",  
            "conditions": "is_going_to_choose_city",
        },
        {
            "trigger": "advance",
            "source": "choose_city",
            "dest": "weather",  
            "conditions": "is_going_to_weather",
        },
        {
            "trigger": "advance",
            "source": "weather",
            "dest": "choose_city",
            "conditions": "is_going_to_back_choose_city",
        },
        {
            "trigger": "advance",
            "source": "choose_information",
            "dest": "choose_news_numbers",
            "conditions": "is_going_to_choose_news_numbers",
        },
        {
            "trigger": "advance",
            "source": "choose_news_numbers",
            "dest": "show_1_news",
            "conditions": "is_going_to_show_1_news",
        },
        {
            "trigger": "advance",
            "source": "choose_news_numbers",
            "dest": "show_3_news",
            "conditions": "is_going_to_show_3_news",
        },
        {
            "trigger": "advance",
            "source": "choose_news_numbers",
            "dest": "show_5_news",
            "conditions": "is_going_to_show_5_news",
        },
        {
            "trigger": "advance",
            "source": "news",
            "dest": "sport",
            "conditions": "is_going_to_sport",
        },
        {
            "trigger": "advance",
            "source": "news",
            "dest": "global",
            "conditions": "is_going_to_global",
        },
        {
            "trigger": "advance",
            "source": "news",
            "dest": "breaknews",
            "conditions": "is_going_to_breaknews",
        },
        {
            "trigger": "advance",
            "source": "news",
            "dest": "society",
            "conditions": "is_going_to_society",
        },
        {
            "trigger": "advance",
            "source": ["fsm_graph","choose_information","weather","sport","global","breaknews","society","show_1_news","show_3_news","show_5_news"],
            "dest": "init",
            "conditions": "is_going_to_init",
        },
        {
            "trigger": "advance",
            "source": ["fsm_graph","weather","sport","global","breaknews","society","choose_news_numbers","show_1_news","show_3_news","show_5_news"],
            "dest": "choose_information",
            "conditions": "is_going_to_back_choose_information",
        },
        {
            "trigger": "advance",
            "source": ["fsm_graph","choose_information","choose_city","weather","choose_news_numbers","news","sport","global","breaknews","society"
    ,"show_1_news","show_3_news","show_5_news","return"],
            "dest": "init",
            "conditions": "is_going_to_return",
        },
    ],
    initial="init",
    auto_transitions=False,
    show_conditions=True,
    )
    return machine