from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Subject
from .forms import SubjectForm

# Grade mapping
GRADE_POINTS = {'S':10, 'A':9, 'B':8, 'C':7, 'D':6, 'F':0}

# --------------------
# Registration
# --------------------
def register_page(request):
    if request.method == "POST":
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()

        if not username or not password:
            messages.error(request, "Both fields are required!")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password)
        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')

    return render(request, "register.html")


# --------------------
# Login
# --------------------
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('cgpa_calculator')
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('login')

    return render(request, "login.html")


# --------------------
# Logout
# --------------------
def custom_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')


# --------------------
# CGPA Calculator
# --------------------
@login_required(login_url='login')
def cgpa_calculator(request):
    subjects = Subject.objects.filter(user=request.user)
    form = SubjectForm()

    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.user = request.user
            subject.save()
            return redirect('cgpa_calculator')

    # Calculate CGPA
    total_credits = sum(sub.credit for sub in subjects)
    total_points = sum(sub.credit * GRADE_POINTS.get(sub.grade, 0) for sub in subjects)
    cgpa = total_points / total_credits if total_credits else 0

    context = {'subjects': subjects, 'form': form, 'cgpa': cgpa}
    return render(request, 'index.html', context)


# --------------------
# Edit Subject
# --------------------
@login_required(login_url='login')
def edit_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id, user=request.user)
    if request.method == "POST":
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('cgpa_calculator')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'edit_subject.html', {'form': form, 'subject_id': subject_id})


# --------------------
# Delete Subject
# --------------------
@login_required(login_url='login')
def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id, user=request.user)
    subject.delete()
    return redirect('cgpa_calculator')


# --------------------
# Result Page (Optional PDF/Print)
# --------------------
@login_required(login_url='login')
def result(request):
    subjects = Subject.objects.filter(user=request.user)
    total_credits = sum(sub.credit for sub in subjects)
    total_points = sum(sub.credit * GRADE_POINTS.get(sub.grade, 0) for sub in subjects)
    cgpa = total_points / total_credits if total_credits else 0
    context = {'subjects': subjects, 'cgpa': cgpa}
    return render(request, 'pdf.html', context)
