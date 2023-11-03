from django.core.management.base import BaseCommand, CommandParser

import random
from datetime import date

from django_seed import Seed
from faker import Faker

from employees_dir.models import Position, Employee

class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        pass

    def handle(self, *args, **options) -> None:
        seeder = Seed.seeder()
        fake = Faker('ru_RU')

        for level in reversed(range(1, 6)):
            seeder.add_entity(Position, (6-level)*3, {
                'title': lambda x: fake.job(),
                'hierarchy_level': level,
            })
            seeder.execute()

            if level == 5:
                quantity = 20
                prev = 0
                first_entry = 0
            else:
                manager_objects = Employee.objects.filter(
                                id__in=range(first_entry, last_entry))
                first_entry = Employee.objects.latest('id').id

            if level in range(2, 5):
                prev += quantity
                quantity *= 5
            if level == 1:
                quantity = 50000 - prev - quantity

            position_objects = Position.objects.filter(hierarchy_level=level)
            
            seeder.add_entity(Employee, quantity, {
                'full_name': lambda x: fake.name(),
                'employment_date': lambda x: fake.date_between(date(1995, 4, 7)),
                'salary': lambda x: random.randrange(40000*level, 40000*(level+1), 5000*level),
                'manager': lambda x: random.choice(manager_objects) if level < 5 else None,
                'position': lambda x: random.choice(position_objects) 
            })
            seeder.execute()

            last_entry = Employee.objects.latest('id').id
