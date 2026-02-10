from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from companies.models import Companies, Language
from .models import SurveySubmission
import json
from django.conf import settings

class ApplyView(TemplateView):
    template_name = 'apply/apply.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = Companies.objects.all()
        return context


class SurveySubmitView(View):
    def post(self, request):
        try:
            # Get form data
            data = json.loads(request.body)

            # Create survey submission
            submission = SurveySubmission(
                company_name=data.get('company_name'),
                company_about=data.get('company_about'),
                contact_email=data.get('contact_email'),
                survivor_accounts=data.get('survivor_accounts', False),
                tailored_content=data.get('tailored_content', False),
                statistics=data.get('statistics', False),
                victim_focused=data.get('victim_focused', False),
                risk_reduction=data.get('risk_reduction', False),
                partnerships=data.get('partnerships', False),
                overall_definition=data.get('overall_definition', False),
                trafficking_signs=data.get('trafficking_signs', False),
                law_enforcement=data.get('law_enforcement', False),
                legal_regulations=data.get('legal_regulations', False),
                pretest=data.get('pretest', False),
                posttest=data.get('posttest', False),
                interactive=data.get('interactive', False),
                languages=data.get('languages', ''),
                logo_path=data.get('logo_path', '')
            )

            # Calculate score
            score = submission.calculate_score()
            submission.save()

            # Return success message - NO auto-adding to website
            # Passing trainings will be pending admin review
            if submission.passed:
                message = 'Congratulations! Your training passed the assessment with a score of {}. It is now pending admin review before being added to the website.'.format(score)
            else:
                message = 'Your training did not meet the minimum score of 18 points. You scored {} points.'.format(score)

            return JsonResponse({
                'success': True,
                'score': score,
                'passed': submission.passed,
                'message': message
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)

    def add_to_companies_json(self, submission):
        """Add passing submission to test_companies.json"""
        json_file_path = settings.BASE_DIR / 'static' / 'test_companies.json'

        # Read existing data
        with open(json_file_path, 'r') as f:
            data = json.load(f)

        # Get next primary key
        next_pk = max([item['pk'] for item in data]) + 1 if data else 1

        # Create new entry
        new_entry = {
            "model": "companies.companies",
            "pk": next_pk,
            "fields": {
                "title": submission.company_name,
                "about": submission.company_about,
                "pretest": submission.pretest,
                "posttest": submission.posttest,
                "interactive": submission.interactive,
                "point_total": submission.total_score,
                "languages": [lang.strip() for lang in submission.languages.split(',')] if submission.languages else [],
                "logo_path": submission.logo_path or "",
                "feedback": "Congratulations! Your training has passed our assessment criteria."
            }
        }

        # Append and save
        data.append(new_entry)

        with open(json_file_path, 'w') as f:
            json.dump(data, f, indent=2)

        return new_entry