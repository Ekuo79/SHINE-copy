from django.contrib import admin
from django.utils import timezone
from .models import SurveySubmission
from companies.models import Companies, Language
import json
from django.conf import settings

# Register your models here.

@admin.register(SurveySubmission)
class SurveySubmissionAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'contact_email', 'total_score', 'passed', 'approval_status', 'submitted_at')
    list_filter = ('passed', 'approval_status', 'submitted_at')
    search_fields = ('company_name', 'contact_email')
    readonly_fields = ('total_score', 'passed', 'submitted_at', 'reviewed_at', 'reviewed_by')
    actions = ['approve_and_add_to_website', 'reject_submission']

    fieldsets = (
        ('Company Information', {
            'fields': ('company_name', 'company_about', 'contact_email', 'languages', 'logo_path')
        }),
        ('1 Point Features', {
            'fields': ('survivor_accounts', 'tailored_content', 'statistics')
        }),
        ('2 Point Features', {
            'fields': ('victim_focused', 'risk_reduction', 'partnerships')
        }),
        ('3 Point Features', {
            'fields': ('overall_definition', 'trafficking_signs', 'law_enforcement', 'legal_regulations')
        }),
        ('Additional Features', {
            'fields': ('pretest', 'posttest', 'interactive')
        }),
        ('Results', {
            'fields': ('total_score', 'passed', 'submitted_at')
        }),
        ('Admin Review', {
            'fields': ('approval_status', 'reviewed_at', 'reviewed_by')
        }),
    )

    def approve_and_add_to_website(self, request, queryset):
        """Approve selected submissions and add them to the website"""
        approved_count = 0
        for submission in queryset:
            # Only approve submissions that passed the assessment
            if submission.passed and submission.approval_status != SurveySubmission.APPROVED:
                # Create Companies object
                company = Companies.objects.create(
                    title=submission.company_name,
                    about=submission.company_about,
                    pretest=submission.pretest,
                    posttest=submission.posttest,
                    interactive=submission.interactive,
                    point_total=submission.total_score,
                    logo_path=submission.logo_path,
                    feedback="Congratulations! Your training has passed our assessment criteria."
                )

                # Add languages
                if submission.languages:
                    lang_list = [lang.strip() for lang in submission.languages.split(',')]
                    for lang_name in lang_list:
                        language, _ = Language.objects.get_or_create(name=lang_name)
                        company.languages.add(language)

                # Add to JSON file
                self.add_to_companies_json(submission)

                # Update submission status
                submission.approval_status = SurveySubmission.APPROVED
                submission.reviewed_at = timezone.now()
                submission.reviewed_by = request.user.username
                submission.save()

                approved_count += 1

        self.message_user(request, f'{approved_count} submission(s) approved and added to website.')
    approve_and_add_to_website.short_description = "Approve and add to website"

    def reject_submission(self, request, queryset):
        """Reject selected submissions"""
        rejected_count = 0
        for submission in queryset:
            if submission.approval_status != SurveySubmission.REJECTED:
                submission.approval_status = SurveySubmission.REJECTED
                submission.reviewed_at = timezone.now()
                submission.reviewed_by = request.user.username
                submission.save()
                rejected_count += 1

        self.message_user(request, f'{rejected_count} submission(s) rejected.')
    reject_submission.short_description = "Reject submission"

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
