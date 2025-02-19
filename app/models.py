from django.db import models
from django.contrib.auth.models import User

# Model for Quiz Categories
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

# Model for Quizzes
class Quiz(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='quizzes')
    description = models.TextField()
    time_limit = models.PositiveIntegerField(help_text="Time limit in minutes", default=30)
    max_attempts = models.PositiveIntegerField(default=1)
    show_answers_after_attempts = models.BooleanField(default=True, help_text="Show answers only after attempts are exhausted")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Model for Questions
class Question(models.Model):
    QUESTION_TYPES = (
        ('MCQ', 'Multiple Choice'),
        ('TXT', 'Text Answer'),
    )
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_type = models.CharField(max_length=3, choices=QUESTION_TYPES, default='MCQ')
    question_text = models.CharField(max_length=500)
    image = models.ImageField(upload_to='question_images/', blank=True, null=True)
    correct_answer = models.CharField(max_length=200)
    explanation = models.TextField(blank=True, null=True, help_text="Explanation shown after attempts")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text

# Model for Multiple Choice Options
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        return self.choice_text

# Model for User Answers
class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.question.question_text} - {self.answer_text}'

# Model for Tracking Quiz Attempts
class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField(default=0)
    attempt_number = models.PositiveIntegerField()
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.quiz.title} - Attempt {self.attempt_number} - Score: {self.score}'

# Model for File Upload (Batch Question Uploads)
class QuestionUpload(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='uploads')
    file = models.FileField(upload_to='uploads/questions/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)  # NEW - To track if file has been processed


    def __str__(self):
        return f'Upload for {self.quiz.title} on {self.uploaded_at}'
