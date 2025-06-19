from django.db import models

# Create your models here.


class Form(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    QUESTION_TYPES = [
        ("text", "Text-based answer"),
        ("choice", "Choose one from multi options"),
        ("range", "Pick one number from the range of 1-5"),
    ]

    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=500)
    type = models.CharField(max_length=10, choices=QUESTION_TYPES, default="text")
    is_mandatory = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "created_at"]

    def __str__(self):
        return f"{self.form.name} - {self.text[:50]}"


class ChoiceOption(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choices"
    )
    text = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "created_at"]

    def __str__(self):
        return f"{self.question.text[:30]} - {self.text}"


class Submission(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="submissions")
    submitted_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(blank=True, null=True)  # Optional email for confirmation

    def __str__(self):
        return f"{self.form.name} - {self.submitted_at.strftime('%Y-%m-%d %H:%M')}"


class Answer(models.Model):
    submission = models.ForeignKey(
        Submission, on_delete=models.CASCADE, related_name="answers"
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text_answer = models.TextField(blank=True, null=True)
    choice_answer = models.ForeignKey(
        ChoiceOption, on_delete=models.CASCADE, blank=True, null=True
    )
    range_answer = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        if self.text_answer:
            return f"{self.question.text[:30]} - {self.text_answer[:30]}"
        elif self.choice_answer:
            return f"{self.question.text[:30]} - {self.choice_answer.text}"
        elif self.range_answer:
            return f"{self.question.text[:30]} - {self.range_answer}"
        return f"{self.question.text[:30]} - No answer"
