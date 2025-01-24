from django.shortcuts import render, redirect, get_object_or_404
from .models import Subject
from .forms import SubjectForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

# Mapping of letter grades to numeric values
GRADE_POINTS = {
    'O': 10, 
    'A+': 9, 
    'A': 8, 
    'B+': 7, 
    'B': 6, 
    'C': 5, 
    'F': 0
}

# Utility function to calculate CGPA
def calculate_cgpa(subjects):
    total_credits = 0
    total_grade_points = 0

    for subject in subjects:
        total_credits += subject.credit
        total_grade_points += subject.credit * GRADE_POINTS.get(subject.grade, 0)

    return total_grade_points / total_credits if total_credits > 0 else 0

# View: CGPA Calculator
@login_required(login_url='/login/')
def cgpa_calculator(request):
    subjects = Subject.objects.all()
    form = SubjectForm()

    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cgpa_calculator')

    cgpa = calculate_cgpa(subjects)

    context = {
        'subjects': subjects,
        'form': form,
        'cgpa': cgpa,
    }
    return render(request, "home/index.html", context)

# View: Edit Subject
@login_required(login_url='/login/')
def edit_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)

    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('cgpa_calculator')
    else:
        form = SubjectForm(instance=subject)

    context = {
        'form': form,
        'subject_id': subject_id,
    }
    return render(request, "home/edit_subject.html", context)

# View: Delete Subject
@login_required(login_url='/login/')
def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    subject.delete()
    return redirect('cgpa_calculator')

# View: Display Result (e.g., PDF view)
@login_required(login_url='/login/')
def result(request):
    subjects = Subject.objects.all()
    cgpa = calculate_cgpa(subjects)

    context = {
        'subjects': subjects,
        'cgpa': cgpa,
    }
    return render(request, "home/pdf.html", context)

# View: Login Page
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=username).first()

        if not user_obj:
            messages.error(request, "Username not found")
            return redirect('/login/')

        user_obj = authenticate(username=username, password=password)
        if user_obj:
            login(request, user_obj)
            return redirect('cgpa_calculator')

        messages.error(request, "Wrong Password")
        return redirect('/login/')

    return render(request, "home/login.html")

# View: Register Page
def register_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=username).first()

        if user_obj:
            messages.error(request, "Username is taken")
            return redirect('/register/')

        user_obj = User.objects.create(username=username)
        user_obj.set_password(password)
        user_obj.save()
        messages.success(request, "Account created")
        return redirect('/login/')

    return render(request, "home/register.html")

# View: Logout
def custom_logout(request):
    logout(request)
    return redirect('/login/')
