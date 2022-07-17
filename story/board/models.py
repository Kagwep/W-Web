import email
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from story.settings import AUTH_USER_MODEL
from django.conf import settings

class UserRegManager(BaseUserManager):
    def create_user(self,email,username,first_name,last_name,phone_number,password=None ):
        if not email:
            return ValueError('please enter your email')
        if not username:
            return ValueError('please enter your username max of six characters')
        if not first_name:
            return ValueError('please enter your first_name')
        if not last_name:
            return ValueError('please enter last name')
        if not phone_number:
            return ValueError('please enter your phone number')
        

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name =first_name,
            last_name = last_name,
            phone_number = phone_number

        )

        user.set_password(password)
        user.save(using =self._db)
        return user
    def create_superuser(self,email,username,first_name,last_name,phone_number,password=None ):
        user = self.create_user(
            email = self.normalize_email(email),
            username= username,
            first_name= first_name,
            last_name= last_name,
            phone_number= phone_number,
            password=password

        )

        user.is_admin=True
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user

class UserReg(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=6, verbose_name='enter username')
    first_name = models.CharField(verbose_name='enter your first name', null= False, max_length=100)
    last_name = models.CharField(verbose_name='enter your last name', null= False, max_length=100)
    phone_number = models.CharField(verbose_name='enter valid phone number', null= False, max_length=100)
    email = models.EmailField(verbose_name='enter your email', null=False, unique=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username','first_name','last_name','phone_number']

    objects = UserRegManager()
   
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)


    def __str__(self):
        return self.first_name + '' + self.last_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Topic(models.Model):
    CH = (
        ('True story','True Story'),
        ('Romance','Romance'),
        ('Short Story','Short Story'),
        ('Childrens story','Childrens story'),
        ('Fantasy','Fantasy'),
        ('Horror','Horror')
    )
    name = models.CharField(max_length= 200, verbose_name= 'topic', choices=CH)

    def __str__(self):
        return self.name

class Mystory(models.Model):
    host = models.ForeignKey(UserReg,  on_delete= models.CASCADE , null= True)
    CH = (
        ('True story','True Story'),
        ('Romance','Romance'),
        ('Short Story','Short Story'),
        ('Childrens story','Childrens story'),
        ('Fantasy','Fantasy'),
        ('Horror','Horror')
    )
    topic = models.CharField(max_length= 200, verbose_name= 'topic', choices=CH)
    title = models.CharField(max_length= 200)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='participants', blank= True)
    description = models.TextField(null=True, blank =True)
    body = models.TextField() 
    
    updated = models.DateTimeField(auto_now =True)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    mystory = models.ForeignKey(Mystory, on_delete= models.CASCADE)
    body = models.TextField() 
    updated = models.DateTimeField(auto_now =True)
    created = models.DateTimeField(auto_now_add = True)



    def __str__(self):
        return self.body[0:50]