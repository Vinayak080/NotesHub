# #from django.shortcuts import render

# # Create your views here.

# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from .forms import NoteForm
# from django.http import FileResponse, HttpResponse
# from django.shortcuts import get_object_or_404
# #from django.contrib.auth.decorators import login_required
# import os
# from .models import Note

# # @login_required
# # def upload_note(request):
# #     if request.method == 'POST':
# #         form = NoteForm(request.POST, request.FILES)
# #         if form.is_valid():
# #             note = form.save(commit=False)

# #             # Convert comma-separated tags into list
# #             tags = form.cleaned_data['tags']
# #             if tags:
# #                 note.tags = [tag.strip() for tag in tags.split(',')]

# #             note.uploaded_by = request.user
# #             note.save()
# #             return redirect('note_list')
# #     else:
# #         form = NoteForm()

# #     return render(request, 'notes/upload_note.html', {'form': form})

# from .models import Note

# # def note_list(request):
# #     notes = Note.objects.all().order_by('-created_at')
# #     return render(request, 'notes/note_list.html', {'notes': notes})

# @login_required
# def download_note(request, note_id):
#     note = get_object_or_404(Note, id=note_id)

#     # Increment download count
#     note.download_count += 1
#     note.save()

#     return FileResponse(note.file.open(), as_attachment=True)


# from django.contrib.admin.views.decorators import staff_member_required

# @staff_member_required
# def upload_note(request):
#     if request.method == 'POST':
#         form = NoteForm(request.POST, request.FILES)
#         if form.is_valid():
#             note = form.save(commit=False)
#             note.uploaded_by = request.user
#             note.save()
#             return redirect('note_list')
#     else:
#         form = NoteForm()
#     return render(request, 'notes/upload_note.html', {'form': form})


# from django.db.models import Q

# def note_list(request):
#     query = request.GET.get('q')
#     notes = Note.objects.all()

#     if query:
#         notes = notes.filter(
#             Q(title__icontains=query) |
#             Q(subject__icontains=query)
#         )

#     return render(request, 'notes/note_list.html', {'notes': notes})


# from django.contrib.auth.decorators import login_required
# from django.shortcuts import get_object_or_404
# from django.http import FileResponse
# from .models import Note

# # @login_required
# # def download_note(request, note_id):
# #     note = get_object_or_404(Note, id=note_id)
# #     return FileResponse(note.file.open(), as_attachment=True)

# from django.shortcuts import get_object_or_404
# from django.http import FileResponse

# from django.contrib.auth.models import User

# def dashboard(request):
#     total_notes = Note.objects.count()
#     total_users = User.objects.count()

#     total_downloads = sum(note.download_count for note in Note.objects.all())

#     most_downloaded = Note.objects.order_by('-download_count').first()

#     context = {
#         'total_notes': total_notes,
#         'total_users': total_users,
#         'total_downloads': total_downloads,
#         'most_downloaded': most_downloaded
#     }

#     return render(request, 'notes/dashboard.html', context)

# from django.shortcuts import redirect

# def like_note(request, note_id):
#     note = get_object_or_404(Note, id=note_id)

#     note.likes += 1
#     note.save()

#     return redirect('note_list')

# from django.contrib.auth.forms import UserCreationForm
# from django.shortcuts import render, redirect

# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)

#         if form.is_valid():
#             form.save()
#             return redirect('login')

#     else:
#         form = UserCreationForm()

#     return render(request, 'notes/register.html', {'form': form})

# from django.contrib.auth.decorators import login_required


from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import logout

from .models import Note
from .forms import NoteForm


# -------------------------------
# Register User
# -------------------------------
# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)

#         if form.is_valid():
#             form.save()
#             return redirect('/accounts/login/')

#     else:
#         form = UserCreationForm()

#     return render(request, 'notes/register.html', {'form': form})

from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# def register(request):

#     if request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password1 = request.POST.get('password1')
#         password2 = request.POST.get('password2')

#         if password1 != password2:
#             return render(request, 'notes/register.html', {
#                 'error': 'Passwords do not match'
#             })

#         if User.objects.filter(username=username).exists():
#             return render(request, 'notes/register.html', {
#                 'error': 'Username already exists'
#             })

#         # Create user (important: hashed password)
#         user = User.objects.create_user(
#             username=username,
#             email=email,
#             password=password1
#         )

#         user.save()

#         return redirect('/login/')

#     return render(request, 'notes/register.html')

from django.contrib.auth.models import User
from django.shortcuts import render, redirect

def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            return render(request, "notes/register.html", {
                "error": "Passwords do not match"
            })

        if User.objects.filter(username=username).exists():
            return render(request, "notes/register.html", {
                "error": "Username already exists"
            })

        # Critical line (handles password hashing)
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        user.save()

        return redirect('/login/')

    return render(request, "notes/register.html")


# -------------------------------
# View Notes + Search
# -------------------------------
def note_list(request):
    query = request.GET.get('q')
    notes = Note.objects.all()

    if query:
        notes = notes.filter(
            Q(title__icontains=query) |
            Q(subject__icontains=query)
        )

    return render(request, 'notes/note_list.html', {'notes': notes})


# -------------------------------
# Upload Notes (Admin Only)
# -------------------------------
@staff_member_required
def upload_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)

        if form.is_valid():
            note = form.save(commit=False)

            tags = form.cleaned_data['tags']
            if tags:
                note.tags = [tag.strip() for tag in tags.split(',')]

            note.uploaded_by = request.user
            note.save()

            return redirect('note_list')

    else:
        form = NoteForm()

    return render(request, 'notes/upload_note.html', {'form': form})


# -------------------------------
# Download Notes (Login Required)
# -------------------------------
@login_required
def download_note(request, note_id):

    note = get_object_or_404(Note, id=note_id)

    note.download_count += 1
    note.save()

    return FileResponse(note.file.open(), as_attachment=True)


# -------------------------------
# Like Notes
# -------------------------------
def like_note(request, note_id):

    note = get_object_or_404(Note, id=note_id)

    note.likes += 1
    note.save()

    return redirect('note_list')


# -------------------------------
# Dashboard (Statistics)
# -------------------------------
def dashboard(request):

    total_notes = Note.objects.count()
    total_users = User.objects.count()

    total_downloads = sum(note.download_count for note in Note.objects.all())

    most_downloaded = Note.objects.order_by('-download_count').first()

    context = {
        'total_notes': total_notes,
        'total_users': total_users,
        'total_downloads': total_downloads,
        'most_downloaded': most_downloaded
    }

    return render(request, 'notes/dashboard.html', context)


def logout_view(request):
    logout(request)
    return redirect('note_list')