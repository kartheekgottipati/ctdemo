from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.contrib.auth.management import get_default_username
from django.db import DEFAULT_DB_ALIAS

class Command(BaseCommand):
    help = 'Creates a couple of test users'
    requires_migrations_checks = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.UserModel = get_user_model()

    def add_arguments(self, parser):
        parser.add_argument(
            "--database",
            default=DEFAULT_DB_ALIAS,
            help='Specifies the database to use. Default is "default".',
        )

    def handle(self, *args, **options):
        database = options["database"]
        users = [
            {
                "username": "testuser1",
                "email": "test1@example.com",
                "password": "testpass1"
            },{
                "username": "testuser2",
                "email": "test2@example.com",
                "password": "testpass2"
            },
            {
                "username": "testuser3",
                "email": "test3@example.com",
                "password": "testpass3"
            },
            {
                "username": "testuser4",
                "email": "test4@example.com",
                "password": "testpass4"
            }
        ]

        for user in users:
            try:
                username = user["username"]
                print(username)
                self.UserModel._default_manager.db_manager(database).get_by_natural_key(
                    username
                )
                print(f"{user['username']} already exists. Skipping.....")
            except self.UserModel.DoesNotExist:
                self.UserModel._default_manager.db_manager(database).create_superuser(
                    **user
                )
                print(f"{user['username']} created successfully.")
