from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    pass

class Customer(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    amount_due_at = models.DateTimeField()

    def __str__(self):
        return self.name
    
class Task(models.Model):
    collector = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer.name}'s Task"
    
class Transaction(models.Model):
    collector = models.ForeignKey(User, related_name='collected_transactions', on_delete=models.CASCADE)
    manager = models.ForeignKey(User, related_name='received_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.collector.username} -> {self.manager.username}: ${self.amount}"

class FrozenCollector(models.Model):
    collector = models.OneToOneField(User, on_delete=models.CASCADE)
    frozen_since = models.DateTimeField()

    def __str__(self):
        return self.collector.username

class ManagerLog(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.manager.username}: {self.action}"
