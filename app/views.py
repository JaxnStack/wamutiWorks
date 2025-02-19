from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import csv
import pandas as pd  # Added for Excel file handling
from .models import Quiz, Question, Choice, QuestionUpload
from .forms import QuestionUploadForm

# Registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('home')

# Landing page view
def landing_page(request):
    return render(request, 'landing_page.html')

# Dashboard for admins (superuser)
def dashboard(request):
    if not request.user.is_superuser:
        return redirect('home')  # Redirect non-admin users to the home page
    return render(request, 'dashboard.html')

# ✅ View to handle file uploads (NEW)
@login_required
def upload_questions(request):
    if request.method == 'POST':
        form = QuestionUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "File uploaded successfully. Processing in background.")
            return redirect('dashboard')  # Redirect after upload
    else:
        form = QuestionUploadForm()
    
    return render(request, 'upload_questions.html', {'form': form})

#  Function to process uploaded files (NEW)
def process_uploaded_questions():
    uploads = QuestionUpload.objects.filter(processed=False)
    for upload in uploads:
        file_path = upload.file.path
        quiz = upload.quiz
        
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            else:
                continue  # Skip unsupported file types

            for _, row in df.iterrows():
                question = Question.objects.create(
                    quiz=quiz,
                    question_text=row['question_text'],
                    question_type=row.get('question_type', 'MCQ'),
                    correct_answer=row['correct_answer'],
                    explanation=row.get('explanation', '')
                )

                # If it's an MCQ, add choices
                if 'choice_1' in row and 'choice_2' in row:
                    for i in range(1, 5):  # Assume max 4 choices
                        choice_text = row.get(f'choice_{i}', None)
                        if choice_text:
                            Choice.objects.create(question=question, choice_text=choice_text)
            
            upload.processed = True
            upload.save()
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

# View to display quiz questions with a limit (NEW)
@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()[:quiz.max_questions]  # Apply question limit
    
    return render(request, 'take_quiz.html', {'quiz': quiz, 'questions': questions})
