# required packages:
#  - openpyxl
import os, traceback
from django.apps import apps
from django.db.models import *
from django.core.management.base import BaseCommand, CommandError
from openpyxl import load_workbook
from quiz.models import *

class Command(BaseCommand):
    help = '''โหลดข้อมูลจาก xlsx
    python manage.py load_xlsx -i quiz/fixtures/quiz_data.xlsx
    '''

    def add_arguments(self, parser):
        parser.add_argument('-i', '--input', type=str, default='quiz/fixtures/quiz_data.xlsx')
        parser.add_argument('-s', '--skip_id', type=bool, default=False)

    def handle(self, *args, **options):
        #xlsx = os.path.join('quiz', 'fixtures', 'quiz_data.xlsx')
        if options['input']:
            xlsx = options['input']
        for k,v in options.items():
            print(k, v)
        wb = load_workbook(xlsx)
        models = [
            'Question',
            'Choice'
        ]
        app = apps.get_app_config('quiz') 
        for name in models:
            print(f'loading... {name}')
            m = app.get_model(name)
            fields = [f.name for f in m._meta.fields]
            keys = []
            for row in wb[name]:
                values = [ cell.value for cell in row ]
                print(values)
                if values[0] == 'id':
                    keys = values
                else:
                    data = dict( (keys[i],values[i]) for i in range(len(keys)) if keys[i] in fields )
                    if options['skip_id']:
                        data.pop('id', 0)
                    print('data', data)
                    for k,value in data.items():
                        field = m._meta.get_field(k)
                        print(type(field), field)
                        try:
                            if type(field) in [OneToOneField, ForeignKey] and value is not None:
                                data[k] = field.related_model.objects.get(id=int(value))
                            elif type(field) == DateTimeField and value is not None:
                                data[k] = value.isoformat()
                            elif type(field) == DateField and value is not None:
                                data[k] = f'{value.year:04}-{value.month:02}-{value.day:02}'
                        except Exception:
                            print('k', type(k), k)
                            print('value', type(value), value)
                            print(traceback.format_exc())
                            del data[k]
                    obj, created = m.objects.get_or_create(**data)


