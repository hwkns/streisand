import invoke


MANAGE_PATH = 'streisand/manage.py'
WWW_SETTINGS = 'streisand.settings.www_settings'
TRACKER_SETTINGS = 'streisand.settings.tracker_settings'

def _manage_run(ctx, command, settings=None):
    torun = f'{MANAGE_PATH} {command}'
    if settings is not None:
        torun += ' --settings=' + settings
    ctx.run(torun)


@invoke.task
def delete_migrations(ctx):
    ctx.run('rm -f streisand/*/migrations/[0-9]*.py')


@invoke.task
def clean_slate(ctx):
    _manage_run(ctx, 'reset_db --noinput')
    delete_migrations(ctx)
    _manage_run(ctx, 'makemigrations users')
    _manage_run(ctx, 'makemigrations')
    _manage_run(ctx, 'migrate')
    _manage_run(ctx, 'loaddata foundation')


@invoke.task
def fixtures(ctx):
    _manage_run(ctx, 'loaddata dev')


@invoke.task
def shell(ctx):
    _manage_run(ctx, 'shell_plus')
