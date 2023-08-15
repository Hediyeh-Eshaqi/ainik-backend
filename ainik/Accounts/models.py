from django.db import models
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.conf import settings
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password
        )
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    avatar = models.ImageField(null=True, default=None, blank=True,)
    firstName = models.CharField(max_length=30, null=True, default=None, blank=True,)
    lastName = models.CharField(max_length=30, null=True, default=None, blank=True,)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin



'''
this class will store the user personality components
that includes 8 questions of user personality. each of
them has a value from range [1,2,3,4] means that user
clicked which choice
'''    
class PersonalityComponent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gender = models.BooleanField()
    age = models.IntegerField()
    q1 = models.IntegerField()
    q2 = models.IntegerField()
    q3 = models.IntegerField()
    q4 = models.IntegerField()
    q5 = models.IntegerField()
    q6 = models.IntegerField()
    q7 = models.IntegerField()
    q8 = models.IntegerField()
      
    
    