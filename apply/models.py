from django.db import models

# Create your models here.

class SurveySubmission(models.Model):
    # Company Information
    company_name = models.CharField(max_length=200)
    company_about = models.TextField()
    contact_email = models.EmailField()

    # Survey Questions (1 point each)
    survivor_accounts = models.BooleanField(default=False)
    tailored_content = models.BooleanField(default=False)
    statistics = models.BooleanField(default=False)

    # Survey Questions (2 points each)
    victim_focused = models.BooleanField(default=False)
    risk_reduction = models.BooleanField(default=False)
    partnerships = models.BooleanField(default=False)

    # Survey Questions (3 points each)
    overall_definition = models.BooleanField(default=False)
    trafficking_signs = models.BooleanField(default=False)
    law_enforcement = models.BooleanField(default=False)
    legal_regulations = models.BooleanField(default=False)

    # Additional fields
    pretest = models.BooleanField(default=False)
    posttest = models.BooleanField(default=False)
    interactive = models.BooleanField(default=False)
    languages = models.TextField(help_text="Comma-separated list of languages")
    logo_path = models.CharField(max_length=255, blank=True)

    # Metadata
    total_score = models.IntegerField(default=0)
    passed = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    # Admin Approval Status
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'

    STATUS_CHOICES = [
        (PENDING, 'Pending Review'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]

    approval_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING,
        help_text="Admin approval status for adding to website"
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.CharField(max_length=100, blank=True)

    def calculate_score(self):
        score = 0
        # 1 point features
        if self.survivor_accounts:
            score += 1
        if self.tailored_content:
            score += 1
        if self.statistics:
            score += 1

        # 2 point features
        if self.victim_focused:
            score += 2
        if self.risk_reduction:
            score += 2
        if self.partnerships:
            score += 2

        # 3 point features
        if self.overall_definition:
            score += 3
        if self.trafficking_signs:
            score += 3
        if self.law_enforcement:
            score += 3
        if self.legal_regulations:
            score += 3

        self.total_score = score
        self.passed = score >= 18
        return score

    def __str__(self):
        return f"{self.company_name} - Score: {self.total_score} - {'Passed' if self.passed else 'Not Passed'}"
