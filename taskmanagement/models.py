from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

"""
I will use a custom manager to require email as the sole username
and ignore the original username field
"""
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **other_fields):
        if not email:
            raise ValueError("You must set the email field")
        email = self.normalize_email(email)
        other_fields.setdefault('role','User')
        other_fields.setdefault('is_active', True)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **other_fields):
        other_fields.setdefault('role','Admin')
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_superuser') is not True:
            raise ValueError("User user must have is_superuser boolean to be True")
        if other_fields.get('is_staff') is not True:
            raise ValueError("User user must have is_staff boolean to be True")
        return self.create_user(email, password, **other_fields)


"""
I will create the needed fields and call the custome manager i created
as the objects, then crete a method to check if role is admin, this
will help in my view
"""
class CustomUser(AbstractBaseUser, PermissionsMixin):

    ROLE=(
        ("Admin", "Admin"),
        ("User", "User")
    )

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=225)
    role = models.CharField(max_length=6, choices=ROLE, default="User")
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = CustomUserManager()

    def is_admin(self):
        return self.role == "Admin"
    
    def is_user(self):
        return self.role == "User"

    def __str__(self):
        return f"{self.full_name} - {self.email}"
    

class Task(models.Model):
    STATUS = (
        ('To-Do', 'To-Do'),
        ('In-Progress', 'In-Progress'),
        ('Done', 'Done')
    )

    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=False)
    status = models.CharField(max_length=15, choices=STATUS, default='To-Do')
    
    # since we are using soft delete, i dont think the task should be deleted
    # when the assigned user is deleted, so that we can still have the task record
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='task')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.status} by {self.assigned_to.full_name}"
    

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        #slicing the name to 12 character to prevent long name
        return f"Comment by {self.author.full_name:12} on {self.task.title}"
