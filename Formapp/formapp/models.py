from django.db import models
from django.contrib.auth.models import User

class UserProfileManager(models.Manager):

    def user_exists(self, username):
        try:
            user = UserProfile.objects.get(username = username)
            return True
        except Exception, e:
            return False

    def save_user(self, username, fname, lname, personal_email, password):
        user_object = User.objects.create_user(username, personal_email, password)
        user_profile = UserProfile()
        user_profile.user = user_object
        user_profile.username = username
        user_profile.first_name = fname
        user_profile.last_name = lname
        user_profile.personal_email = personal_email
        user_profile.password = password
        user_profile.is_active = False
        user_profile.save()
        return True

class UserProfile(models.Model):
    id = models.AutoField(primary_key = True)
    user = models.OneToOneField(User)
    username = models.CharField(max_length=200, blank=False, unique=True)
    first_name = models.CharField(max_length=200, blank=False)
    last_name = models.CharField(max_length=200)
    personal_email = models.EmailField()
    password = models.CharField(blank=False, max_length=20)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now = True)
    objects = UserProfileManager()

#    def __str__(self):
#        return 'User - %s' (self.username)


class PhotoAlbum(models.Model):
    id = models.AutoField(primary_key = True)
    user = models.ForeignKey(UserProfile)
    album_name = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return 'album_name - %s, description - %s' % (self.album_name, self.description)

    def album_exists(self, album_name):
        try:
            album = PhotoAlbum.objects.get(album_name = album_name)
            return True
        except Exception, e:
            return False



class UploadPhoto(models.Model):
    id = models.AutoField(primary_key = True)
    user = models.ForeignKey(UserProfile)
    album = models.ForeignKey(PhotoAlbum)
    image = models.CharField(max_length=1000)
    img_path = models.CharField(blank=False, max_length=1000)
    caption = models.CharField(blank=False, max_length=200)

    def __str__(self):
        return 'image - %s, caption - %s path - %s' % (self.image, self.caption, self.img_path)
