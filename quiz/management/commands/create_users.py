import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from quiz.models import *

class Command(BaseCommand):
    help = '''สร้างผู้ใช้ 'n' คน จากการสุ่ม https://randomuser.me/api
    python manage.py random_users
    '''

    def add_arguments(self, parser):
        parser.add_argument('-n', '--number', type=int)

    def handle(self, *args, **options):
        url = 'https://randomuser.me/api'
        n = 1
        if options['number']:
            n = options['number']

        for i in range(n):
            u = requests.get(url).json()['results'][0]
            user, created = User.objects.get_or_create(
                username=u['login']['username'], 
                email=u['email']
            )
            if created:
                user.set_password('1234')
                user.first_name = u['name']['first']
                user.last_name = u['name']['last']
                user.save()
                quote = requests.get(f'https://dummyjson.com/quotes/{user.id}').json()['quote']
                member = Member.objects.create(
                    user = user,
                    quote = quote,
                    state = u['location']['state'],
                    country = u['location']['country'],
                    picture_url = u['picture']['large'],
                )
                member.save()
                print(user.id, user.username, member.quote)
