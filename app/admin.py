from django.contrib import admin
from .models import Category, Quiz, Question, Choice, Answer, QuizAttempt, QuestionUpload

# Inline for Choices (for MCQ)
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4  # Show 4 choices by default

# Admin for Questions
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'quiz', 'question_type', 'created_at')
    list_filter = ('quiz', 'question_type')
    search_fields = ('question_text',)
    inlines = [ChoiceInline]

# Admin for Quizzes
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'time_limit', 'max_attempts', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'description')

# Admin for Categories
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

# Admin for Answers
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'answer_text', 'is_correct', 'submitted_at')
    list_filter = ('is_correct', 'question__quiz')
    search_fields = ('user__username', 'question__question_text')

# Admin for Quiz Attempts
@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'attempt_number', 'started_at', 'completed_at')
    list_filter = ('quiz', 'attempt_number')
    search_fields = ('user__username', 'quiz__title')

# Admin for Question Uploads
@admin.register(QuestionUpload)
class QuestionUploadAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'file', 'uploaded_at')
    list_filter = ('quiz',)
    search_fields = ('quiz__title',)

