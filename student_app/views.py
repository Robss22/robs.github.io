from .forms import UploadContentForm
from django.conf import settings  # Import Django settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from student_app.models import CustomUser  # Import the User model from your app
from django.urls import reverse
from .models import Class  # Make sure to import your ClassModel
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
import os
from .models import UploadedFile  # Import your model

from .utils import allowed_file  # Import your allowed_file function if it's defined in a separate file
from django.contrib import messages  # Make sure you have imported messages
from django.http import HttpResponseServerError
import traceback
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.http import FileResponse  # Add this line
from django.shortcuts import render, redirect

from .models import Student  # Import your Student model
from .forms import UploadFileForm  # Assuming you have a form defined for the file upload
import pandas as pd
import csv
import openpyxl
from django.http import HttpResponse
from django.shortcuts import render
from .forms import StudentForm
import logging
from django.template import loader
from io import BytesIO
from django.shortcuts import get_object_or_404
from .models import Student, Course, Enrollment, Progress  # Import your models





from django.contrib.auth.hashers import make_password
logger = logging.getLogger(__name__)


def download_student_template(request):
    # Define the column headers for the template
    headers = ['name', 'gender', 'class_name', 'stream', 'photo', 'parents_name',
               'parents_contact', 'parents_email', 'admission_date', 'address']

    # Create a response object with the appropriate content type
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="student_template.csv"'

    # Create a CSV writer and write the headers to the response
    writer = csv.writer(response)
    writer.writerow(headers)

    return response

def process_row(row):
    # Replace this with your actual logic to create a Student instance
    return Student(
        name=row['name'],
        gender=row['gender'],
        class_name=row['class_name'],
        stream=row['stream'],
        dob=row['dob'],
        former_school=row['former_school'],
        scores=row['scores'],
        parents_name=row['parents_name'],
        parents_contact=row['parents_contact'],
        parents_email=row['parents_email'],
        admission_date=row['admission_date'],
        address=row['address'],
    )


def save_student(student):
    # Replace this with your actual logic to save the Student instance
    # This assumes you have defined a model named Student with the required fields
    student.save()


def upload_bulk_students_view(request):
    message = None
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES.get('file')
            if uploaded_file:
                if allowed_file(uploaded_file.name, allowed_extensions=['xlsx', 'xls']):
                    df = pd.read_excel(uploaded_file)
                    for index, row in df.iterrows():
                        student = process_row(row)
                        try:
                            student.save()
                        except Exception as e:
                            messages.error(request, f'Error saving student {student.name}: {e}')
                            continue
                    messages.success(request, 'Bulk students uploaded successfully!')
                else:
                    message = 'Invalid file extension.'
            else:
                message = 'No file selected.'
        else:
            message = 'Form errors.'
    else:
        form = StudentForm()
    
    context = {'form': form, 'message': message}
    return render(request, 'upload_bulk_students.html', context)






















def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions





def download_file(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id)
    file_path = os.path.join(settings.MEDIA_ROOT, str(file.file))
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{file.file.name}"'
    return response





def download_view(request):
    class_name = request.GET.get('class')
    subject = request.GET.get('subject')
    page = request.GET.get('page', 1)
    per_page = 10

    # Query the files based on class and subject
    query = UploadedFile.objects.all()
    if class_name and subject:
        query = query.filter(class_name=class_name, subject=subject)
    elif class_name:
        query = query.filter(class_name=class_name)
    elif subject:
        query = query.filter(subject=subject)

    # Pagination
    paginator = Paginator(query, per_page)
    files = paginator.get_page(page)

    context = {
        'files': files,
        'class_name': class_name,
        'subject': subject,
    }

    return render(request, 'download.html', context)



def download_by_class_and_subject(request, class_name, subject):
    page = request.GET.get('page', 1)
    per_page = 10

    # Query the files based on class and subject
    files = UploadedFile.objects.filter(class_name=class_name, subject=subject)

    # Pagination
    paginator = Paginator(files, per_page)
    files = paginator.get_page(page)

    # Retrieve the distinct class and subject values from the database
    classes = UploadedFile.objects.values('class_name').distinct()
    subjects = UploadedFile.objects.values('subject').distinct()

    return render(request, 'download.html', {'classes': classes, 'subjects': subjects, 'files': files})





def upload_content_view(request):
    if request.method == 'POST':
        form = UploadContentForm(request.POST, request.FILES)

        if form.is_valid():
            # Get form data
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            subject = form.cleaned_data['subject']
            class_name = form.cleaned_data['class_name']

            # Use request.user directly to get the currently logged-in user
            uploaded_by_user = request.user

            uploaded_file = UploadedFile(
                title=title,
                description=description,
                subject=subject,
                class_name=class_name,
                uploaded_by=uploaded_by_user,  # Set the uploaded_by field
                file=request.FILES['file']  # Assign the file directly to the model field
            )

            uploaded_file.save()

            messages.success(request, 'Content uploaded successfully!')
            return redirect('student_app:upload_content')  # Redirect to a success page or back to the upload form
        else:
            messages.error(request, 'Invalid form data')
    else:
        form = UploadContentForm()

    return render(request, 'upload_content.html', {'form': form, 'messages': messages.get_messages(request)})



def home(request):
    return render(request, 'home.html')


def contact(request):
    # Your view logic here
    return render(request, 'contact.html')

def applicationform(request):
    # Your view logic for the download view here
    return render(request, 'applicationform.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use authenticate to check credentials
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Authentication successful, log the user in
            login(request, user)

            if user.role == "0":
                return redirect('student_app:student_dashboard')
            elif user.role == "1":
                return redirect('student_app:teacher_dashboard')
            elif user.role == "2":
                return redirect('student_app:admin_dashboard')
        else:
            messages.error(request, 'Invalid login details. Please try again')

    # For GET requests or failed login attempts, render the login page
    return render(request, 'login.html')






def add_student_view(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            try:
                form.save()
                messages.success(request, 'Student added successfully!')
                return redirect('student_app:add_student')
            except Exception as e:
                print(f"Error saving student: {e}")
                return HttpResponseServerError("Error saving student data. Please try again.")
        else:
            print(f"Form errors: {form.errors}")
    else:
        form = StudentForm()
    
    return render(request, 'add_student.html', {'form': form})






def teacher_dashboard_view(request):
    # Your view logic for the download view here
    return render(request, 'teacher_dashboard.html')


def admin_dashboard_view(request):

    return render(request, 'admin_dashboard.html')



def upload_marks_view(request):

    return render(request, 'add_marks.html')


def add_user_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        name = request.POST.get('name')
        email = request.POST.get('email')  # Make sure to capture 'email' from the form

        # Check if the username already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('student_app:add_user')

        # Check if the email field is empty
        if not email:
            messages.error(request, 'Email cannot be empty.')
            return redirect('student_app:add_user')

        # Check if the email already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('student_app:add_user')

        # Hash the password before saving it
        hashed_password = make_password(password)

        # Create a new CustomUser instance and save it to the database
        custom_user = CustomUser(username=username, password=hashed_password, role=role, name=name, email=email)
        custom_user.save()

        messages.success(request, 'User added successfully.')
        return redirect('student_app:add_user')  # Redirect back to the registration page for more registrations

    return render(request, 'add_user.html')



def add_class_view(request):

    return render(request, 'add_class.html')




def add_subject_view(request):
    # Your view logic here
    return render(request, 'add_subject.html')



def logout_view(request):
    logout(request)
    # You can redirect to a different page after logout if needed
    return redirect('login')  # Assuming 'login' is the name of your login view.



@login_required
def student_dashboard_view(request):
    user_name = request.user.username 
    return render(request, 'student_dashboard.html', {'user_name': user_name})



def download_excel_template_view(request):
    # Create a new workbook and get the active sheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # Add headers for the fields in your "add student" form
    headers = [
            'name',
            'gender',
            'class_name',
            'stream',
            'photo',
            'dob',
            'former_school',
            'scores',
            'parents_name',
            'parents_contact',
            'parents_email',
            'admission_date',
            'address',
    ]
    
    # Add more headers based on your form fields

    sheet.append(headers)

    # Save the workbook to a BytesIO buffer
    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)

    response = HttpResponse(buffer.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=student_template.xlsx'

    return response







@login_required
def student_progress_view(request):
    student = get_object_or_404(Student, user=request.user)  # Assuming `user` field links to Student
    enrollments = Enrollment.objects.filter(student=student)
    progress_data = Progress.objects.filter(enrollment__in=enrollments)

    context = {
        'student': student,
        'enrollments': enrollments,
        'progress_data': progress_data,
    }

    return render(request, 'student_progress.html', context)





@login_required
def mark_attendance_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    student = get_object_or_404(Student, user=request.user)

    if request.method == 'POST':
        # Logic to mark attendance
        Attendance.objects.update_or_create(
            lesson=lesson,
            student=student,
            defaults={'attended': True}
        )
        messages.success(request, 'Attendance marked successfully.')
        return redirect('student_app:student_progress')

    return render(request, 'mark_attendance.html', {'lesson': lesson})



@login_required
def quiz_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        # Process quiz answers
        # Save results
        pass

    context = {
        'quiz': quiz,
    }
    return render(request, 'quiz.html', context)



@login_required
def exam_schedule_view(request):
    exams = Exam.objects.all()
    context = {
        'exams': exams,
    }
    return render(request, 'exam_schedule.html', context)



