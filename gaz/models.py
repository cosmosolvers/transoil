from django.db import models
from uuid import uuid4

from django.contrib.auth.models import AbstractUser


class BaseModel(models.Model):
    id = models.CharField(max_length=128, primary_key=True, editable=False, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class Location(BaseModel):
    lng = models.DecimalField(max_digits=8 ,decimal_places=2, default=0)
    lat = models.DecimalField(max_digits=8 ,decimal_places=2, default=0)
    street = models.CharField(max_length=16)

    def save(self):
        return str(self.street) + str(self.longitude) + str(self.latitude)
    
    class Meta:
        db_table = 'Location'
        ordering = ['-created_at']
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'



class User(BaseModel, AbstractUser):
    ROLE_CHOICE = (
        ("Admin","Admin"),
        ("client", "Client"),
        ("saleman", "Saleman")
    )

    username = models.CharField(max_length=32, unique=True)
    first_name = models.CharField(max_length=128, blank=True, null=True)
    last_name = models.CharField(max_length=128, blank=True, null=True)

    password = models.CharField(max_length=128)
    phone_number1 = models.CharField(max_length=32)
    phone_number2 = models.CharField(max_length=32)
    
    role = models.CharField(max_length=16, choices=ROLE_CHOICE, default='client')
    location = models.OneToOneField(Location, on_delete=models.PROTECT, related_name='user_location', blank=True, null=True)
    img = models.ImageField(upload_to='user', default='nouser.png')

    class Meta:
        db_table = 'user'
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'



class Depot(BaseModel):
    STATE_CHOICE = [
        ("open", "Open"),
        ("close", "Close"),
    ]
    saleman = models.OneToOneField(User, on_delete=models.PROTECT, related_name='depot_saleman')
    state = models.CharField(max_length=8, choices=STATE_CHOICE, default='open')
    stock = models.IntegerField(default=0)

    def save(self):
        return str(self.stock)


class Gaz(BaseModel):
    TYPE_CHOICES = [
        ("Sanol", "Sanol"),
        ("Sodigaz", "Sodigaz")
    ]
    SIZE_CHOICES = [
        ("small", "Small"),
        ("middle", "Midlle"),
        ("great", "Great")
    ]
    rtype = models.CharField(max_length=128)
    weight = models.IntegerField(default=0)
    size = models.CharField(max_length=8, choices=SIZE_CHOICES)
    price = models.DecimalField(max_digits=10 ,decimal_places=2, default=0)
    img = models.ImageField(upload_to='gaz/', blank=True, null=True)

    def save(self):
        str(self.type) + str(self.size) + str(self.price)
    
    class Meta:
        db_table = 'gaz'
        ordering = ['-created_at']
        verbose_name = 'Gaz'
        verbose_name_plural = 'Gazs'



class Qte(BaseModel):
    depot = models.ForeignKey(Depot, on_delete=models.PROTECT, related_name='qte_depot')
    quantity = models.IntegerField(default=0)
    gaz = models.ForeignKey(Gaz, on_delete=models.PROTECT, related_name='qte_gaz')

    def save(self):
        return str(self.qte)

    class Meta:
        db_table = 'qte'
        ordering = ['-created_at']
        verbose_name = 'Qte'
        verbose_name_plural = 'Qtes'



class Recharge(BaseModel):
    STATE_CHOICE = [
        ("complet", "Complet"),
        ("partial", "Partial")
    ]
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='recharge_user')
    gaz = models.ForeignKey(Gaz, on_delete=models.PROTECT, related_name='recharge_gaz')
    count = models.IntegerField(default=0)
    state = models.CharField(max_length=8, choices=STATE_CHOICE)
    amount = models.DecimalField(max_digits=10 ,decimal_places=2, default=0)

    def save(self):
        return str(self.user.username) + str(self.gaz) + str(self.amount)
    
    class Meta:
        db_table = 'recharge'
        ordering = ['-created_at']
        verbose_name = 'Recharge'
        verbose_name_plural = 'Recharges'




class Transaction(BaseModel):
    STATUS= (
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("canceled", "Canceled")
    )
    
    type = models.CharField(max_length=128)
    recharge = models.OneToOneField(Recharge, on_delete=models.PROTECT, related_name='transaction_recharge')
    phone = models.CharField(max_length=150)
    fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    commission = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    distance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=16, choices=STATUS, default='pending')

    def save(self):
        return str(self.type) + str(self.total_amount)
    
    class Meta:
        db_table = 'Transaction'
        ordering = ['-created_at']
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'


class Notification(BaseModel):
    
    STATUS = (
        ("read", "Read"),
        ("unread", "Unread"),
        ("marked", "Marked")
    )
    
    title = models.CharField(max_length=32)
    subject = models.CharField(max_length=32)
    status = models.BooleanField(max_length=8, choices=STATUS, default='unread')
    message = models.TextField(max_length=1000)

    def sav(self):
        return str(self.transaction) + str(self.status)

    class Meta:
        db_table = 'Notification'
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
