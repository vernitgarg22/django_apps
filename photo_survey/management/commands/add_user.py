from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q


class Command(BaseCommand):
    help = """
        Use this to add users to an app, e.g.,
        python manage.py add_user database first_name last_name email
        python manage.py add_user photo_survey karl kaebnick karl.kaebnick@mail.com"""

    def add_arguments(self, parser):
        # parser.add_argument('database', type=str, help="Database to add user to")
        parser.add_argument('first_name', type=str, help="User's first name")
        parser.add_argument('last_name', type=str, help="User's last name")
        parser.add_argument('email', type=str, help="User's email address")
        parser.add_argument('password', type=str, help="User's password")

    def handle(self, *args, **options):

        database = 'photo_survey'
        first_name = options['first_name']
        last_name = options['last_name']
        email = options['email']
        password = options['password']

        username = email

        if User.objects.using(database).filter(Q(email=email) | Q(username=username)).exists():
            raise CommandError('User "%s" already exists' % email)

        user = User.objects.db_manager(database).create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
