# Registration View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from taskapp.forms import RegisterForm, LoginForm
from taskapp.models import Question, UserResponse
import json


def home(request):
    return render(request,'home.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        print("post method")
        form = LoginForm(request.POST)
        print("Form data received:", request.POST)  # Print form data received
        # Check if the form is valid
        if form.is_valid():
            print("Form is valid")
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(username, password)
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    print(f"User {username} logged in successfully.")
                    return redirect('submit_response')  # Redirect after successful login
                else:
                    messages.error(request, "Your account is inactive. Please contact support.")
                    print(f"User {username} is inactive.")
            else:
                messages.error(request, "Invalid credentials. Please try again.")
                print(f"Authentication failed for {username}. Invalid username or password.")
        else:
            print("Form is invalid:", form.errors)  # Print form validation errors
            messages.error(request, "Form is invalid. Please check your details.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


# Logout View
def user_logout(request):
    logout(request)
    return redirect('login')


# Questions View
from django.http import JsonResponse
from django.core import serializers

@login_required
def submit_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        question_id = data.get('question_id')
        answer = data.get('answer')

        # Retrieve the question and corresponding score
        question = Question.objects.get(id=question_id)
        score = 0
        if answer == 'a':
            score = question.score_a
        elif answer == 'b':
            score = question.score_b
        elif answer == 'c':
            score = question.score_c
        elif answer == 'd':
            score = question.score_d

        # Check if the UserResponse already exists
        existing_response = UserResponse.objects.filter(user=request.user, question=question).first()
        if existing_response:
            # Update the existing response
            existing_response.answer = answer
            existing_response.score = score
            existing_response.save()
            return JsonResponse({'status': 'updated', 'message': 'Response updated successfully.'})

        # Create the UserResponse instance if it doesn't exist
        UserResponse.objects.create(
            user=request.user,
            question=question,
            answer=answer,
            score=score
        )

        return JsonResponse({'status': 'success', 'message': 'Response submitted successfully.'})

    questions = Question.objects.all()
    questions_data = [{'id': question.id, 'question_text': question.question_text,
                       'answer_a': question.answer_a, 'answer_b': question.answer_b,
                       'answer_c': question.answer_c, 'answer_d': question.answer_d}
                      for question in questions]

    return render(request, 'questions.html', {'questions': questions_data})


# Results View
@login_required
def calculate_credit_score(request):
    user_responses = UserResponse.objects.filter(user=request.user)
    total_score = sum(response.score for response in user_responses)
    credit_score = total_score  # You can scale or categorize it as per requirement
    return render(request, 'results.html', {'credit_score': credit_score})


# Submit Response View (API for dynamic submission)
@login_required
def submit_response_api(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        answer = request.POST.get('answer')

        question = Question.objects.get(id=question_id)
        score = getattr(question, f"score_{answer.lower()}", None)

        if score is None:
            return JsonResponse({'status': 'error', 'message': 'Invalid answer'}, status=400)

        UserResponse.objects.create(user=request.user, question=question, answer=answer, score=score)
        return JsonResponse({'status': 'success'})