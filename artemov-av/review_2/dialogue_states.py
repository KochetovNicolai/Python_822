from abc import ABC
from bot_database import *
from imdb_api_handler import *


class Response:
    def __init__(self, next_state, response=''):
        self.response = response
        self.next_state = next_state


class DialogueState(ABC):
    @staticmethod
    def handle_replica(replica, user_id):
        pass


class RootState(DialogueState):
    @staticmethod
    def handle_replica(replica, user_id):
        replica = replica.lower()
        response = None
        next_state = None
        if replica == 'find film':
            response = 'Enter the title'
            next_state = FindFilmState
        elif replica == 'add film in watched list':
            response = 'Enter the title'
            next_state = AddToWatchedListState
        elif replica == 'add film in wish list':
            response = 'Enter the title'
            next_state = AddToWishListState
        elif replica == 'show my watched list':
            response = '\n'.join(s[0] for s in BotDatabase().get_watched(user_id))
            next_state = RootState
            if response == '':
                response = 'Your watched list is empty'
        elif replica == 'show my wish list':
            response = '\n'.join(s[0] for s in BotDatabase().get_wished(user_id))
            next_state = RootState
            if response == '':
                response = 'Your wish list is empty'
        else:
            response = 'Didn\'t understand you :с'
            next_state = RootState

        return Response(next_state, response)


class FindFilmState(DialogueState):
    @staticmethod
    def handle_replica(replica, user_id):
        api_answer = ImdbApiHandler.find_film_by_name(replica)
        if api_answer.get('Response') is None:
            return Response(RootState, 'Failed to get info from IMDB')

        if api_answer['Response'] == 'False':
            return Response(RootState, 'Film was not found :c')
        elif api_answer.get('Title') is None:
            return Response(RootState, 'We lack information about this film')
        else:
            response = 'Title: ' + api_answer['Title'] + '\n'
            response += 'Year: ' + api_answer['Year'] + '\n' if api_answer.get('Year') is not None else ''
            response += 'Released: ' + api_answer['Released'] + '\n' if api_answer.get('Year') is not None else ''
            response += 'Genre: ' + api_answer['Genre'] + '\n' if api_answer.get('Year') is not None else ''
            response += 'Director: ' + api_answer['Director'] + '\n' if api_answer.get('Year') is not None else ''
            return Response(RootState, response)


class AddToWatchedListState(DialogueState):
    @staticmethod
    def handle_replica(replica, user_id):
        api_answer = ImdbApiHandler.find_film_by_name(replica)
        if api_answer.get('Response') is None:
            return Response(AddToWatchedListState, 'Failed to get info from IMDB')

        if api_answer['Response'] == 'False':
            return Response(AddToWatchedListState, 'Film was not found :c')
        elif api_answer.get('Title') is None or api_answer.get('Year') is None:
            return Response(AddToWatchedListState, 'We lack information about this film')
        else:
            BotDatabase().add_to_watched(user_id, api_answer['Title'])
            return Response(RootState, 'Added film in your watch list:\n' +
                            api_answer['Title'] + ' (' + api_answer['Year'] + ')')


class AddToWishListState(DialogueState):
    @staticmethod
    def handle_replica(replica, user_id):
        api_answer = ImdbApiHandler.find_film_by_name(replica)
        if api_answer.get('Response') is None:
            return Response(AddToWishListState, 'Failed to get info from IMDB')
        if api_answer.get('Title') is None or api_answer.get('Year') is None:
            return Response(AddToWishListState, 'We lack information about this film')

        if api_answer['Response'] == 'False':
            return Response(AddToWishListState, 'Film was not found :c')
        elif api_answer.get('Title') is None or api_answer.get('Year') is None:
            return Response(AddToWishListState, 'We lack information about this film')
        else:
            BotDatabase().add_to_wished(user_id, api_answer['Title'])
            return Response(RootState, 'Added film in your wish list:\n' +
                            api_answer['Title'] + ' (' + api_answer['Year'] + ')')
