from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.validators import RegexValidator

class Term(models.IntegerChoices):
    FIRST_TERM = 1
    SECOND_TERM = 2
    THIRD_TERM = 3

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=150)
    role = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    date_joined = models.DateTimeField(default=timezone.now)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['role', 'name', 'email']

    def __str__(self):
        return self.username



class Student(models.Model):
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=[('F', 'Female'), ('M', 'Male')])
    class_name = models.CharField(max_length=255)
    stream = models.CharField(max_length=255, choices=[('A', 'A'), ('B', 'B'), ('Arts', 'Arts'), ('Sciences', 'Sciences')])
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    dob = models.DateField()
    former_school = models.CharField(max_length=255)
    scores = models.IntegerField()
    parents_name = models.CharField(max_length=255)
    parents_contact = models.CharField(max_length=15)
    parents_email = models.EmailField()
    admission_date = models.DateField(null=True)
    address = models.TextField()

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

class Subject(models.Model):
    subject_name = models.CharField(max_length=50)

    def __str__(self):
        return self.subject_name

class Class(models.Model):
    class_name = models.CharField(max_length=10)
    stream = models.CharField(max_length=10, choices=[('A', 'A'), ('B', 'B'), ('Arts', 'Arts'), ('Science', 'Science')])

    def __str__(self):
        return self.class_name



class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    progress = models.FloatField(default=0)  # Progress as a percentage

    def __str__(self):
        return f"{self.student.user.username} - {self.course.title}"


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    order = models.IntegerField()  # Order of the lesson in the course

    def __str__(self):
        return self.title

class LessonCompletion(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.lesson.title}"

class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()

    def __str__(self):
        return self.title

class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.TextField()

    def __str__(self):
        return self.question_text

class QuizAnswer(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    answer_text = models.TextField()
    is_correct = models.BooleanField()

    def __str__(self):
        return self.answer_text

class QuizSubmission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField()
    score = models.FloatField()

    def __str__(self):
        return f"{self.student.user.username} - {self.quiz.title}"

class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    scheduled_date = models.DateTimeField()

    def __str__(self):
        return self.title

class ExamResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    result = models.FloatField()  # Exam score
    completed_at = models.DateTimeField()

    def __str__(self):
        return f"{self.student.user.username} - {self.exam.title}"

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title





class UploadedFile(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    subject = models.CharField(max_length=100)
    class_name = models.CharField(max_length=100)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.title





class Progress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    progress = models.FloatField()  # Example field

    def __str__(self):
        return f"{self.student} - {self.course} - {self.progress}"

