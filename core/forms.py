# forms.py
from django import forms

class CertificateIssueForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "w-full bg-white dark:bg-gray-700 text-gray-800 dark:text-white border border-gray-300 dark:border-gray-600 rounded-md p-2",
        "placeholder": "Enter Student Name"
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "w-full bg-white dark:bg-gray-700 text-gray-800 dark:text-white border border-gray-300 dark:border-gray-600 rounded-md p-2",
        "placeholder": "Enter Student Email"
    }))
    roll_no = forms.CharField(widget=forms.TextInput(attrs={
        "class": "w-full bg-white dark:bg-gray-700 text-gray-800 dark:text-white border border-gray-300 dark:border-gray-600 rounded-md p-2",
        "placeholder": "Enter Roll Number"
    }))
    course_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "w-full bg-white dark:bg-gray-700 text-gray-800 dark:text-white border border-gray-300 dark:border-gray-600 rounded-md p-2",
        "placeholder": "Course Name"
    }))
    percentage = forms.DecimalField(widget=forms.NumberInput(attrs={
        "class": "w-full bg-white dark:bg-gray-700 text-gray-800 dark:text-white border border-gray-300 dark:border-gray-600 rounded-md p-2",
        "placeholder": "Percentage / CGPA"
    }))
    status = forms.CharField(widget=forms.TextInput(attrs={
        "class": "w-full bg-white dark:bg-gray-700 text-gray-800 dark:text-white border border-gray-300 dark:border-gray-600 rounded-md p-2",
        "placeholder": "Status (e.g. Course Completed)"
    }))
