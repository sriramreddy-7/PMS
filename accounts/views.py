from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from .models import RecruiterProfile, InstituteProfile, Profile, StudentProfile,JobOpening, InstituteProfile,JobApplication,Request
import pandas as pd
from django.db.models import Q
# Create your views here.
from django.utils.dateparse import parse_date
from django.db.models import Count


def test(request):
    return render(request, 'test.html')

def index(request):
    return render(request, 'index.html')

def signup(request):
    return render(request, 'signup.html')

@login_required
def student_dashboard(request):
    if request.user.profile.role != 'student':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')
    else:
        student = get_object_or_404(StudentProfile, user__username=request.user.username)
        context = {
            'student': student,
        }
        return render(request, 'student/dashboard.html',context)



@login_required
def institute_dashboard(request):
    if request.user.profile.role != 'institute':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')
    else:
        institute_profile = get_object_or_404(InstituteProfile, user=request.user)
        job_openings = JobOpening.objects.filter(institute=institute_profile)
        sent_requests = Request.objects.filter(sender=request.user)
        received_requests = Request.objects.filter(receiver=request.user)
    
    context = {
        'institute_profile': institute_profile,
        'job_openings': job_openings,
        'sent_requests': sent_requests,
        'received_requests': received_requests,
    } 
    return render(request, 'institute/dashboard.html',context)


def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if not email or not first_name or not last_name or not password or not role:
            messages.error(request, 'Please fill out all required fields.')
            return render(request, 'signup.html')

        # Create the user
        user = User.objects.create_user(username=email, email=email, first_name=first_name, last_name=last_name, password=password)

        # Create profile based on role
        profile = Profile(user=user, role=role)
        profile.save()

        if role == 'recruiter':
            organization_name = request.POST.get('organization_name')
            website = request.POST.get('website')
            location = request.POST.get('location')
            phone_number = request.POST.get('phone_number')
            designation = request.POST.get('designation')

            recruiter_profile = RecruiterProfile(user=user, organization_name=organization_name, website=website, location=location, contact_number=phone_number, designation=designation)
            recruiter_profile.save()

            messages.success(request, 'Recruiter account created successfully!')
            return redirect('login')  # Replace with your login URL

        elif role == 'institute':
            institute_name = request.POST.get('institute_name')
            website = request.POST.get('website')
            location = request.POST.get('location')
            contact_number = request.POST.get('phone_number')

            institute_profile = InstituteProfile(user=user, institute_name=institute_name, website=website, location=location, contact_number=contact_number)
            institute_profile.save()

            messages.success(request, 'Institute account created successfully!')
            return redirect('login')  # Replace with your login URL

        elif role == 'student':
            contact_number = request.POST.get('phone_number')
            resume = request.FILES.get('resume')
            education = request.POST.get('education')
            institute_id = request.POST.get('institute_id')

            if not contact_number or not education or not institute_id:
                messages.error(request, 'Please fill out all required fields.')
                return render(request, 'signup.html')

            institute = InstituteProfile.objects.get(id=institute_id)
            student_profile = StudentProfile(user=user, contact_number=contact_number, resume=resume, education=education, institute=institute)
            student_profile.save()

            messages.success(request, 'Student account created successfully!')
            return redirect('login')  # Replace with your login URL

        else:
            messages.error(request, 'Invalid role selected.')

    # If GET request or form is invalid, render the signup form
    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        if not username_or_email or not password:
            messages.error(request, 'Please fill out all required fields.')
            return render(request, 'login.html')
        
        # Attempt to authenticate using the username or email
        user = None
        if '@' in username_or_email:
            try:
                user_obj = User.objects.get(email=username_or_email)
                username = user_obj.username
                user = authenticate(request, username=username, password=password)
            except User.DoesNotExist:
                user = None
        else:
            user = authenticate(request, username=username_or_email, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login successful!')
            if user.profile.role == 'student':
                return redirect('student_dashboard')
            elif user.profile.role == 'recruiter':
                return redirect('recruiter_dashboard')
            elif user.profile.role == 'institute':
                return redirect('institute_dashboard')
            else:
                messages.error(request, 'Invalid role.')
                return render(request, 'login.html')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')

    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def bulk_student_upload(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        password = request.POST.get('password')

        # Check if the uploaded file is CSV
        if not csv_file.name.endswith('.csv'):
            error_message = 'File is not in CSV format.'
            return render(request, 'institute/bulk_student_upload.html', {'error_message': error_message})

        try:
            # Read CSV file into pandas DataFrame
            df = pd.read_csv(csv_file)

            # Normalize column names by stripping leading/trailing spaces
            df.columns = df.columns.str.strip()

            # Strip leading/trailing spaces from all data
            df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
            institute_profile = InstituteProfile.objects.get(user=request.user)
            role = 'student'
            # Convert DataFrame to list of dictionaries
            for index, row in df.iterrows():
                email = row['Email']
                first_name = row['First_Name']
                last_name = row['Last_Name']
                username = row['Username']
                
                if email == "":
                    break

                print(email, first_name, last_name, password, username, institute_profile)

                if not User.objects.filter(username=username).exists():
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                        password=password
                    )
                    user.save()
                    print(f"User {username} created successfully.")
                    profile = Profile(user=user, role=role)
                    profile.save()
                    
                    # Assuming request.user is the institute user
                    institute_profile = InstituteProfile.objects.get(user=request.user)

                    student_profile = StudentProfile.objects.create(
                        user=user,
                        institute=institute_profile,
                        contact_number='',
                        resume=None,
                    )
                    student_profile.save()
                else:
                    messages.warning(request, f'User {username} already exists and was skipped.')
                    print(f"User {username} already exists and was skipped.")
            
            data = df.to_dict('records')
            return render(request, 'institute/bulk_student_upload.html', {'data': data})

        except Exception as e:
            error_message = f'Error processing CSV file: {str(e)}'
            return render(request, 'institute/bulk_student_upload.html', {'error_message': error_message})

    return render(request, 'institute/bulk_student_upload.html')

@login_required
def student_details(request):
    try:
        # Retrieve the InstituteProfile object associated with the current user
        institute_profile = get_object_or_404(InstituteProfile, user=request.user)
        
        # Retrieve all StudentProfile objects associated with this institute
        students = StudentProfile.objects.filter(institute=institute_profile)
    except InstituteProfile.DoesNotExist:
        institute_profile = None
        students = None

    context = {
        'institute_profile': institute_profile,
        'students': students,
    }
    return render(request, 'institute/student_details.html', context)

@login_required
def student_profile(request, username):
    print("he")
    institute_profile = get_object_or_404(InstituteProfile, user=request.user)
    student = get_object_or_404(StudentProfile, user__username=username)
    context = {
        'institute_profile': institute_profile,
        'student': student,
    }
    return render(request, 'institute/student_profile.html', context)

@login_required
def student_account(request, username):
    print("she")
    student = get_object_or_404(StudentProfile, user__username=username)
    context = {
        'student': student,
    }
    return render(request, 'student/student_account.html', context)

@login_required
def student_details_update(request):
    student_profile = request.user.student_profile
    if request.method == 'POST':
        # Update fields based on form data
        student_profile.degree = request.POST.get('degree', '')
        student_profile.branch_specialization = request.POST.get('branch_specialization', '')
        student_profile.year_of_passout = request.POST.get('year_of_passout', '')
        student_profile.contact_number = request.POST.get('contact_number', '')
        student_profile.resume = request.FILES.get('resume', student_profile.resume)
        
        # Check if a new profile picture is uploaded
        if 'profile_picture' in request.FILES:
            student_profile.profile_picture = request.FILES['profile_picture']

        # Save the updated profile
        student_profile.save()

        # Display success message and redirect to student dashboard
        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('student_dashboard')

    # Render the update profile form with current profile data
    return render(request, 'student/update_profile.html', {'student_profile': student_profile})


def all_recruiters(request):
    recruiters = RecruiterProfile.objects.all()
    context = {
        'recruiters': recruiters,
    }
    return render(request, 'institute/all_recruiters.html', context)


@login_required
def post_job_opening(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        deadline = request.POST.get('deadline')
        post = request.POST.get('post')
        job_type = request.POST.get('job_type')
        company = request.POST.get('company')
        institute_profile = InstituteProfile.objects.get(user=request.user)
        
        # Create job opening instance
        job_opening = JobOpening(
            institute=institute_profile,
            title=title,
            description=description,
            deadline=deadline,
            post=post,
            job_type=job_type,
            company=company,
        )
        job_opening.save()
        
        messages.success(request, 'Job opening posted successfully.')
        return redirect('institute_job_data')  # Redirect to institute dashboard
    
    return render(request, 'institute/institute_post_job.html')

def institute_job_data(request):
    # Retrieve job openings for the current institute
    institute = InstituteProfile.objects.get(user=request.user)
    job_openings = JobOpening.objects.filter(institute=institute)
    
    data = []
    for job in job_openings:
        total_applications = job.applications.count()  # Replace with actual related name for applications
        total_students = institute.students.count()  # Replace with actual related name for students
        if total_students > 0:
            percentage = (total_applications / total_students) * 100
        else:
            percentage = 0  # or handle as needed
        data.append({
            'job': job,
            'total_applications': total_applications,
            'percentage': percentage,
        })

    context = {
        'job_openings': job_openings,
        'job_data': data,
    }
    return render(request, 'institute/institute_job_data.html', context)

def edit_job(request, job_id):
    job = get_object_or_404(JobOpening, id=job_id)
    if request.method == 'POST':
        job.title = request.POST.get('title')
        job.company = request.POST.get('company')
        job.description = request.POST.get('description')
        job.deadline = parse_date(request.POST.get('deadline'))
        job.job_type = request.POST.get('job_type')
        job.post = request.POST.get('post')
        job.status = request.POST.get('status')
        job.save()
        return redirect('institute_job_data')
    context = {
        'job': job
    }
    return render(request, 'institute/institute_job_data.html', context)

def delete_job(request, job_id):
    job = get_object_or_404(JobOpening, id=job_id)
    job.delete()
    return redirect('institute_job_data')


@login_required
def student_job_openings(request):
    student_profile = StudentProfile.objects.get(user=request.user)
    print(student_profile.institute)
    job_openings = JobOpening.objects.filter(institute=student_profile.institute, status='open')
    return render(request, 'student/student_job_openings.html', {'job_openings': job_openings})


@login_required
def student_job_applications(request):
    student_profile = StudentProfile.objects.get(user=request.user)
    applications = JobApplication.objects.filter(student=student_profile)
    job_openings = JobOpening.objects.filter(institute=student_profile.institute, status='open')

    if request.method == 'POST':
        application_id = request.POST.get('application_id')
        new_status = request.POST.get('status')
        new_job_opening_id = request.POST.get('new_job_opening')

        if application_id and new_status:
            application = get_object_or_404(JobApplication, id=application_id, student=student_profile)
            if new_status in ['pending', 'accepted', 'rejected']:
                application.status = new_status
                application.save()
                messages.success(request, 'Application status updated successfully.')
            else:
                messages.error(request, 'Invalid status.')

        elif new_job_opening_id:
            job_opening = get_object_or_404(JobOpening, id=new_job_opening_id)
            JobApplication.objects.create(student=student_profile, job_opening=job_opening, status='pending')
            messages.success(request, 'New job application added successfully.')

        return redirect('student_job_applications')

    return render(request, 'student/student_job_applications.html', {'applications': applications, 'job_openings': job_openings})



@login_required
def institute_student_off_campus_jobs_status(request):
    institute_profile = InstituteProfile.objects.get(user=request.user)
    job_openings = JobOpening.objects.filter(institute=institute_profile, job_type='off_campus')
    
    # Group applications by company and fetch their statuses
    job_applications = JobApplication.objects.filter(job_opening__in=job_openings).select_related('job_opening__institute')
    companies = {}
    for application in job_applications:
        company_name = application.job_opening.company
        if company_name not in companies:
            companies[company_name] = []
        companies[company_name].append(application)

    context = {
        'companies': companies
    }
    return render(request, 'institute/institute_student_off_campus_jobs_status.html', context)



def institute_job_applications(request, job_id):
    job = get_object_or_404(JobOpening, id=job_id)
    applications = JobApplication.objects.filter(job_opening=job)
    return render(request, 'institute/institute_job_applications.html', {'job': job, 'applications': applications})



@login_required
def edit_institute_profile(request):
    user = request.user
    institute_profile = get_object_or_404(InstituteProfile, user=user)

    if request.method == 'POST':
        institute_name = request.POST.get('institute_name')
        website = request.POST.get('website')
        location = request.POST.get('location')
        contact_number = request.POST.get('contact_number')
        state = request.POST.get('state')
        country = request.POST.get('country')
        # Handle file upload for logo
        if 'logo' in request.FILES:
            logo = request.FILES['logo']
            institute_profile.logo = logo
        institute_profile.institute_name = institute_name
        institute_profile.website = website
        institute_profile.location = location
        institute_profile.contact_number = contact_number
        institute_profile.state = state
        institute_profile.country = country
        institute_profile.save()
        return redirect('view_institute_profile')  # Replace with your desired redirect

    return render(request, 'institute/edit_institute_profile.html', {'institute_profile': institute_profile})


@login_required
def view_institute_profile(request):
    user = request.user
    try:
        institute_profile = InstituteProfile.objects.get(user=user)
    except InstituteProfile.DoesNotExist:
        messages.error(request, 'Institute profile does not exist.')
        return redirect('home')  # Redirect to home or another appropriate view
    
    context = {
        'institute': institute_profile,
    }
    return render(request, 'institute/institute_details_view.html', context)




@login_required
def recruiter_dashboard(request):
    # Retrieve all available institute
    if request.user.profile.role != 'recruiter':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')
    # institutes = InstituteProfile.objects.all()
    institutes = InstituteProfile.objects.annotate(num_students=Count('students'))
    recruiter_profile=request.user.recruiter_profile
    context = {
        'institutes': institutes,
        'recruiter_profile':recruiter_profile,
    }
    return render(request, 'recruiter/dashboard.html', context)

@login_required
def send_request(request, institute_id):
    if request.method == 'POST':
        recruiter = request.user.recruiter_profile  # Assuming recruiter profile is linked to User
        institute = get_object_or_404(InstituteProfile, pk=institute_id)
        request_type = 'recruiter_to_institute'
        
        # Check if a similar request already exists
        existing_request = Request.objects.filter(
            Q(sender=request.user, receiver=institute.user) |
            Q(sender=institute.user, receiver=request.user),
            request_type=request_type,
            status='pending'
        ).exists()
        
        if existing_request:
            messages.warning(request, 'Request already sent. Please wait for a response.')
        else:
            # Create a new request
            request_obj = Request.objects.create(
                request_type=request_type,
                sender=request.user,
                receiver=institute.user,
                status='pending'
            )
            messages.success(request, 'Request sent successfully.')
        
        return redirect('recruiter_dashboard')

@login_required
def institute_requests(request):
    if request.user.profile.role != 'institute':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')
    institute_profile = request.user.institute_profile  # Assuming institute profile is linked to User
    received_requests = Request.objects.filter(receiver=request.user)
    context = {
        'requests': received_requests,
        'institute_profile': institute_profile,
    }
    return render(request, 'institute/institute_requests.html', context)

@login_required
def manage_request(request, request_id):
    request_obj = get_object_or_404(Request, pk=request_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            request_obj.status = 'accepted'
            # Implement logic to share student details here
            messages.success(request, 'Request accepted.')
        elif action == 'decline':
            request_obj.status = 'declined'
            messages.success(request, 'Request declined.')
        request_obj.save()
        return redirect('institute_requests')

@login_required
def institute_list(request):
    if request.user.profile.role != 'recruiter':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')
    
    # Fetch all accepted requests for the current recruiter
    accepted_requests = Request.objects.filter(sender=request.user, status='accepted')
    
    # Use a set to store unique institutes
    unique_institutes = set()
    institute_list = []
    
    for req in accepted_requests:
        institute = req.receiver.institute_profile
        
        # Check if institute already exists in set, skip if it does
        if institute.id in unique_institutes:
            continue
        
        # Add institute id to set to mark it as processed
        unique_institutes.add(institute.id)
        
        # Calculate shared student count
        shared_students_count = StudentProfile.objects.filter(institute=institute).count()
        is_accepted = req.status == 'accepted'
        
        institute_list.append({
            'id': institute.id,
            'name': institute.institute_name,
            'accepted': is_accepted,
            'shared_students_count': shared_students_count,
        })
    recruiter_profile = request.user.recruiter_profile
    context = {
        'institute_list': institute_list,
        'recruiter_profile':recruiter_profile,
    }
    return render(request, 'recruiter/institute_list.html', context)






@login_required
def view_shared_students(request, institute_id):
    # Ensure only recruiters can access this view
    if request.user.profile.role != 'recruiter':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')
    
    institute = get_object_or_404(InstituteProfile, pk=institute_id)
    
    # accepted_requests = Request.objects.filter(receiver=request.user, status='accepted')
    
    # shared_students = StudentProfile.objects.filter(
    #     institute=institute,
    #     id__in=[req.sender.student_profile.id for req in accepted_requests]
    # )
    shared_students = StudentProfile.objects.filter(institute=institute)
    recruiter_profile = request.user.recruiter_profile
    context = {
        'institute': institute,
        'shared_students': shared_students,
        'recruiter_profile':recruiter_profile,
    }
    return render(request, 'recruiter/view_shared_students.html', context)



@login_required
def list_shared_students(request):
    if request.user.profile.role != 'recruiter':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')
    
    recruiter = request.user.recruiter_profile
    recruiter_profile=recruiter
    accepted_requests = Request.objects.filter(sender=request.user, status='accepted')
    students = StudentProfile.objects.filter(institute__in=[req.receiver.institute_profile for req in accepted_requests])
    
    context = {
        'students': students,
        'recruiter_profile':recruiter_profile,
    }
    return render(request, 'recruiter/list_shared_students.html', context)


@login_required
def recruiter_student_profile(request, username):
    # Ensure only recruiters can access this view
    recruiter_profile = request.user.recruiter_profile
    if request.user.profile.role != 'recruiter':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('login')
    
    # Retrieve the student profile
    student = get_object_or_404(StudentProfile, user__username=username)
    
    context = {
        'student': student,
        'recruiter_profile':recruiter_profile,
    }
    return render(request, 'recruiter/recruiter_student_profile.html', context)


def institute_profile(request, institute_id):
    try:
        institute_profile = InstituteProfile.objects.get(id=institute_id)
    except InstituteProfile.DoesNotExist:
        messages.error(request, 'Institute profile does not exist.')
        return redirect('home')  # Redirect to home or another appropriate view
    recruiter_profile = request.user.recruiter_profile
    context = {
        'institute': institute_profile,
        'recruiter_profile':recruiter_profile,
    }
    return render(request, 'recruiter/institute_profile.html', context)


@login_required
def recruiter_profile(request):
    recruiter_profile = request.user.recruiter_profile
    context = {
        'recruiter_profile': recruiter_profile,
    }
    return render(request, 'recruiter/recruiter_profile.html', context)




@login_required
def edit_recruiter_profile(request):
    recruiter_profile = request.user.recruiter_profile
    
    if request.method == 'POST':
        recruiter_profile.organization_name = request.POST.get('organization_name')
        recruiter_profile.website = request.POST.get('website')
        recruiter_profile.location = request.POST.get('location')
        recruiter_profile.contact_number = request.POST.get('contact_number')
        recruiter_profile.designation = request.POST.get('designation')
        
        # Handle logo update
        if 'logo' in request.FILES:
            recruiter_profile.logo = request.FILES['logo']
        
        recruiter_profile.save()
        return redirect('recruiter_profile')
    
    context = {
        'recruiter_profile': recruiter_profile,
    }
    return render(request, 'recruiter/edit_recruiter_profile.html', context)