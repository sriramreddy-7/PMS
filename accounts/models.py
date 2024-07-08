from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('recruiter', 'Recruiter'),
        ('admin', 'Admin'),
        ('institute', 'Institute'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f'{self.user.username} - {self.role}'

class InstituteProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='institute_profile')
    institute_name = models.CharField(max_length=255)
    website = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True, default=None)
    country = models.CharField(max_length=100, blank=True, null=True, default=None)
    logo = models.ImageField(upload_to='institute_logos/', blank=True, null=True, default=None)
    
    def __str__(self):
        return self.institute_name
    
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    institute = models.ForeignKey(InstituteProfile, on_delete=models.CASCADE, related_name='students')
    degree = models.CharField(max_length=100, blank=True, null=True,default=None)
    branch_specialization = models.CharField(max_length=100, blank=True, null=True,default=None)
    year_of_passout = models.IntegerField(blank=True, null=True,default=None)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, default=None)
    cgpa = models.FloatField(blank=True, null=True, default=None)

    def __str__(self):
        return f'{self.user.username} - Student'
    

def upload_location(instance, filename):
    return f"recruiter_profiles/{instance.user.username}/{filename}"

class RecruiterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='recruiter_profile')
    organization_name = models.CharField(max_length=255, default='Default Organization')
    website = models.URLField(blank=True, null=True, default=None)
    location = models.CharField(max_length=255, blank=True, null=True, default=None)
    contact_number = models.CharField(max_length=15, blank=True, null=True, default=None)
    designation = models.CharField(max_length=255, default='Default Designation')
    logo = models.ImageField(upload_to=upload_location, blank=True, null=True,default=None)

    def __str__(self):
        return self.organization_name

class JobOpening(models.Model):
    institute = models.ForeignKey(InstituteProfile, on_delete=models.CASCADE, related_name='job_openings')
    title = models.CharField(max_length=255)
    company=models.CharField(max_length=255,default="None")
    description = models.TextField()
    posted_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField()
    post=models.URLField(default="None")
    job_type_choices = [
        ('off_campus', 'Off Campus'),
        ('on_campus', 'On Campus'),
    ]
    job_type = models.CharField(max_length=10, choices=job_type_choices)
    status_choices = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='open')

    def __str__(self):
        return self.title

class JobApplication(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='job_applications')
    job_opening = models.ForeignKey(JobOpening, on_delete=models.CASCADE, related_name='applications')
    application_date = models.DateTimeField(auto_now_add=True)
    status_choices = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='pending')

    def __str__(self):
        return f'{self.student.user.username} - {self.job_opening.title}'
    
    
    
class Request(models.Model):
    REQUEST_TYPES = [
        ('recruiter_to_institute', 'Recruiter to Institute'),
        ('institute_to_recruiter', 'Institute to Recruiter'),
    ]
    
    request_type = models.CharField(max_length=50, choices=REQUEST_TYPES)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    status_choices = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='pending')

    def __str__(self):
        return f'{self.get_request_type_display()} - {self.sender.username} -> {self.receiver.username}'
    
    
    
class Skill(models.Model):
    SKILL_CHOICES = [
        ('Python', 'Python'),
        ('Java', 'Java'),
        ('JavaScript', 'JavaScript'),
        ('C++', 'C++'),
        ('Ruby', 'Ruby'),
        ('PHP', 'PHP'),
        ('HTML/CSS', 'HTML/CSS'),
        ('SQL', 'SQL'),
        ('Data Analysis', 'Data Analysis'),
        ('Machine Learning', 'Machine Learning'),
        ('UI/UX Design', 'UI/UX Design'),
        ('Project Management', 'Project Management'),
        ('Leadership', 'Leadership'),
        ('Communication', 'Communication'),
        ('Problem Solving', 'Problem Solving'),
        ('Teamwork', 'Teamwork'),
    ]
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='skills')
    skill = models.CharField(max_length=100, choices=SKILL_CHOICES)

    def __str__(self):
        return self.skill   