from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager

# class UserManager(BaseUserManager):
#     def create_user(self, email,first_name,last_name,phone, password=None,password2=None):
#         if not email:
#             raise ValueError('Users must have an email address')
#         user = self.model(
#             email=self.normalize_email(email),
#             first_name=first_name,
#             last_name=last_name,
#             phone=phone
#         )
#         user.set_password(password)

    
#     def create_superuser(self, email,first_name,last_name,phone, password=None):
#         user = self.model(
#             email=self.normalize_email(email),
#             first_name=first_name,
#             last_name=last_name,
#             phone=phone
#         )
#         user.is_staff = True
#         user.is_superuser = True
#         user.set_password(password)

        

class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True,null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField()
    
    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.username 
    
class device_detail(models.Model):
    report_by = models.ForeignKey(User,on_delete=models.CASCADE)
    model = models.CharField(max_length=50)
    imei1 = models.BigIntegerField(unique=True)
    imei2 = models.BigIntegerField(unique=True)
    missing_date = models.DateField(auto_now=True)
    description = models.CharField(null=True)
    class Meta:
        ordering = ['id']
        unique_together = ['imei1','imei2']
        
    def __str__(self):
        return f"{self.report_by.username} {self.model}"

class search_record(models.Model):
    search_device = models.ForeignKey(device_detail,on_delete=models.CASCADE,related_name='missing_device')
    search_date = models.DateField(auto_now=True)
    search_user = models.ForeignKey(User,blank=True,on_delete=models.CASCADE,related_name='searcheing_user')
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return f"{self.serech_device.model} {self.search_date}"
