#accounts.model.py

from django.db import models
from django.contrib.auth.models import(
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and save a User with the given email and password
        """
        if not email:
            raise ValueError('Users must have an email')
        
        user = self.model(
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and save a User with the given email and password
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff=True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and save a User with the given email and password
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff=True
        user.admin=True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) #admin user, bukan superuser
    admin = models.BooleanField(default=False) #superuser

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # email & password are required by default
    
    def get_full_name(self):
        # User is identified by their email address
        return self.email

    def get_short_name(self):
        # User is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a spesific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permission to view the `app_label`"
        return True
    
    @property
    def is_staff(self):
        return self.staff
    
    @property
    def is_admin(self):
        return self.admin
    
    @property
    def is_active(self):
        return self.active
    
    objects = UserManager()