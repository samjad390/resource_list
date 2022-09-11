import names
import random
import string
import requests
import json

from django.core.management.base import BaseCommand

from resource_notes.models import ResourceNotes


class Command(BaseCommand):
    letters = string.ascii_lowercase[:22]

    def add_arguments(self, parser):
        parser.add_argument('-total', '--total', nargs='+', type=str,)

    def generate_email_name(self, letters, length):
        return ''.join(random.choice(letters) for i in range(length))

    def get_rand_emails(self, no_of_emails, length):
        return [self.generate_email_name(self.letters, length) + '@' + "xyz.com" for i in range(no_of_emails)]

    def handle(self, *args, **kwargs):
        total = kwargs.get('total', None)
        if total is None:
            total = 10000
        emails = self.get_rand_emails(total, 10)
        resource_notes_list = []
        for i in range(total):
            resource_notes_list.append(
                ResourceNotes(
                    name=names.get_first_name(), email=emails[i], notes="Some random notes"
                )
            )
        ResourceNotes.objects.bulk_create(resource_notes_list)

