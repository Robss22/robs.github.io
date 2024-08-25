from django import forms
from .models import UploadedFile, Student

class UploadContentForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['title', 'description', 'subject', 'class_name', 'file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if not file.name.endswith(('.pdf', '.doc', '.docx', '.ppt', '.pptx')):
                raise forms.ValidationError('Unsupported file extension. Only PDF, DOC, DOCX, PPT, and PPTX files are allowed.')
        return file


class UploadFileForm(forms.Form):
    file = forms.FileField(
        label='Select Excel File',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if not file.name.endswith(('.xlsx', '.xls')):
                raise forms.ValidationError('Invalid file extension. Only .xlsx and .xls files are allowed.')
        return file


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
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
        widgets = {
            'class_name': forms.Select(choices=[
                ('S1', 'S1'), ('S2', 'S2'), ('S3', 'S3'),
                ('S4', 'S4'), ('S5', 'S5'), ('S6', 'S6')
            ]),
            'stream': forms.Select(choices=[
                ('A', 'A'), ('B', 'B'), ('Arts', 'Arts'), ('Sciences', 'Sciences')
            ]),
            'photo': forms.FileInput(attrs={'accept': 'image/*'}),
            'gender': forms.Select(choices=[
                ('F', 'Female'), ('M', 'Male')
            ]),
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'admission_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo'].required = False
        self.fields['photo'].initial = None

    def clean_scores(self):
        scores = self.cleaned_data.get('scores')
        if scores is not None and scores < 0:
            raise forms.ValidationError('Scores must be a positive number.')
        return scores

    def clean_parents_contact(self):
        contact = self.cleaned_data.get('parents_contact')
        if contact and not contact.isdigit():
            raise forms.ValidationError('Parents contact number must be digits only.')
        return contact
