from time import time
from requests import get
from pathlib import Path
from hashlib import sha512
from tabulate import tabulate
from datetime import datetime
from random import SystemRandom
from webbrowser import open_new_tab
from string import ascii_lowercase, digits


def typeChecker(value, expected, canBeNone=False):
    '''
    Checks if value has wrong type. Raises TypeError if True.
    1)  value       : variable to check.
    2)  expected    : expected type of variable
    3)  canBeNone : accept the \"None\" variable value?
    '''
    if not (isinstance(value, expected) or (canBeNone and value is None)):
        raise TypeError('Founded type {}, \
                        expected {}'.format(value.__class__.__name__,
                                            expected.__name__))


def listTypeChecker(values, expected, canBeNone):
    '''
    Checks if any value in list has wrong type. Raises
    TypeError if False. Lists must have the same len.
    1)  values      : list. variables to check.
    2)  expected    : list. expected type of variable
    3)  canBeNone   : list. accept the \"None\" variable value?
    '''
    for i in range(len(values)):
        typeChecker(values[i], expected[i], canBeNone[i])


class CodeforcesEntity:
    '''
    Basic class for all Codeforces API responses.
    '''

    def __init__(self, json):
        '''
        Initializes user object by gived json. Json must be a dict
        object.
        '''
        typeChecker(json, dict)
        for name, value in json.items():
            setattr(self, name, value)


class User(CodeforcesEntity):
    '''
    Represents a Codeforces user.
    handle                  : str. Codeforces user handle.
    email                   : str. Shown only if user allowed to share
                                   his contact info.
    vkId                    : str. User id for VK social network. Shown
                                   only if user allowed to share his
                                   contact info.
    openId                  : str. Shown only if user allowed to share
                                   his contact info.
    firstName               : str. Localized. Can be absent.
    lastName                : str. Localized. Can be absent.
    country                 : str. Localized. Can be absent.
    city                    : str. Localized. Can be absent.
    organization            : str. Localized. Can be absent.
    contribution            : int. User contribution.
    rank                    : str. Localized.
    rating                  : int.
    maxRank                 : str. Localized.
    maxRating               : int.
    lastOnlineTimeSeconds   : int. Time, when user was last seen online,
                                   in unix format.
    registrationTimeSeconds : int. Time, when user was registered, in
                                   unix format.
    friendOfCount           : int. Amount of users who have this user
                                   in friends.
    avatar                  : str. User's avatar URL.
    titlePhoto              : str. User's title photo URL.
    '''
    pass


class BlogEntry(CodeforcesEntity):
    '''
    Represents a Codeforces blog entry. May be in either short or full
    version.
    id                      : int.
    originalLocale          : str. Original locale of the blog entry.
    creationTimeSeconds     : int. Time, when blog entry was created,
                                   in unix format.
    authorHandle            : str. Author user handle.
    title                   : str. Localized.
    content                 : str. Localized. Not included in short
                                   version.
    locale                  : str.
    modificationTimeSeconds : int. Time, when blog entry has been
                                   updated, in unix format.
    allowViewHistory        : bool. If True, you can view any specific
                                    revision of the blog entry.
    tags                    : str list.
    rating                  : int.
    '''
    pass


class Comment(CodeforcesEntity):
    '''
    Represents a comment.
    id                  : int.
    creationTimeSeconds : int. Time, when comment was created, in
                               unix format.
    commentatorHandle   : str.
    locale              : str.
    text                : str.
    parentCommentId     : int. Can be absent.
    rating              : int.
    '''
    pass


class RecentAction(CodeforcesEntity):
    '''
    Represents a recent action.
    timeSeconds : int. Action time, in unix format.
    blogEntry     : BlogEntry in short form. Can be absent.
    comment     : Comment. Can be absent.
    '''

    def __init__(self, json):
        super().__init__(json)
        if hasattr(self, 'blogEntry'):
            self.blogEntry = BlogEntry(self.blogEntry)
        if hasattr(self, 'comment'):
            self.comment = Comment(self.comment)


class RatingChange(CodeforcesEntity):
    '''
    Represents a participation of user in rated contest.
    contestId               : int.
    contestName             : str. Localized.
    handle                  : str. Codeforces user handle.
    rank                    : int. Place of the user in the contest.
                                   This field contains user rank on
                                   the moment of rating update. If
                                   afterwards rank changes (e.g.
                                   someone get disqualified), this
                                   field will not be update and will
                                   contain old rank.
    ratingUpdateTimeSeconds : int. Time, when rating for the contest
                                   was update, in unix-format.
    oldRating               : int. User rating before the contest.
    newRating               : int. User rating after the contest.
    '''
    pass


class Contest(CodeforcesEntity):
    '''
    Represents a contest on Codeforces.
    id                  : int.
    name                : str.  Localized.
    type                : Enum: CF, IOI, ICPC. Scoring system used for
                                the contest.
    phase               : Enum: BEFORE, CODING, PENDING_SYSTEM_TEST,
                                SYSTEM_TEST, FINISHED.
    frozen              : bool. If true, then the ranklist for the contest
                                is frozen and shows only submissions,
                                created before freeze.
    durationSeconds     : int.  Duration of the contest in seconds.
    startTimeSeconds    : int.  Can be absent. Contest start time in unix
                                format.
    relativeTimeSeconds : int.  Can be absent. Number of seconds, passed
                                after the start of the contest. Can be
                                negative.
    preparedBy          : str.  Can be absent. Handle of the user, how
                                created the contest.
    websiteUrl          : str.  Can be absent. URL for contest-related
                                website.
    description         : str.  Localized. Can be absent.
    difficulty          : int.  Can be absent. From 1 to 5. Larger number
                                means more difficult problems.
    kind                : str.  Localized. Can be absent. Human-readable
                                type of the contest from the following
                                categories:
                                Official ACM-ICPC Contest,
                                Official School Contest,
                                Opencup Contest,
                                School/University/City/Region Championship,
                                Training Camp Contest,
                                Official International Personal Contest,
                                Training Contest.
    icpcRegion          : str.  Localized. Can be absent. Name of the
                                ICPC Region for official ACM-ICPC contests.
    country             : str.  Localized. Can be absent.
    city                : str.  Localized. Can be absent.
    season              : str.  Can be absent.
    '''
    pass


class Member(CodeforcesEntity):
    '''
    Represents a member of a party.
    handle : str. Codeforces user handle.
    '''
    pass


class Party(CodeforcesEntity):
    '''
    Represents a party, participating in a contest.
    contestId           : int.  Can be absent. Id of the contest, in
                                which party is participating.
    members             : List of Member. Members of the party.
    participantType     : Enum: CONTESTANT, PRACTICE, VIRTUAL, MANAGER,
                                OUT_OF_COMPETITION.
    teamId              : int.  Can be absent. If party is a team,
                                then it is a unique team id. Otherwise,
                                this field is absent.
    teamName            : str.  Localized. Can be absent. If party is a
                                team or ghost, then it is a localized
                                name of the team. Otherwise, it is absent.
    ghost               : bool. If true then this party is a ghost. It
                                participated in the contest, but not on
                                Codeforces. For example, Andrew Stankevich
                                Contests in Gym has ghosts of the
                                participants from Petrozavodsk Training Camp.
    room                : int.  Can be absent. Room of the party. If absent,
                                then the party has no room.
    startTimeSeconds    : int.  Can be absent. Time, when this party started
                                a contest.
    '''

    def __init__(self, json):
        super().__init__(json)
        self.members = list(map(Member, self.members))


class Problem(CodeforcesEntity):
    '''
    Represents a problem.
    contestId       : int.   Can be absent. Id of the contest, containing
                             the problem.
    problemsetName  : str.   Can be absent. Short name of the problemset
                             the problem belongs to.
    index           : str.   Usually a letter of a letter, followed by a
                             digit, that represent a problem index in a
                             contest.
    name            : str.   Localized.
    type            : Enum:  PROGRAMMING, QUESTION.
    points          : float. Can be absent. Maximum ammount of points for
                             the problem.
    rating          : int.   Can be absent. Problem rating (difficulty).
    tags            : list of str objects. Problem tags.
    '''
    pass


class ProblemStatistics(CodeforcesEntity):
    '''
    Represents a statistic data about a problem.
    contestId   : int. Can be absent. Id of the contest, containing
                       the problem.
    index       : str. Usually a letter of a letter, followed by a digit,
                       that represent a problem index in a contest.
    solvedCount : int. Number of users, who solved the problem.
    '''
    pass


class Submission(CodeforcesEntity):
    '''
    Represents a submission.
    id                  : int.
    contestId           : int.  Can be absent.
    creationTimeSeconds : int.  Time, when submission was created,
                                in unix-format.
    relativeTimeSeconds : int.  Number of seconds, passed after the
                                start of the contest (or a virtual
                                start for virtual parties), before
                                the submission.
    problem             : Problem object.
    author              : Party object.
    programmingLanguage : str.
    verdict             : Enum: FAILED, OK, PARTIAL, COMPILATION_ERROR,
                                RUNTIME_ERROR, WRONG_ANSWER,
                                PRESENTATION_ERROR, TIME_LIMIT_EXCEEDED,
                                MEMORY_LIMIT_EXCEEDED,
                                IDLENESS_LIMIT_EXCEEDED, SECURITY_VIOLATED,
                                CRASHED, INPUT_PREPARATION_CRASHED,
                                CHALLENGED, SKIPPED, TESTING, REJECTED.
                                Can be absent.
    testset             : Enum: SAMPLES, PRETESTS, TESTS,
                                CHALLENGES, TESTS1, ..., TESTS10.
                                Testset used for judging the submission.
    passedTestCount     : int.  Number of passed tests.
    timeConsumedMillis  : int.  Maximum time in milliseconds, consumed by
                                solution for one test.
    memoryConsumedBytes : int.  Maximum memory in bytes, consumed by
                                solution for one test.
    '''

    def __init__(self, json):
        super().__init__(json)
        self.problem = Problem(self.problem)
        self.author = Party(self.author)


class Hack(CodeforcesEntity):
    '''
    Represents a hack, made during Codeforces Round.
    id                  : int.
    creationTimeSeconds : int.  Hack creation time in unix format.
    hacker              : Party object.
    defender            : Party object.
    verdict             : Enum: HACK_SUCCESSFUL, HACK_UNSUCCESSFUL,
                                INVALID_INPUT, GENERATOR_INCOMPILABLE,
                                GENERATOR_CRASHED, IGNORED, TESTING,
                                OTHER. Can be absent.
    problem             : Problem object. Hacked problem.
    test                : str.  Can be absent.
    judgeProtocol       : Object with three fields: "manual", "protocol"
                          and "verdict". Field manual can have values
                          "true" and "false". If manual is "true" then
                          test for the hack was entered manually. Fields
                          "protocol" and "verdict" contain human-readable
                          description of judge protocol and hack verdict.
                          Localized. Can be absent.
    '''

    def __init__(self, json):
        super().__init__(json)
        self.hacker = Party(self.hacker)
        self.defender = Party(self.defender)


class ProblemResult(CodeforcesEntity):
    '''
    Represents a submissions results of a party for a problem.
    points                      : float.
    penalty                     : int.  Penalty (in ICPC meaning) of
                                        the party for this problem.
    rejectedAttemptCount        : int.  Number of incorrect submissions.
    type                        : Enum: PRELIMINARY, FINAL. If type is
                                        PRELIMINARY then points can
                                        decrease (if, for example, solution
                                        will fail during system test).
                                        Otherwise, party can only increase
                                        points for this problem by submitting
                                        better solutions.
    bestSubmissionTimeSeconds   : int.  Number of seconds after the start of
                                        the contest before the submission,
                                        thatbrought maximal amount of points
                                        for this problem.
    '''
    pass


class RanklistRow(CodeforcesEntity):
    '''
    Represents a ranklist row.
    party                       : Party object. Party that took a
                                  corresponding place in the contest.
    rank                        : int.   Party place in the contest.
    points                      : float. Total ammount of points,
                                         scored by the party.
    penalty                     : int.   Total penalty (in ICPC meaning)
                                         of the party.
    successfulHackCount         : int.
    unsuccessfulHackCount       : int.
    problemResults              : List of ProblemResult objects.
                                  Party results for each problem.
                                  Order of the problems is the same
                                  as in "problems" field of the returned
                                  object.
    lastSubmissionTimeSeconds   : int.   For IOI contests only. Time in
                                         seconds from the start of the
                                         contest to the last submission
                                         that added some points to the
                                         total score of the party.
    '''

    def __init__(self, json):
        super().__init__(json)
        self.party = Party(self.party)
        self.problemResults = list(map(ProblemResult,
                                       self.problemResults))


class CodeforcesAPI:
    '''
    A wrapper class for simple and convenient use of Codeforces.com
    API and page requests. You don't need to read any info about API
    if you don't need anything unusual to do with it.
    '''

    _site_link = 'http://codeforces.com/'
    _api_link = 'http://codeforces.com/api/'

    def __init__(self,
                 key=None,
                 secret=None,
                 lang='en'):
        '''
        Initialize a Codeforces wrapper for single user.
        key    : str. User API key from https://codeforces.com/settings/api
        secret : str. User API secret from https://codeforces.com/settings/api
        lang   : str. Local language for requests. Can be \"en\" or \"ru\"
        '''
        listTypeChecker([key, secret, lang],
                        [str, str, str],
                        [True, True, False])
        self._key = key
        self._secret = secret
        self.language = lang

    @property
    def language(self):
        return self.__lang

    @language.setter
    def language(self, value):
        if value == 'ru' or value == 'en':
            self.__lang = value
        else:
            raise TypeError('Language can be only \"en\" \
                             or \"ru\", not {}'.format(value))

    def _to_http(self, param, value):
        '''
        Convert param into HTTP format: param=value.
        '''
        if isinstance(value, list):
            value = ';'.join(map(str, value))
        else:
            value = str(value)
        return '{}={}'.format(param, value)

    def _sorted_str_kwargs(self, **kwargs):
        '''
        Returns list of params and values, sorted lexicographically.
        '''
        lst = list()
        for param, value in kwargs.items():
            if value is not None:
                lst.append(self._to_http(param, value))
        return sorted(lst)

    def _get_url(self, **kwargs):
        '''
        Create url by sorted lexicographically kwargs:
        param_1=value_1&param_2=value_2...param_n=value_n.
        '''
        return '&'.join(self._sorted_str_kwargs(**kwargs))

    def _url_api_request(self, method, **kwargs):
        '''
        Creates url for API request. Uses key and secret from
        https://codeforces.com/settings/api if provided.
        '''
        kwargs['lang'] = self.__lang
        if self._key is not None and self._secret is not None:
            kwargs['time'] = int(time())
            kwargs['apiKey'] = self._key
            rand = ''.join(SystemRandom().choice(ascii_lowercase +
                                                 digits) for i in range(6))
            sig = rand + sha512((rand + '/' + method + '?' +
                                 self._get_url(**kwargs) + '#' +
                                 self._secret).encode('utf-8')).hexdigest()
            kwargs['apiSig'] = sig
        return self._get_url(**kwargs)

    def _check_request(self, request):
        if request.ok is False:
            raise ConnectionError('Request status \
                                  is {}'.format(self.last_api.status_code))

    def request_api(self, method, **kwargs):
        '''
        Requests http://codeforces.com/api/<method_name> and returns
        json object with info from site. Type of method must be a
        string.
        Uses key and secret if provided. Make sure you have set
        correct system time.
        Checks the request.Response object for valid answer.
        Raises ConnectionError if request is not OK.
        Cryptographically secure.
        Creates last_api dict. Contains JSON with last API request result.
        Example: cf.request_api('user.info', handles=['tourist', 'Petr'])
        '''
        typeChecker(method, str)
        self.last_api = get(self._api_link +
                            method + '?' +
                            self._url_api_request(method, **kwargs))
        self._check_request(self.last_api)
        self.last_api = self.last_api.json()
        if self.last_api['status'] != 'OK':
            raise ConnectionError('Codeforces API error: \
                                  {}', self.last_api['comment'])
        return self.last_api

    def blogEntry_comments(self, blogEntryId):
        '''
        Codeforces API name: blogEntry.comments.
        Returns a list of Comment to the specified blog entry.
        blogEntry_id (Required): int. id of the blog entry. It can be
                                      seen in blog entry URL.
        Example: cf.blogEntry_comments(blogEntryId=79)
        '''
        typeChecker(blogEntryId, int)
        self.request_api('blogEntry.comments',
                         blogEntryId=blogEntryId)
        return list(map(Comment, self.last_api['result']))

    def blogEntry_view(self, blogEntryId):
        '''
        Codeforces API name: blogEntry.view.
        Returns BlogEntry.
        blogEntryId (Required): int. Id of the blog entry. It can be
                                     seen in blog entry URL.
        Example: cf.blogEntry_view(blogEntryId=79)
        '''
        typeChecker(blogEntryId, int)
        self.request_api('blogEntry.view',
                         blogEntryId=blogEntryId)
        return BlogEntry(self.last_api['result'])

    def contest_hacks(self, contestId):
        '''
        Codeforces API name: contest.hacks.
        Returns list of Hack in the specified contests. Full
        information about hacks is available only after some
        time after the contest end. During the contest user can
        see only own hacks.
        contestId (Required): int. Id of the contest. It is not the
                                   round number. It can be seen in
                                   contest URL.
                                   For example: .../contest/566/status
        Example: cf.contest_hacks(contestId=566)
        '''
        typeChecker(contestId, int)
        self.request_api('contest.hacks',
                         contestId=contestId)
        return list(map(Hack, self.last_api['result']))

    def contest_list(self, gym=False):
        '''
        Codeforces API name: contest.list.
        Returns information about all available contest as list of
        contest_ob. If this method is called not anonymously, then
        all available contests for a calling user will be returned
        too, including mashups and private gyms.
        gym : bool. If true - than gym contests are returned. Otherwide,
                    regular contests are returned.
        Example: cf.contest_list(gym=True)
        '''
        typeChecker(gym, bool)
        self.request_api('contest.list',
                         gym=gym)
        return list(map(Contest, self.last_api['result']))

    def contest_ratingChanges(self, contestId):
        '''
        Codeforces API name: contest.ratingChanges.
        Returns rating changes after the contest as list
        of RatingChange.
        contestId (Required): int. Id of the contest. It is not
                                    the round number. It can be
                                    seen in contest URL.
        Example: cf.contest_ratingChanges(contestId=566)
        '''
        typeChecker(contestId, int)
        self.request_api('contest.ratingChanges',
                         contestId=contestId)
        return list(map(RatingChange, self.last_api['result']))

    def contest_standings(self, contestId, from_row=None,
                          count=None, handles=None, room=None,
                          showUnofficial=None):
        '''
        Codeforces API name: contest.standings.
        Returns the description of the contest and the
        requested part of the standings as list of 3 lists:
        1)  List of Contest object.
        2)  List of Problem objects.
        3)  List of RanklistRow objects.
        contestId (Required): int. Id of the contest. It is not
                                    the round number. It can be
                                    seen in contest URL.
                                    For example: .../contest/566/status
        from_row (API: from) : int. 1-based index of the standings
                                    row to start the ranklist.
        count                : int. Number of standing rows to return.
        handles              : str or list of str. Semicolon-separated list
                                                   of handles. No more than
                                                   10000 handles is accepted.
        room                 : int. If specified, than only participants
                                    from this room will be shown in the
                                    result. If not — all the participants
                                    will be shown.
        showUnofficial       : bool. If true than all participants (virtual,
                                     out of competition) are shown.
                                     Otherwise, only official contestants
                                     are shown.
        Example: cf.contest_standings(contestId=566,
                                      from_row=1,
                                      count=5,
                                      showUnofficial=True)
        '''
        # NOTE: from is a keyword in Python.
        if isinstance(handles, str):
            handles = [handles]
        listTypeChecker([contestId, from_row, count,
                         handles, room, showUnofficial],
                        [int, int, int, list, int, bool],
                        [False, True, True, True, True, True])
        if handles is not None and len(handles) > 10000:
            raise TypeError('handles len is {}. \
                            Maximum: 10000'.format(len(handles)))
        kwargs = {
            'contestId': contestId,
            'from': from_row,
            'count': count,
            'handles': handles,
            'room': room,
            'showUnofficial': showUnofficial
        }
        self.request_api('contest.standings', **kwargs)
        return [Contest(self.last_api['result']['contest']),
                list(map(Problem, self.last_api['result']['problems'])),
                list(map(RanklistRow, self.last_api['result']['rows']))]

    def contest_status(self, contestId, handle=None,
                       from_sub=None, count=None):
        '''
        Codeforces API name: contest.status
        Returns submissions as list of Submission for specified contest.
        Optionally can return submissions of specified user.
        contestId (Required) : int. Id of the contest. It is not the
                                    round number. It can be seen in
                                    contest URL.
                                    For example: .../contest/566/status
        handle               : str. Codeforces user handle.
        from_sub (API: from) : int. 1-based index of the first submission
                                    to return.
        count                : int. Number of returned submissions.
        Example: cf.contest_status(contestId=566, from_sub=1, count=10)
        '''
        listTypeChecker([contestId, handle, from_sub, count],
                        [int, str, int, int],
                        [False, True, True, True])
        # NOTE: from is a keyword in Python.
        kwargs = {
            'contestId': contestId,
            'handle': handle,
            'from': from_sub,
            'count': count
        }
        self.request_api('contest.status', **kwargs)
        return list(map(Submission, self.last_api['result']))

    def problemset_problems(self, tags=None, problemsetName=None):
        '''
        Codeforces API name: problemset.problems.
        Returns all problems from problemset as list of two lists:
        1)  List of Problem objects.
        2)  List of ProblemStatistics objests.
        Problems can be filtered by tags.
        tags           : list of str. Semicilon-separated list of tags.
        problemsetName : str. Custom problemset's short name, like 'acmsguru'
        Example: cf.problemset_problems(tags=['implementation'])
        '''
        listTypeChecker([tags, problemsetName],
                        [list, str],
                        [True, True])
        self.request_api('problemset.problems',
                         tags=tags,
                         problemsetName=problemsetName)
        return [list(map(Problem,
                         self.last_api['result']['problems'])),
                list(map(ProblemStatistics,
                         self.last_api['result']['problemStatistics']))]

    def problemset_recent_status(self, count, problemsetName=None):
        '''
        Codeforces API name: problemset.recentStatus.
        Returns recent submissions as list of Submission objects.
        count (Required) : int. Number of submissions to return.
                                Can be up to 1000.
        problemsetName   : str. Custom problemset's short name,
                                like 'acmsguru'.
        Example: cf.problemset_recent_status(count=10)
        '''
        listTypeChecker([count, problemsetName],
                        [int, str],
                        [False, True])
        if count > 1000:
            raise TypeError('count is {}. Maximim: 1000'.format(count))
        self.request_api('problemset.recentStatus',
                         count=count,
                         problemsetName=problemsetName)
        return list(map(Submission, self.last_api['result']))

    def recentActions(self, maxCount):
        '''
        Codeforces API name: recentActions.
        Returns recent actions as list of RecentAction objects.
        maxCount (Required) : int. Number of recent actions to return.
                                   Can be up to 100.
        Example: cf.recentActions(maxCount=30)
        '''
        typeChecker(maxCount, int)
        if maxCount > 100:
            raise TypeError('maxCount is {}. Maximum: 100'.format(maxCount))
        self.request_api('recentActions', maxCount=maxCount)
        return list(map(RecentAction, self.last_api['result']))

    def user_blogEntries(self, handle):
        '''
        Codeforces API name: user.blogEntries.
        Returns a list of all user's blog entries as list
        of BlogEntry in short form.
        handle (Required) : Codeforces user handle.
        Example: cf.user_blogEntries(handle='Fefer_Ivan')
        '''
        typeChecker(handle, str)
        self.request_api('user.blogEntries', handle=handle)
        return list(map(BlogEntry, self.last_api['result']))

    def user_friends(self, onlyOnline=False):
        '''
        Codeforces API name: user.friends.
        Returns authorized user's friends as list of str.
        Using this method requires authorization.
        onlyOnline : bool. If true - only online friends
                           are returned. Otherwise, all
                           friends are returned.
        Example: cf.user_friends(onlyOnline=True)
        '''
        typeChecker(onlyOnline, bool)
        self.request_api('user.friends', onlyOnline=onlyOnline)
        return self.last_api['result']

    def user_info(self, handles):
        '''
        Codeforces API name: user.info.
        Returns information about one or several users as
        User or list of User.
        handles (Required) : str or list of str. Semicolon-separated
                                                 list of handles. No
                                                 more than 10000 handles
                                                 is accepted.
        Examples: cf.user_info(handles='tourist')
                  cf.user_info(handles=['DmitryH', 'Fefer_Ivan'])
        '''
        if isinstance(handles, str):
            handles = [handles]
        typeChecker(handles, list)
        if len(handles) > 10000:
            raise TypeError('handles len is {}. \
                            Maximum: 10000'.format(len(handles)))
        self.request_api('user.info',
                         handles=handles)
        if len(self.last_api['result']) == 1:
            return User(self.last_api['result'][0])
        else:
            return list(map(User, self.last_api['result']))

    def user_ratedList(self, active_only=False):
        '''
        Codeforces API name: user.ratedList.
        Returns the list users who have participated
        in at least one rated contest as list of
        User objects.
        active_only : bool. If true then only users,
                            who participated in rated
                            contest during the last
                            month are returned. Otherwise,
                            all users with at least one
                            rated contest are returned.
        Example: cf.user_ratedList(active_only=True)
        '''
        typeChecker(active_only, bool)
        self.request_api('user.ratedList', activeOnly=active_only)
        return list(map(User, self.last_api['result']))

    def user_rating(self, handle):
        '''
        Codeforces API name: user.rating.
        Returns rating history of the specified user as list
        of RatingChange objects.
        handle (Required) : str. Codeforces user handle.
        Example: cf.user_rating(handle='Fefer_Ivan')
        '''
        typeChecker(handle, str)
        self.request_api('user.rating',
                         handle=handle)
        return list(map(RatingChange, self.last_api['result']))

    def user_status(self, handle, from_sub=None, count=None):
        '''
        Codeforces API name: user.status.
        Returns submissions of specified user as list of
        Submission objects.
        handle (Required)   : str. Codeforces user handle.
        from_sub (API: from): int. 1-based index of the first
                                   submission to return.
        count               : int. Number of returned submissions.
        Example: cf.user_status(handle='Fefer_Ivan',
                                from_sub=1,
                                count=10)
        '''
        # NOTE: from is a keyword in Python
        listTypeChecker([handle, from_sub, count],
                        [str, int, int],
                        [False, True, True])
        kwargs = {
            'handle': handle,
            'from': from_sub,
            'count': count
        }
        self.request_api('user.status', **kwargs)
        return list(map(Submission, self.last_api['result']))


class ext_CodeforcesAPI(CodeforcesAPI):
    '''
    This class provides comfortable functionality
    for in-contest and problemset submissions.
    last_verdict           : Submission. Contains last result of request to
                                         get_lastVerdict.
    last_page              : str. Contains str with HTML page from last
                                  get_page request.
    last_contestStatements : list of str. Contains HTML page with all
                                          contest results. Result of last
                                          get_contestStatements.
    '''

    def __init__(self,
                 handle=None,
                 workingDir=None,
                 **kwargs):
        '''
        Initialize the extended wrapper.
        handle     : str. Your handle from Codeforces.
        workingDir : str. Absolute path to working directory.
                          If not provided, data will be saved
                          and founded in directory with this file.
        **kwargs   : Used for initialization of CodeforcesAPI.
        '''
        listTypeChecker([handle, workingDir],
                        [str, str],
                        [True, True])
        CodeforcesAPI.__init__(self, **kwargs)
        self._handle = handle
        self._workingDir = workingDir

    @property
    def get_workingDir(self):
        '''
        Returns current working directory.
        '''
        if self._workingDir is None:
            return str(Path(__file__).parent.absolute())
        else:
            return self._workingDir

    def _file_save(self, file, name):
        '''
        Saves file str as <name> in working directory.
        If workingDir is not provided, data will be
        save in directory with this file.
        '''
        with open(self.get_workingDir + '/' + name, 'w') as stream:
            stream.write(str(file))

    def _hack_format(self, succ, unsucc):
        '''
        Create str with hacks:
        +<succ>:-<unsucc>.
        '''
        if succ == 0:
            if unsucc == 0:
                return ''
            else:
                return '-' + str(unsucc)
        else:
            if unsucc == 0:
                return '+' + str(succ)
            else:
                return '+{}:-{}'.format(succ, unsucc)

    def _problem_format(self, problem):
        '''
        Create str with problem result.
        '''
        if problem.points != 0:
            return '+{:<2} ({:02d}:{:02d})'.format(problem.rejectedAttemptCount or '',
                                                   problem.bestSubmissionTimeSeconds // 3600,
                                                   problem.bestSubmissionTimeSeconds % 3600 // 60)
        elif problem.rejectedAttemptCount != 0:
            return '-{:<2}'.format(problem.rejectedAttemptCount)
        else:
            return ''

    def _party_format(self, party):
        '''
        Create string with handles of party members.
        '''
        return ', '.join(i.handle for i in party.members)

    def _problem_symb(self, num):
        '''
        Return symbols for problems: A, B, C...
        '''
        return [chr(ord('A') + i) for i in range(num)]

    def get_verdicts(self, handle, from_sub=1, count=10, mode='fancy_grid'):
        '''
        Get the table of latest verdicts of user.
        '''
        listTypeChecker([handle, from_sub, count, mode],
                        [str, int, int, str],
                        [False, False, False, False])
        self.last_verdict = self.user_status(handle=handle,
                                                from_sub=from_sub,
                                                count=count)

        if len(self.last_verdict):
            if self.language == 'en':
                cols = ['#', 'When', 'Who', 'Problem',
                        'Lang', 'Verdict', 'Time', 'Memory']
            else:
                cols = ['#', 'Когда', 'Кто', 'Задача',
                        'Язык', 'Вердикт', 'Время', 'Память']
            rows = []
            for tmp in self.last_verdict:
                rows.append([tmp.id,
                             datetime.fromtimestamp(
                                 tmp.creationTimeSeconds
                             ).strftime("%d.%m.%Y %H:%M"),
                             handle,
                             tmp.problem.name,
                             tmp.programmingLanguage,
                             tmp.verdict,
                             tmp.timeConsumedMillis,
                             int(tmp.memoryConsumedBytes / 1024 + 0.5)
                        ])
            return tabulate(rows, cols, tablefmt=mode)
        else:
            return ''

    def get_lastVerdict(self, handle=None, mode='fancy_grid'):
        '''
        Returns result of the latest user submission and return
        table by tabulate. You can choose mode for tabulate.
        If handle is None, provided handle used.
        '''
        if handle is None:
            handle = self._handle
        return self.get_verdicts(handle=handle,
                                 from_sub=1,
                                 count=1,
                                 mode=mode)

    def get_page(self, link, **params):
        '''
        Requests and returns HTML page by link with params:
        http://codeforces.com/<link>
        '''
        params['locale'] = self.language
        self.last_page = get(self._site_link + link, params=params)
        self._check_request(self.last_page)
        return self.last_page.text

    def get_problemStatement(self, num, sym):
        return self.get_page('contest/{}/problem/{}'.format(num, sym))

    def get_contestStatements(self, contestId):
        '''
        Get all problem statements from contest
        by contestId in HTML format.
        '''
        self.last_contestStatements = \
            self.get_page('contest/{}/problems'.format(contestId))
        return self.last_contestStatements

    def save_contestStatements(self, contestId):
        '''
        Save the webpage with contest statements
        in your working directory.
        '''
        self._file_save(self.get_contestStatements(contestId),
                        'statements{}.html'.format(contestId))

    def open_contestStatements(self, contestId):
        '''
        Opens the contest statements. If the
        statements are not saved, they will
        be downloaded.
        '''
        filename = self.get_workingDir + '/statements{}.html'.format(contestId)
        if not Path(filename).is_file():
            self.save_contestStatements(contestId)
        open_new_tab('file://' + filename)

    def contest_standingsTable(self, contestId, from_row=1,
                               count=100, mode='fancy_grid'):
        '''
        Get the contest standings by contestId and return table
        by tabulate. You can choose mode for tabulate.
        '''
        listTypeChecker([contestId, from_row, count, mode],
                        [int, int, int, str],
                        [True, False, False, False])
        request = self.contest_standings(contestId=contestId,
                                         from_row=from_row,
                                         count=count)[2]
        rows, cols = list(), list()
        if self.language == 'en':
            cols = ['#', 'Who', 'Hacks',
                    *self._problem_symb(len(request[0].problemResults)),
                    'Penalty']
        else:
            cols = ['#', 'Кто', 'Взломы',
                    *self._problem_symb(len(request[0].problemResults)),
                    'Пенальти']
        for i in request:
            rows.append([i.rank,
                         self._party_format(i.party),
                         self._hack_format(i.successfulHackCount,
                                           i.unsuccessfulHackCount),
                         *(self._problem_format(i.problemResults[j])
                           for j in range(len(i.problemResults))),
                         i.penalty])
        return tabulate(rows, cols, tablefmt=mode)
