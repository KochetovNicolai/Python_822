import dialogue_states
from dialogue_states import *
from bot_database import *
from singleton import Singleton


class BotLogic(metaclass=Singleton):
    def __init__(self):
        pass

    def handle_text_message(self, text, user_id):
        if BotDatabase().is_new_user(user_id):
            BotDatabase().insert_new_user(user_id, RootState.__name__)
        cur_state = getattr(dialogue_states, ''.join(BotDatabase().get_user_dialog_state(user_id)))
        response = cur_state.handle_replica(text, user_id)
        BotDatabase().set_user_dialog_state(user_id, response.next_state.__name__)
        return response.response

