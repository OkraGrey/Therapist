from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Form, Question, ChoiceOption, Submission, Answer

User = get_user_model()


class FormSubmissionTestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        # Create a test user
        self.user = User.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="testpass123",
            first_name="Admin",
            last_name="User",
            is_staff=True,
        )

        # Create a test form
        self.form = Form.objects.create(
            name="Test Form", description="A test form for testing submissions"
        )

        # Create test questions
        self.text_question = Question.objects.create(
            form=self.form,
            text="What is your name?",
            type="text",
            is_mandatory=True,
            order=1,
        )

        self.choice_question = Question.objects.create(
            form=self.form,
            text="What is your favorite color?",
            type="choice",
            is_mandatory=True,
            order=2,
        )

        # Create choice options
        self.choice1 = ChoiceOption.objects.create(
            question=self.choice_question, text="Red", order=1
        )
        self.choice2 = ChoiceOption.objects.create(
            question=self.choice_question, text="Blue", order=2
        )

        self.range_question = Question.objects.create(
            form=self.form,
            text="Rate your experience (1-5)",
            type="range",
            is_mandatory=False,
            order=3,
        )

        self.client = Client()

    def test_public_form_view_get(self):
        """Test that public form view displays correctly"""
        url = reverse("forms:public_form", kwargs={"form_id": self.form.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Form")
        self.assertContains(response, "What is your name?")
        self.assertContains(response, "What is your favorite color?")
        self.assertContains(response, "Rate your experience")

    def test_form_submission_success(self):
        """Test successful form submission"""
        url = reverse("forms:public_form", kwargs={"form_id": self.form.id})
        data = {
            f"answer_{self.text_question.id}": "John Doe",
            f"answer_{self.choice_question.id}": self.choice1.id,
            f"answer_{self.range_question.id}": "4",
            "email": "test@example.com",
        }

        response = self.client.post(url, data)

        # Should redirect to success page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("forms:submission_success", kwargs={"form_id": self.form.id}),
        )

        # Check that submission was created
        self.assertEqual(Submission.objects.count(), 1)
        submission = Submission.objects.first()
        self.assertEqual(submission.form, self.form)
        self.assertEqual(submission.email, "test@example.com")

        # Check that answers were created
        self.assertEqual(Answer.objects.count(), 3)

        # Check text answer
        text_answer = Answer.objects.get(question=self.text_question)
        self.assertEqual(text_answer.text_answer, "John Doe")

        # Check choice answer
        choice_answer = Answer.objects.get(question=self.choice_question)
        self.assertEqual(choice_answer.choice_answer, self.choice1)

        # Check range answer
        range_answer = Answer.objects.get(question=self.range_question)
        self.assertEqual(range_answer.range_answer, 4)

    def test_form_submission_mandatory_validation(self):
        """Test that mandatory fields are validated"""
        url = reverse("forms:public_form", kwargs={"form_id": self.form.id})
        data = {
            # Missing mandatory text answer
            f"answer_{self.choice_question.id}": self.choice1.id,
            f"answer_{self.range_question.id}": "4",
        }

        response = self.client.post(url, data)

        # Should not redirect (validation error)
        self.assertEqual(response.status_code, 200)

        # Check that no submission was created
        self.assertEqual(Submission.objects.count(), 0)
        self.assertEqual(Answer.objects.count(), 0)

    def test_submission_success_view(self):
        """Test submission success page"""
        # Create a submission first
        submission = Submission.objects.create(form=self.form, email="test@example.com")

        url = reverse("forms:submission_success", kwargs={"form_id": self.form.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Submission Successful")
        self.assertContains(response, "Test Form")

    def test_form_without_email(self):
        """Test form submission without email"""
        url = reverse("forms:public_form", kwargs={"form_id": self.form.id})
        data = {
            f"answer_{self.text_question.id}": "John Doe",
            f"answer_{self.choice_question.id}": self.choice1.id,
            f"answer_{self.range_question.id}": "4",
            # No email provided
        }

        response = self.client.post(url, data)

        # Should still succeed
        self.assertEqual(response.status_code, 302)

        # Check that submission was created without email
        submission = Submission.objects.first()
        self.assertIsNone(submission.email)

    def test_invalid_form_id(self):
        """Test accessing non-existent form"""
        url = reverse("forms:public_form", kwargs={"form_id": 99999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)


class ModelTestCase(TestCase):
    def test_form_str(self):
        """Test Form model string representation"""
        form = Form.objects.create(name="Test Form")
        self.assertEqual(str(form), "Test Form")

    def test_question_str(self):
        """Test Question model string representation"""
        form = Form.objects.create(name="Test Form")
        question = Question.objects.create(form=form, text="What is your name?")
        self.assertIn("Test Form", str(question))
        self.assertIn("What is your name?", str(question))

    def test_submission_str(self):
        """Test Submission model string representation"""
        form = Form.objects.create(name="Test Form")
        submission = Submission.objects.create(form=form)
        self.assertIn("Test Form", str(submission))

    def test_answer_str(self):
        """Test Answer model string representation"""
        form = Form.objects.create(name="Test Form")
        question = Question.objects.create(form=form, text="What is your name?")
        submission = Submission.objects.create(form=form)
        answer = Answer.objects.create(
            submission=submission, question=question, text_answer="John Doe"
        )
        self.assertIn("John Doe", str(answer))
