from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class User(AbstractUser):
    phone_number = PhoneNumberField()


class UIManager(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    text_description = models.TextField(max_length=200)
    UI_position = models.IntegerField(null=False, blank=False)


class MainTables(models.Model):
    table_id = models.AutoField(primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(default=timezone.now)
    carat_range = models.TextField(max_length=25)
    tabel_date = models.DateField()
    shape = models.TextField(max_length=25)
    text_description = models.TextField(max_length=200)

    def __str__(self):
        return self.carat_range + " - " + self.shape

class DataManager(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(default=timezone.now)
    parent_table = models.ForeignKey(MainTables, on_delete=models.CASCADE)
    D_IF  = models.DecimalField(max_digits=5, decimal_places=0)
    D_VV1 = models.DecimalField(max_digits=5, decimal_places=0)
    D_VV2 = models.DecimalField(max_digits=5, decimal_places=0)
    D_VS1 = models.DecimalField(max_digits=5, decimal_places=0)
    D_VS2 = models.IntegerField(null=False, blank=False)
    D_SI1 = models.IntegerField(null=False, blank=False)
    D_SI2 = models.IntegerField(null=False, blank=False)

    E_IF  = models.IntegerField(null=False, blank=False)
    E_VV1 = models.IntegerField(null=False, blank=False)
    E_VV2 = models.IntegerField(null=False, blank=False)
    E_VS1 = models.IntegerField(null=False, blank=False)
    E_VS2 = models.IntegerField(null=False, blank=False)
    E_SI1 = models.IntegerField(null=False, blank=False)
    E_SI2 = models.IntegerField(null=False, blank=False)

    F_IF  = models.IntegerField(null=False, blank=False)
    F_VV1 = models.IntegerField(null=False, blank=False)
    F_VV2 = models.IntegerField(null=False, blank=False)
    F_VS1 = models.IntegerField(null=False, blank=False)
    F_VS2 = models.IntegerField(null=False, blank=False)
    F_SI1 = models.IntegerField(null=False, blank=False)
    F_SI2 = models.IntegerField(null=False, blank=False)

    G_IF  = models.IntegerField(null=False, blank=False)
    G_VV1 = models.IntegerField(null=False, blank=False)
    G_VV2 = models.IntegerField(null=False, blank=False)
    G_VS1 = models.IntegerField(null=False, blank=False)
    G_VS2 = models.IntegerField(null=False, blank=False)
    G_SI1 = models.IntegerField(null=False, blank=False)
    G_SI2 = models.IntegerField(null=False, blank=False)

    H_IF  = models.IntegerField(null=False, blank=False)
    H_VV1 = models.IntegerField(null=False, blank=False)
    H_VV2 = models.IntegerField(null=False, blank=False)
    H_VS1 = models.IntegerField(null=False, blank=False)
    H_VS2 = models.IntegerField(null=False, blank=False)
    H_SI1 = models.IntegerField(null=False, blank=False)
    H_SI2 = models.IntegerField(null=False, blank=False)

    I_IF  = models.IntegerField(null=False, blank=False)
    I_VV1 = models.IntegerField(null=False, blank=False)
    I_VV2 = models.IntegerField(null=False, blank=False)
    I_VS1 = models.IntegerField(null=False, blank=False)
    I_VS2 = models.IntegerField(null=False, blank=False)
    I_SI1 = models.IntegerField(null=False, blank=False)
    I_SI2 = models.IntegerField(null=False, blank=False)

    J_IF  = models.IntegerField(null=False, blank=False)
    J_VV1 = models.IntegerField(null=False, blank=False)
    J_VV2 = models.IntegerField(null=False, blank=False)
    J_VS1 = models.IntegerField(null=False, blank=False)
    J_VS2 = models.IntegerField(null=False, blank=False)
    J_SI1 = models.IntegerField(null=False, blank=False)
    J_SI2 = models.IntegerField(null=False, blank=False)

    increased = models.TextField(max_length=500,null=False, blank=False)
    dropped = models.TextField(max_length=500,null=False, blank=False)

    current_percentage_change = models.DecimalField(max_digits=6, decimal_places=2,null=True, blank=False)
    last_percentage_change = models.DecimalField(max_digits=6, decimal_places=2,null=True, blank=False)
    second_last_percentage_change = models.DecimalField(max_digits=6, decimal_places=2,null=True, blank=False)
    postion = models.IntegerField()



