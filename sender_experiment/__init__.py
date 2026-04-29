from otree.api import *
import random
import time


doc = """
Sender experiment with instructions followed by repeated decision screens.
"""


class C(BaseConstants):
    NAME_IN_URL = 'sender_experiment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 10
    RAVEN_SET_1 = [
        dict(question_id='Q2', correct_answer='R2'),
        dict(question_id='Q8', correct_answer='R1'),
        dict(question_id='Q11', correct_answer='R3'),
        dict(question_id='Q12', correct_answer='R3'),
        dict(question_id='Q15', correct_answer='R2'),
    ]
    RAVEN_SET_2 = [
        dict(question_id='Q17', correct_answer='R6'),
        dict(question_id='Q18', correct_answer='R5'),
        dict(question_id='Q24', correct_answer='R8'),
        dict(question_id='Q26', correct_answer='R4'),
        dict(question_id='Q30', correct_answer='R1'),
    ]
    RAVEN_SET_LABELS = dict(set1='Set 1', set2='Set 2')
    GENDER_CHOICES = ['Male', 'Female', 'Other/prefer not to say']
    EDUCATION_CHOICES = [
        'High School diploma',
        'Bachelors Degree',
        "Master's Degree or Above",
    ]
    AGE_CHOICES = list(range(18, 101))


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    sender_status = models.StringField()
    type_number = models.IntegerField()
    sent_message = models.LongStringField()
    raven_trial_1_selected = models.StringField(blank=True)
    raven_trial_1_correct = models.BooleanField(initial=False)
    raven_trial_1_rt_ms = models.IntegerField(blank=True)
    raven_trial_2_selected = models.StringField(blank=True)
    raven_trial_2_correct = models.BooleanField(initial=False)
    raven_trial_2_rt_ms = models.IntegerField(blank=True)
    raven_trial_3_selected = models.StringField(blank=True)
    raven_trial_3_correct = models.BooleanField(initial=False)
    raven_trial_3_rt_ms = models.IntegerField(blank=True)
    raven_trial_4_selected = models.StringField(blank=True)
    raven_trial_4_correct = models.BooleanField(initial=False)
    raven_trial_4_rt_ms = models.IntegerField(blank=True)
    raven_trial_5_selected = models.StringField(blank=True)
    raven_trial_5_correct = models.BooleanField(initial=False)
    raven_trial_5_rt_ms = models.IntegerField(blank=True)
    age = models.IntegerField(
        choices=C.AGE_CHOICES,
        blank=True,
    )
    gender = models.StringField(
        choices=C.GENDER_CHOICES,
        widget=widgets.RadioSelect,
        blank=True,
    )
    education = models.StringField(
        choices=C.EDUCATION_CHOICES,
        widget=widgets.RadioSelect,
        blank=True,
    )


def creating_session(subsession: Subsession):
    players = subsession.get_players()

    if subsession.round_number == 1:
        shuffled_players = players[:]
        random.shuffle(shuffled_players)
        split_index = len(shuffled_players) // 2

        for index, player in enumerate(shuffled_players):
            if len(shuffled_players) % 2 == 1 and index == len(shuffled_players) - 1:
                player.participant.raven_set_id = random.choice(['set1', 'set2'])
            else:
                player.participant.raven_set_id = 'set1' if index < split_index else 'set2'

            player.participant.raven_score = 0
            player.participant.sender_status = ''
            player.participant.raven_deadline = None
            player.participant.raven_complete = False

    for player in players:
        player.type_number = random.randint(1, 3)


INSTRUCTION_META = {
    'InstructionsWelcome': dict(
        section_title='Sender Experiment: Participant Instructions',
        section_subtitle='Instructions',
        progress_text='Screen 1 of 3',
        page_title='Welcome To The Study!',
    ),
    'InstructionsRole': dict(
        section_title='Sender Experiment: Participant Instructions',
        section_subtitle='Instructions',
        progress_text='Screen 2 of 3',
        page_title='Important Information',
    ),
    'InstructionsStatus': dict(
        section_title='Sender Experiment: Participant Instructions',
        section_subtitle='Instructions',
        progress_text='Screen 3 of 3',
        page_title='Part 1',
    ),
}


POST_RAVEN_META = {
    'Part2Transition': dict(
        section_title='Sender Experiment: Game Instructions',
        section_subtitle='Part 2',
        progress_text='Screen 1 of 3',
        page_title='Part 2',
    ),
    'GameInstructionsOverview': dict(
        section_title='Sender Experiment: Game Instructions',
        section_subtitle='Part 2',
        progress_text='Screen 2 of 3',
        page_title='Part 2',
    ),
    'GameInstructionsSets': dict(
        section_title='Sender Experiment: Game Instructions',
        section_subtitle='Part 2',
        progress_text='Screen 3 of 3',
        page_title='Description of the game: Each round of the game has 4 steps.',
    ),
}


RAVEN_FIELDS = {
    1: ('raven_trial_1_selected', 'raven_trial_1_correct', 'raven_trial_1_rt_ms'),
    2: ('raven_trial_2_selected', 'raven_trial_2_correct', 'raven_trial_2_rt_ms'),
    3: ('raven_trial_3_selected', 'raven_trial_3_correct', 'raven_trial_3_rt_ms'),
    4: ('raven_trial_4_selected', 'raven_trial_4_correct', 'raven_trial_4_rt_ms'),
    5: ('raven_trial_5_selected', 'raven_trial_5_correct', 'raven_trial_5_rt_ms'),
}


def instruction_context(page_name):
    context = dict(INSTRUCTION_META[page_name])
    screen_number = int(context['progress_text'].split()[1])
    context['progress_percent'] = round((screen_number / 3) * 100)
    context['countdown_seconds'] = None
    return context


def post_raven_context(page_name):
    context = dict(POST_RAVEN_META[page_name])
    screen_number = int(context['progress_text'].split()[1])
    context['progress_percent'] = round((screen_number / 3) * 100)
    context['countdown_seconds'] = None
    return context


DECISION_META = {
    'MessageDecision': (1, 'Secret Number'),
    'Part2Ended': (2, 'Part 2'),
    'Demographics': (3, 'Demographic Part'),
    'EndScreen': (4, ''),
}


def raven_trials_for_player(player: Player):
    raven_set_id = player.participant.raven_set_id or 'set1'
    if raven_set_id == 'set2':
        return C.RAVEN_SET_2
    return C.RAVEN_SET_1


def raven_time_remaining(player: Player):
    deadline = getattr(player.participant, 'raven_deadline', None)
    if not deadline:
        return 300
    return max(0, int(deadline - time.time()))


def current_sender_status(player: Player):
    participant_status = getattr(player.participant, 'sender_status', '') or ''
    stored_status = player.field_maybe_none('sender_status') or ''
    return participant_status or stored_status


def compute_raven_score(player: Player):
    return sum(
        1
        for _, correct_field, _ in RAVEN_FIELDS.values()
        if getattr(player, correct_field)
    )


def finalize_raven(player: Player):
    score = compute_raven_score(player)
    player.participant.raven_score = score
    player.participant.sender_status = 'High Status' if score > 2 else 'Low Status'
    player.participant.raven_complete = True
    player.sender_status = player.participant.sender_status


def available_messages_for_type(type_number: int):
    choices = []
    for start in range(1, type_number + 1):
        for end in range(type_number, 4):
            if start <= type_number <= end:
                choice = '{' + ', '.join(str(value) for value in range(start, end + 1)) + '}'
                if choice not in choices:
                    choices.append(choice)
    return sorted(choices, key=lambda value: (len(value), value))


def decision_context(player: Player, page_name):
    screen_number, page_title = DECISION_META[page_name]
    total_screens = 4 if player.round_number == C.NUM_ROUNDS else 1
    return dict(
        section_title='Sender Experiment: Decision Screens',
        section_subtitle=f'Round {player.round_number} of {C.NUM_ROUNDS}',
        progress_text=f'Screen {screen_number} of {total_screens}',
        page_title=page_title,
        progress_percent=round((screen_number / total_screens) * 100),
        countdown_seconds=None,
    )


def raven_context(player: Player, trial_number: int):
    trial = raven_trials_for_player(player)[trial_number - 1]
    selected_field, _, rt_field = RAVEN_FIELDS[trial_number]
    return dict(
        section_title='Raven Matrices',
        section_subtitle='',
        progress_text='',
        page_title=f'Question {trial_number}',
        progress_percent=round((trial_number / 5) * 100),
        countdown_seconds=raven_time_remaining(player),
        question_id=trial['question_id'],
        matrix_image=f"/static/raven/{trial['question_id']}/stem.png",
        option_images=[
            dict(
                value=f'R{i}',
                image=f"/static/raven/{trial['question_id']}/{trial['question_id']}R{i}.png",
            )
            for i in range(1, 9)
        ],
        selected_field_name=selected_field,
        rt_field_name=rt_field,
        saved_selection=player.field_maybe_none(selected_field) or '',
    )


def raven_error_message(player: Player, values, trial_number: int):
    if raven_time_remaining(player) <= 0:
        return
    selected_field, _, rt_field = RAVEN_FIELDS[trial_number]
    selected_value = (values.get(selected_field) or '').strip()
    valid_answers = {f'R{i}' for i in range(1, 9)}
    if selected_value not in valid_answers:
        return 'Please choose one answer option before continuing.'
    rt_value = values.get(rt_field)
    if rt_value in (None, ''):
        return 'Response time was not captured. Please select your answer again.'


def store_raven_result(player: Player, trial_number: int):
    trial = raven_trials_for_player(player)[trial_number - 1]
    selected_field, correct_field, _ = RAVEN_FIELDS[trial_number]
    selected_value = getattr(player, selected_field, '') or ''
    setattr(player, correct_field, selected_value == trial['correct_answer'])

    if trial_number == 5 or raven_time_remaining(player) <= 0:
        finalize_raven(player)


class InstructionsWelcome(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return instruction_context('InstructionsWelcome')


class InstructionsRole(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return instruction_context('InstructionsRole')


class InstructionsStatus(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return instruction_context('InstructionsStatus')

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.raven_deadline = time.time() + (5 * 60)
        player.participant.raven_complete = False


class RavenTrial1(Page):
    form_model = 'player'
    form_fields = ['raven_trial_1_selected', 'raven_trial_1_rt_ms']
    template_name = 'sender_experiment/RavenTrial.html'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and not getattr(player.participant, 'raven_complete', False)

    @staticmethod
    def get_timeout_seconds(player: Player):
        return raven_time_remaining(player)

    @staticmethod
    def vars_for_template(player: Player):
        return raven_context(player, 1)

    @staticmethod
    def error_message(player: Player, values):
        return raven_error_message(player, values, 1)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        store_raven_result(player, 1)


class RavenTrial2(Page):
    form_model = 'player'
    form_fields = ['raven_trial_2_selected', 'raven_trial_2_rt_ms']
    template_name = 'sender_experiment/RavenTrial.html'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and not getattr(player.participant, 'raven_complete', False)

    @staticmethod
    def get_timeout_seconds(player: Player):
        return raven_time_remaining(player)

    @staticmethod
    def vars_for_template(player: Player):
        return raven_context(player, 2)

    @staticmethod
    def error_message(player: Player, values):
        return raven_error_message(player, values, 2)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        store_raven_result(player, 2)


class RavenTrial3(Page):
    form_model = 'player'
    form_fields = ['raven_trial_3_selected', 'raven_trial_3_rt_ms']
    template_name = 'sender_experiment/RavenTrial.html'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and not getattr(player.participant, 'raven_complete', False)

    @staticmethod
    def get_timeout_seconds(player: Player):
        return raven_time_remaining(player)

    @staticmethod
    def vars_for_template(player: Player):
        return raven_context(player, 3)

    @staticmethod
    def error_message(player: Player, values):
        return raven_error_message(player, values, 3)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        store_raven_result(player, 3)


class RavenTrial4(Page):
    form_model = 'player'
    form_fields = ['raven_trial_4_selected', 'raven_trial_4_rt_ms']
    template_name = 'sender_experiment/RavenTrial.html'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and not getattr(player.participant, 'raven_complete', False)

    @staticmethod
    def get_timeout_seconds(player: Player):
        return raven_time_remaining(player)

    @staticmethod
    def vars_for_template(player: Player):
        return raven_context(player, 4)

    @staticmethod
    def error_message(player: Player, values):
        return raven_error_message(player, values, 4)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        store_raven_result(player, 4)


class RavenTrial5(Page):
    form_model = 'player'
    form_fields = ['raven_trial_5_selected', 'raven_trial_5_rt_ms']
    template_name = 'sender_experiment/RavenTrial.html'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and not getattr(player.participant, 'raven_complete', False)

    @staticmethod
    def get_timeout_seconds(player: Player):
        return raven_time_remaining(player)

    @staticmethod
    def vars_for_template(player: Player):
        return raven_context(player, 5)

    @staticmethod
    def error_message(player: Player, values):
        return raven_error_message(player, values, 5)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        store_raven_result(player, 5)


class GameInstructionsOverview(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return post_raven_context('GameInstructionsOverview')


class Part2Transition(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return post_raven_context('Part2Transition')


class GameInstructionsSets(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        context = post_raven_context('GameInstructionsSets')
        context['example_sets'] = ['{1, 2, 3}', '{2, 3}', '{3}']
        return context


class MessageDecision(Page):
    form_model = 'player'
    form_fields = ['sent_message']

    @staticmethod
    def vars_for_template(player: Player):
        if not current_sender_status(player):
            score = getattr(player.participant, 'raven_score', 0)
            player.participant.sender_status = 'High Status' if score > 2 else 'Low Status'
        player.sender_status = current_sender_status(player)
        context = decision_context(player, 'MessageDecision')
        context['message_choices'] = available_messages_for_type(player.type_number)
        context['saved_message_value'] = player.field_maybe_none('sent_message') or ''
        return context

    @staticmethod
    def error_message(player: Player, values):
        raw_value = (values.get('sent_message') or '').strip()
        if not raw_value:
            return 'Please choose one set of numbers before submitting.'

        valid_choices = set(available_messages_for_type(player.type_number))
        if raw_value not in valid_choices:
            return 'Please choose a valid set of numbers.'


class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'education']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        return decision_context(player, 'Demographics')


class Part2Ended(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        return decision_context(player, 'Part2Ended')


class EndScreen(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        return decision_context(player, 'EndScreen')


page_sequence = [
    InstructionsWelcome,
    InstructionsRole,
    InstructionsStatus,
    RavenTrial1,
    RavenTrial2,
    RavenTrial3,
    RavenTrial4,
    RavenTrial5,
    Part2Transition,
    GameInstructionsOverview,
    GameInstructionsSets,
    MessageDecision,
    Part2Ended,
    Demographics,
    EndScreen,
]
