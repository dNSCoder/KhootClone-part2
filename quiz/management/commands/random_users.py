from django.core.management import BaseCommand
from django.contrib.auth.models import User
import requests

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-n', '--number', type=int)
    def handle(self, *args, **options):
        url = 'https://randomuser.me/api/'
        n = 1
        if options['number']:
            n = options['number']
        for i in range(n):
            u = requests.get(url).json()['results'][0]
            user, created = User.objects.get_or_create(username=u['login']['username'])
            if created:
                user.set_password('1234')
                user.first_name = u['name']['first']
                user.last_name = u['name']['last']
                user.email = u['email']
                user.save()