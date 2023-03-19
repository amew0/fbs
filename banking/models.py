from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField


# Create your models here.
# These are all the tables on the database
class CreditCardDetail(models.Model):
    accountNumber = models.CharField(
        max_length = 19) # XXXX-XXXX-XXXX-XXXX
    phoneNumber = models.CharField(
        max_length=15)   # +971 5 XXX-XXXX
    linked_users = models.ManyToManyField(
            'User',
            related_name = "linked_accounts",
            blank=True
        )
    balance = models.DecimalField(
        max_digits = 10, 
        decimal_places = 2,
        default=0.00)
    def __str__(self):
        return f"{self.accountNumber} (AED {self.balance})"
    
    def serialize(self):
        return {
            "id" : self.id,
            "accountNumber" : self.accountNumber,
            "phoneNumber" : self.phoneNumber,
            "balance" : self.balance,
            "linked_users" : [
                linked_user.serialize() for linked_user in self.linked_users.all()
            ],

        }

PRIVILEGES = [
	('Main', 'Main'),
	('Sub', 'Sub')
]
class User (AbstractUser):
    account = models.ForeignKey(
            CreditCardDetail,
            on_delete = models.SET_NULL, 
            null=True, 
            related_name = "numberU"
        )
    dateOfBirth = models.DateField(null=True)
    privilege = models.TextField(choices = PRIVILEGES,null=True)
    def __str__(self):
        return f"{self.username} ({self.privilege})"
    def serialize(self):
        return {
            "UserId" : self.id,
            "AccountId" : self.account.id,
            "Username" : self.username,
            "Date of birth" : self.dateOfBirth,
            "Privilege" : self.privilege,
            "Balance"  : self.account.balance,
            "Account"  : self.account.accountNumber,
            "Phone"  : self.account.phoneNumber,
            "Linked"  : str(self.account.linked_users)

        }
    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        dateOfBirth = extra_fields.pop('dateOfBirth', None)
        privilege = extra_fields.pop('privilege', None)
        """
        if phoneNumber is not None and phoneNumber (condition):
            raise ValueError('Phone number must be sth')
        """
        user = super().create_user(username=username,email=email,passowrd=password,**extra_fields)
        user.dateOfBirth = dateOfBirth
        user.privilege = privilege

        user.save(using=self._db)
        return user

class Allowance (models.Model):
    userMain = models.ForeignKey(
        User, 
        on_delete = models.SET_NULL, 
        null=True, 
        related_name = "userMain")
    userSub = models.ForeignKey(
        User, 
        on_delete = models.SET_NULL, 
        null=True, 
        related_name = "userSub")
    allowance = models.DecimalField(
        max_digits = 10, 
        decimal_places = 2,
        default=0.0)
    
    # def __str__(self):
    #     return f"{self.userSub: (AED {self.allowance})}"

BILLS = (
    ('rent', 'Rent or mortgage payment'),
    ('electricity', 'Electricity bill'),
    ('gas', 'Gas bill'),
    ('water', 'Water bill'),
    ('internet', 'Internet bill'),
    ('cable', 'Cable or satellite TV bill'),
    ('phone', 'Phone bill'),
    ('car_payment', 'Car payment (if applicable)'),
    ('car_insurance', 'Car insurance'),
    ('health_insurance', 'Health insurance'),
    ('life_insurance', 'Life insurance'),
    ('home_insurance', 'Homeowners or renters insurance'),
    ('property_tax', 'Property tax (if you own a home)'),
    ('credit_card', 'Credit card bills'),
    ('student_loan', 'Student loan payments (if applicable)'),
    ('childcare', 'Childcare expenses'),
    ('groceries', 'Groceries'),
    ('clothing', 'Clothing expenses'),
    ('entertainment', 'Entertainment expenses'),
    ('medical', 'Medical expenses (co-pays, prescriptions, etc.)'),
    ('other','Other'),
)
class Bill (models.Model):
    
    accountNumBill = models.ForeignKey(
        CreditCardDetail,
        on_delete = models.SET_NULL, 
        null=True, 
        related_name = "accountNumBill")
    billUser = models.ForeignKey(
        User,
        on_delete = models.SET_NULL, 
        null=True, 
        related_name = "billUser"
    )
    billType = models.CharField(
        max_length = 25,
        choices=BILLS)
    billDescription = models.TextField(
        blank=True,
        null=True
    )
    billAmount = models.DecimalField(
        max_digits = 10, 
        decimal_places = 2,
        default=0.00
    )
    billMonthly = models.BooleanField(
        default=False
    )
    date = models.DateField(null=True)
    
    def __str__(self):
        return f"{self.billType} (AED{self.billAmount})"
    


class Debit (models.Model):
    
    accountNumDebit = models.ForeignKey(
        CreditCardDetail,
        on_delete = models.SET_NULL, 
        null=True, 
        related_name = "accountNumDebit")
    DebitName = models.CharField(
        max_length = 25,
        )
    DebitFinalDate = models.TextField(
        blank=True,
        null=True
    )
    DebitAmount = models.DecimalField(
        max_digits = 10, 
        decimal_places = 2,
        default=0.00
    )
    DebitInstallmentMonthly = models.DecimalField(
        max_digits = 10, 
        decimal_places = 2,
        default=0.00
    )
    
    def __str__(self):
        return f"{self.DebitName} (AED{self.DebitAmount})"

class statement (models.Model):
    userId=models.IntegerField(
        
    )
    statements=models.TextField(
        blank=True
    )
    def __str__(self):
        return f"{self.userId}"