# Create your views here.
import os
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_protect
from django import template
from django.core.files.uploadhandler import FileUploadHandler
from django.core.files.base import ContentFile
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from formapp.forms import LoginForm, RegistrationForm, UploadImageForm, PhotoAlbumForm
from formapp.models import UserProfile, UploadPhoto, PhotoAlbum
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.template import RequestContext
from settings import MEDIA_ROOT

def login_user(request, login_template):
    def errorHandle(error):
        form = LoginForm()
        return render_to_response(login_template, {
                          'error' : error,
                          'form' : form,
        })

    if request.method == 'POST': # If the form has been submitted...
        form = LoginForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            username = request.POST['username']
            password = request.POST['password']
            from django.contrib.auth import authenticate
            user = authenticate(username=username, password=password)
            if user:
                from django.contrib.auth import login
                login(request, user)
                #request.session.session_key = username
                return HttpResponseRedirect(reverse("home"))

            else:
                error = u"Authentication Failed "
                return errorHandle(error)
        else:
            error = u'Username and Password should not be empty'
            return errorHandle(error)
    else:
        form = LoginForm() # An unbound form
        return render_to_response(login_template, {
                'form': form,
                })

def register_user(request, register_template):
    def errorHandle(error):
        form = RegistrationForm()
        return render_to_response(register_template, {
                          'error' : error,
                          'form' : form,
        })
    if request.method == 'POST': # If the form has been submitted...
        form = RegistrationForm(request.POST) # A form bound to the POST data
        register_obj = UserProfile()
        if form.is_valid(): # All validation rules pass
            uname = request.POST['username']
            fname = request.POST['first_name']
            lname = request.POST['last_name']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if password1 != password2:
                error = u'Password must be same'
                return errorHandle(error)
            email = request.POST['email']
            user_exists = UserProfile.objects.user_exists(uname)
            if not user_exists:
                UserProfile.objects.save_user(uname, fname, lname, email, password1)
                return HttpResponseRedirect('/login/')
            else:
                error = u'User already exist'
                return errorHandle(error)
        else:
            error = u'Fields should not empty'
            return errorHandle(error)
    else:
        form = RegistrationForm() # An unbound form
        return render_to_response('fapp/register.html', {
                'form': form,
                })

def home_page(request, logged_in_template):
    img_cap_list = []
    context = RequestContext(request)
    if request.user.is_active:
        user_exists = UserProfile.objects.get(user = request.user)
        photo_album = PhotoAlbum()
        if not photo_album.album_exists('default'):
            photo_album.album_name = 'default'
            photo_album.description = "Default Album"
            photo_album.user = user_exists
            photo_album.user_id = user_exists.user_id
            photo_album.save()
        img_cap_list_dict = PhotoAlbum.objects.filter(user = request.user).values('album_name', 'description')
        img_cap_list = map(lambda img_cap_dict: (str(img_cap_dict['album_name']),str(img_cap_dict['description'])),img_cap_list_dict)
        context['photos'] = img_cap_list
        return render_to_response(logged_in_template, {'request': request}, context_instance=context)
    else: return HttpResponseRedirect(reverse("login"))

def upload_photo_page(request, album_name, upload_photo_template):
    if request.user.is_active:
        #import pdb;pdb.set_trace()
        if request.method == 'POST':
            img_cap_list = []
            user_exists = UserProfile.objects.get(user = request.user)
            user_photo = UploadPhoto()
            if not album_name:
                album_name = request.POST['album']
            photo_album = PhotoAlbum.objects.get(user = request.user, album_name = album_name)
            form = UploadImageForm(request.POST, request.FILES)
            form.handle_uploaded_file(request.FILES['image'], request.user.username, album_name)
            user_photo.image = request.FILES['image']
            user_photo.img_path = os.path.join(MEDIA_ROOT, request.user.username)
            user_photo.caption = request.POST['caption']
            user_photo.user = user_exists
            user_photo.user_id = user_exists.user_id
            user_photo.album = photo_album
            user_photo.album_id = photo_album.id
            user_photo.save()
            return HttpResponseRedirect('/home/')
        elif request.path == '/upload/':
            album_list = PhotoAlbum.objects.filter(user = request.user).values('album_name')
            album_list = map(lambda albums: str(albums['album_name']),album_list)
            #album_list.remove('default')
            form = UploadImageForm() # An unbound form
            return render_to_response(upload_photo_template, {
                    'form': form,
                    'album_list': album_list 
                    })
        else:
            form = UploadImageForm() # An unbound form
            return render_to_response(upload_photo_template, {
                    'form': form,
                    })
    else: return HttpResponseRedirect(reverse("login"))

def display_album_page(request, album_name, display_album_template):
    img_cap_list = []
    context = RequestContext(request)
    if request.user.is_active:
        img_cap_list_dict = UploadPhoto.objects.filter(user = request.user, album__album_name=album_name).values('image', 'caption')
        img_cap_list = map(lambda img_cap_dict: (str(img_cap_dict['image']),str(img_cap_dict['caption'])),img_cap_list_dict)
        context['photos'] = img_cap_list
        return render_to_response(display_album_template, {'request': request, 'album_name': album_name}, context_instance=context)
    else: return HttpResponseRedirect(reverse("login"))

def create_album_page(request, new_album_template):
    if request.user.is_active:
        if request.method == 'POST': # If the form has been submitted...
            user_exists = UserProfile.objects.get(user = request.user)
            album_obj = PhotoAlbum()
            album_obj.album_name = request.POST['album_name']
            album_obj.description = request.POST['description']
            album_obj.user = user_exists
            album_obj.user_id = user_exists.user_id
            album_obj.save()
            return HttpResponseRedirect('/home/')
        else:
            form = PhotoAlbumForm() # An unbound form
            return render_to_response(new_album_template, {
                    'form': form,
                    })
    else: return HttpResponseRedirect(reverse("login"))

def logout_page(request, log_out_template):
    from django.contrib.auth import logout
    logout(request)
    form = LoginForm()
    return HttpResponseRedirect(reverse("login"))
