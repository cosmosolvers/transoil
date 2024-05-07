from django.db import models


class BaseModel(models.Model):
    id = models.CharField(max_length=128, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_add_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class User(BaseModel):
    ROLE_CHOICE = (
        ("Admin","Admin"),
        ("client", "Client"),
        ("saleman", "Saleman")
    )
    
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    username = models.CharField(max_length=32)
    phone_number1 = models.CharField(max_length=32)
    phone_number2 = models.CharField(max_length=32)
    role = models.CharField(max_length=16 ,choices=ROLE_CHOICE)
    last_login = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    location = models.OneToOneField(Location, on_delete=models.PROTECT)
    depot = models.OneToOneField(Depot, on_delete=models.PROTECT, blank=True, null=True)

    def save(self):
        return str(self.username)

    class Meta:
        db_table = 'user'
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Depot(models.Model):
    STATE_CHOICE = [
        ("open", "Open"),
        ("close", "Close"),
    ]
    sellsman = models.ForeignKey(User, on_delete=models.PROTECT)
    state = models.CharField(max_length=8, choices=STATE_CHOICE)
    stock = models.IntegerField(default=0)
    
    def save(self):
        return str(self.stock)
    
class Qte(models.Model):
    depot = models.ForeignKey(Depot, on_delete=models.CASCADE)
    stock_gaz = models.IntegerField(default=0)

    def save(self):
        return str(self.qte)

    class Meta:
        db_table = 'qte'
        ordering = ['-created_at']
        verbose_name = 'Qte'
        verbose_name_plural = 'Qtes'
    
class Gaz(models.Model):
    TYPE_CHOICES = [
        ("Sanol", "Sanol"),
        ("Sodigaz", "Sodigaz")
    ]
    SIZE_CHOICES = [
        ("small", "Small"),
        ("middle", "Midlle"),
        ("great", "Great")
    ]
    type = models.CharField(max_length=128)
    weight = models.IntegerField(default=0)
    size = models.CharField(max_length=8, choices=SIZE_CHOICES)
    price = models.DecimalField(max_digits=10 ,decimal_places=2, default=0)
    qte = models.OneToOneField(Qte, on_delete=models.CASCADE)

    def save(self):
        str(self.type) + str(self.size) + str(self.price)
    
    class Meta:
        db_table = 'gaz'
        ordering = ['-created_at']
        verbose_name = 'Gaz'
        verbose_name_plural = 'Gazs'

class Recharge(models.Model):
    STATE_CHOICE = [
        ("complet", "Complet"),
        ("partial", "Partial")
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gaz = models.ForeignKey(Gaz, on_delete=models.CASCADE)
    count = models.IntegerField(default=0, verbose_name="Nombre")
    state = models.CharField(max_length=8, choices=STATE_CHOICE)
    amount = models.DecimalField(max_digits=10 ,decimal_places=2, default=0)

    def save(self):
        return str(self.user.username) + str(self.gaz) + str(self.amount)
    class Meta:
        db_table = 'recharge'
        ordering = ['-created_at']
        verbose_name = 'Recharge'
        verbose_name_plural = 'Recharges'

class Location(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    longitude = models.DecimalField(max_digits=8 ,decimal_places=2, default=0)
    latitude = models.DecimalField(max_digits=8 ,decimal_places=2, default=0)
    street = models.CharField(max_length=16)

    def save(self):
        return str(self.street) + str(self.longitude) + str(self.latitude)
    
    class Meta:
        db_table = 'Location'
        ordering = ['-created_at']
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

class Transaction(models.Model):
    type = models.CharField(max_length=128)
    recharge = models.OneToOneField(Recharge, on_delete=models.CASCADE)
    phone = models.CharField(max_length=150)
    fees = models.DecimalField(max_length = 10 ,decimal_places=2, default=0)
    commission = models.DecimalField(max_length = 10 ,decimal_places=2, default=0)
    total_amount = models.DecimalField(max_length = 10 ,decimal_places=2, default=0)
    distance = models.DecimalField(max_length = 10 ,decimal_places=2, default=0)

    def save(self):
        return str(self.type) + str(self.total_amount)
    
    class Meta:
        db_table = 'Transaction'
        ordering = ['-created_at']
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

class Notification(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE)
    title = models.CharField(max_length=32)
    subject = models.CharField(max_length=32)
    status = models.BooleanField(max_length=8, default=False)
    message = models.TextField(max_length=1000)

    def sav(self):
        return str(self.transaction) + str(self.status)

    class Meta:
        db_table = Notification
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
