from os import environ

SESSION_CONFIGS = [
    dict(
        name='sender_experiment',
        display_name='Sender Experiment',
        num_demo_participants=1,
        app_sequence=['sender_experiment'],
    ),
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=0.00,
    doc='',
)

PARTICIPANT_FIELDS = [
    'raven_set_id',
    'raven_score',
    'sender_status',
    'raven_deadline',
    'raven_complete',
]
SESSION_FIELDS = []

LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD', 'admin')

DEMO_PAGE_INTRO_HTML = """
<p>Sender experiment with participant instructions and 10 repeated decision rounds.</p>
"""

SECRET_KEY = environ.get('SECRET_KEY', 'replace-me-for-production')

INSTALLED_APPS = ['otree']
