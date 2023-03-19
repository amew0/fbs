import json
from tokenize import generate_tokens
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import secrets

# Imported from current project
from .models import *

# Create your views here.
def index(request):
    # print(request.user.linked_accounts.all())
    
    linked_accounts = None if request.user is None else request.user.linked_accounts.all()
    
    return render(request, "banking/index.html",{
        "linked_accounts": linked_accounts
    })

PASSWORD = "a" # later will update to generate a new one
EMAIL = "a@a.a"

def register(request):
    if request.method == "POST":
        user = register_user(request,"register")
        
        login(request, user)
        return render(request, "banking/index.html")
    else:
        return render(request, "banking/register.html")

def register_user(request,called_from):
    username = request.POST["username"]
    # fullname = request.POST["fullname"]
    phone_number = request.POST["phoneNumber"]
    dateOfBirth = request.POST["dateOfBirth"]
    privilege = request.POST.get("privilege")
    
    if called_from == "register":
        account = CreditCardDetail.objects.get(phoneNumber=phone_number)
    elif called_from == "family":
        account = CreditCardDetail.objects.get(phoneNumber = request.user.account.phoneNumber)

    user = None
    try:
        # Attempt to create new user
        user = User.objects.create_user(username, EMAIL, PASSWORD, account = account,
            dateOfBirth = dateOfBirth,
            privilege = privilege
            )
        user.save()

    except IntegrityError:
        """
        Handle possible error here, like:
            Username already taken
        """    
        return render(request, "banking/register.html", {
            "message": "Username already taken."
        })


    if privilege == "Main":
        
        # User is 'Main' and hence should be linked to the bank account
        account.linked_users.add(user)
        account.save()

    elif privilege == "Sub":
        allowance_account = Allowance.objects.create(
            userMain = request.user,
            userSub = user,
            allowance = 0.00
        )
        allowance_account.save()

    return user

def login_view(request):
	if request.method == "POST":

		# Attempt to sign user in
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)

		# Check if authentication successful
		if user is not None:
			login(request, user)
			return render(request, "banking/index.html")
		else:
			return render(request, "banking/login.html", {
				"message": "Invalid username and/or password."
			})
	else:
		return render(request, "banking/login.html")

def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse("index"))

def family_member(request):
    if request.method == "POST":
        user = register_user(request,"family")
        return HttpResponseRedirect(reverse("family"))
    else:
        loggedInUser = User.objects.get(pk = request.user.id)
        
        return render(request, "banking/family.html",{
            "Privilege": loggedInUser.privilege
        })

def pay_bills(request):
    if request.method == "POST":
        billAmount = request.POST["bill_amount"]
        billType = request.POST["bill_name"]
        billDescription = request.POST["bill_description"]
        
        # This should be implemented later
        billMonthly = request.POST.get("bill_scheduled_monthly")
        # print(billScheduled) billScheduled is "Yes" from the value I set.
        billMonthly = True if request.POST.get("bill_scheduled_monthly") else False

        bill = Bill.objects.create(
            accountNumBill=request.user.account,
            billType=billType,
            billDescription=billDescription,
            billAmount=billAmount,
            billMonthly=billMonthly
        )
        bill.save()
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "banking/pay_bills.html",{
            "bills":BILLS,
            "max_amount": request.user.linked_accounts.all()[0].balance
        })

def add_debits(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "banking/add_debits.html")


# API
# @login_required
def credit_card_details(request):
    ccds = CreditCardDetail.objects.all()
    if request.method == "GET":
        return JsonResponse([ccd.serialize() for ccd in ccds], safe=False)
@csrf_exempt
def login_view_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        print(username)
        print(password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token = generate_tokens(user)
            return JsonResponse({'token': token})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)