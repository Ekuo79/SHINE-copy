from django.core.management.base import BaseCommand
from django.conf import settings
from companies.models import Companies, Language
import json

class Command(BaseCommand):
    help = 'Safely update or create companies from JSON in production'

    def handle(self, *args, **options):
        json_file_path = settings.BASE_DIR / 'static' / 'test_companies.json'

        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

            Companies.objects.all().delete()

            for company_data in data:
                fields = company_data['fields']

                company, created = Companies.objects.update_or_create(
                    title=fields['title'],  # match existing by title
                    defaults={
                        'about': fields['about'],
                        'pretest': fields['pretest'],
                        'posttest': fields['posttest'],
                        'point_total': fields.get('point_total', 0),
                        'interactive': fields.get('interactive', False),
                        'logo_path': fields.get('logo_path', ''),
                        'feedback': fields.get('feedback', '')
                    }
                )

                # Clear and reassign languages (or add new ones)
                company.languages.clear()
                for lang_name in fields['languages']:
                    language, _ = Language.objects.get_or_create(name=lang_name)
                    company.languages.add(language)

                action = "Created" if created else "Updated"
                self.stdout.write(self.style.SUCCESS(f"{action}: {company.title}"))

        self.stdout.write(self.style.SUCCESS("Production-safe database update complete"))
