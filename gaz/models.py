from django.db import models

class User(models.Model):
    ROLE_CHOICE = [
        ("Admin","Admin"),
    ]
    firstname = models.CharField(max_length=150, verbose_name="Nom")
    lastname = models.CharField(max_length=150, verbose_name="Prénom")
    username = models.CharField(max_length=150, verbose_name="Nom d'Utilisateur")
    phone_number1 = models.CharField(max_length=150, verbose_name="Numéro de téléphone 1")
    phone_number2 = models.CharField(max_length=150, verbose_name="Numéro de téléphone 2")
    role = models.CharField(max_length=50 ,choices=ROLE_CHOICE, verbose_name="Rôle")
    location = models.OneToOneField(Location, on_delete=models.CASCADE, verbose_name="Location")
    depot = models.OneToOneField(Depot, on_delete=models.CASCADE, verbose_name="Dépôt")

    def save(self):
        return str(self.username)
    

class Depot(models.Model):
    STATE_CHOICE = [
        ("Ouvert", "Ouvert"),
        ("Fermé", "Fermé"),
    ]
    sellsman = models.ForeignKey(Sellsman, on_delete=models.CASCADE, verbose_name="Vendeur")
    state = models.CharField(choices=STATE_CHOICE, verbose_name="Status")
    stock = models.IntegerField(default=0, verbose_name="Stock")
    
    def save(self):
        return str(self.stock)
    
class Qte(models.Model):
    qte = models.OneToOneField(Qte, on_delete=models.CASCADE, verbose_name="Quantité")
    depot = models.ForeignKey(Depot, on_delete=models.CASCADE, verbose_name="Dépôt")
    stock_gaz = models.IntegerField(default=0, verbose_name="Stock")

    def save(self):
        return str(self.qte)
    
class Gaz(models.Model):
    TYPE_CHOICES = [
        ("Sanol", "Sanol"),
        ("Sodigaz", "Sodigaz")
    ]
    SIZE_CHOICES = [
        ("Petit", "Petit"),
        ("Moyen", "Moyen"),
        ("Grand", "Grand")       
    ]
    type = models.CharField(max_length="100", verbose_name="Type")
    weight = models.IntegerField(default=0, verbose_name="Poids")
    size = models.CharField(max_length="50", choices=SIZE_CHOICES, verbose_name="Taille")
    price = models.DecimalField(decimal_places=2, default=0, verbose_name="Prix")
    qte = models.OneToOneField(Qte, on_delete=models.CASCADE, verbose_name="Quantité")

    def save(self):
        str(self.type) + str(self.size) + str(self.price)

class Recharge(models.Model):
    STATE_CHOICE = [
        ("Complète", "Complète"),
        ("Partiel", "Partiel")
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, verbose_name="Utilisateur")
    gaz = models.ForeignKey(Gaz, on_delete=models.CASCADE, null=False, verbose_name="Gaz")
    count = models.IntegerField(default=0, verbose_name="Nombre")
    state = models.CharField(max_length="100", choices=STATE_CHOICE, verbose_name="Status")
    amount = models.DecimalField(decimal_places=2, default=0, verbose_name="Montant")

    def save(self):
        return str(self.user.username) + str(self.gaz) + str(self.amount)

class Sellsman(models.Model):
    firstname = models.CharField(max_length=150, verbose_name="Nom")
    lastname = models.CharField(max_length=150, verbose_name="Prénom")
    phone_number = models.CharField(max_length=150, verbose_name="Numéro de téléphone")

    def save(self):
        return str(self.firstname) + str(self.lastname)

class Location(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Utilisateur")
    longitude = models.DecimalField(decimal_places=2, default=0, verbose_name="Longitude")
    latitude = models.DecimalField(decimal_places=2, default=0, verbose_name="Latitude")
    street = models.CharField(max_length="100", verbose_name="Rue")

    def save(self):
        return str(self.street) + str(self.longitude) + str(self.latitude)

class Transaction(models.Model):
    type = models.CharField(max_length="100", verbose_name="Type")
    recharge = models.OneToOneField(Recharge, on_delete=models.CASCADE, verbose_name="Recharge")
    phone = models.CharField(max_length=150, verbose_name="Numéro de téléphone")
    fees = models.DecimalField(decimal_places=2, default=0, verbose_name="Frais")
    commission = models.DecimalField(decimal_places=2, default=0, verbose_name="Commission")
    total_amount = models.DecimalField(decimal_places=2, default=0, verbose_name="Montant total")
    distance = models.DecimalField(decimal_places=2, default=0, verbose_name="Distance")

    def save(self):
        return str(self.type) + str(self.total_amount)

class Notification(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, verbose_name="Transaction")
    title = models.CharField(max_length="100", verbose_name="Auteur")
    subject = models.CharField(max_length="100", verbose_name="Sujet")    
    status = models.BooleanField(max_length="100", default=False, verbose_name="Status")
    message = models.TextField(max_length="1000", verbose_name="Message")

    def sav(self):
        return str(self.transaction) + str(self.status)