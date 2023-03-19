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
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken
import secrets

from banking import scheduler
from banking.reminder import schedule_reminder

# Imported from current project
from .models import *

# Create your views here.
def index(request):
    # print(request.user.linked_accounts.all())
    linked_accounts = request.user.linked_accounts.all() if request.user.is_authenticated else None
    
    return render(request, "banking/index.html",{
        "linked_accounts": linked_accounts
    })

PASSWORD = "a" # later will update to generate a new one
EMAIL = "a@a.a"

@csrf_exempt
def register(request):
    if request.method == "POST":
        # user = register_user(request,"register")
        print("its here")
        # data = json.loads(request.body)
        # # username = data.get('username')
        # # phone_number = data.get('phoneNumber')
        # print(request.body)
        user = registration_view_flutter(request,"register")
        user1=[]
        login(request, user)
        user=user.serialize()
        token = str(generate_tokens(user))
        user1.append(user)
        user1.append(token)
        return JsonResponse([ user1], safe=False, status=200)

        # return render(request, "banking/index.html")
    else:
        return JsonResponse({'error': 'Invalid credentials'}, safe=False, status=400)

        # return render(request, "banking/register.html")

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
        
		# scheduler.start() #Attempt to sign user in
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

@csrf_exempt

def logout_view(request):
    
	logout(request)
   
    
    # return JsonResponse({'message': 'successfully logged out'}, status=200)

	return JsonResponse({'message':'successfully logged out'},status=200)
	# return HttpResponseRedirect(reverse("index"))

def family_member(request):
    if request.method == "POST":
        # user = register_user(request,"family")
        user = registration_view_flutter(request,"family")

        return HttpResponseRedirect(reverse("family"))
    else:
        loggedInUser = User.objects.get(pk = request.user.id)
        
        return render(request, "banking/family.html",{
            "Privilege": loggedInUser.privilege
        })

@csrf_exempt
def pay_bills(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print("its here")
        billAmount = data.get("bill_amount")
        billType = data.get("bill_name")
        billDescription = data.get("bill_description")
        billMonthly = data.get("bill_scheduled_monthly")
        date = data.get("date")
        user = data.get("user")
        account = CreditCardDetail.objects.get(phoneNumber=user[0]['Phone'])
        print(user)
        # billAmount = request.POST["bill_amount"]
        # billType = request.POST["bill_name"]
        # billDescription = request.POST["bill_description"]
        
        # This should be implemented later
        # billMonthly = request.POST.get("bill_scheduled_monthly")
        # print(billScheduled) billScheduled is "Yes" from the value I set.
        # billMonthly = True if request.POST.get("bill_scheduled_monthly") else False
        billMonthly = True if data.get("bill_scheduled_monthly") else False

        
        bill = Bill.objects.create(
            accountNumBill=account,
            # accountNumBill=request.user.account,
            billType=billType,
            billDescription=billDescription,
            billAmount=billAmount,
            billMonthly=billMonthly,
            date=date
        )
        bill.save()
        stat=str(billType+", "+billDescription+", "+billAmount+". ")
        Statement=statement.objects.create(
            userId=int(user[0]['UserId']),
            statements=stat
        )
        Statement.save()
        print(billAmount)
        return JsonResponse({'message': 'bill added successfully'}, safe=False, status=200)
        # return HttpResponseRedirect(reverse("index"))

    else:
        return JsonResponse({"bills":BILLS,
        "max_amount": CreditCardDetail.objects.get(phoneNumber=json.loads(request.body).get("user")[0]['Phone']).balance}, safe=False, status=400)

        # return render(request, "banking/pay_bills.html",{
        # "bills":BILLS,
        # "max_amount": request.user.linked_accounts.all()[0].balance
        # })

@csrf_exempt
def add_debits(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print("its here")
        DebitAmount = data.get("debit_amount")
        DebitName = data.get("debit_name")
        DebitInstallmentMonthly = data.get("debit_installment")
        DebitFinalDate = data.get("debit_final_date")
        user = data.get("user")
        account = CreditCardDetail.objects.get(phoneNumber=user[0]['Phone'])
        print(user)
       
        billMonthly = True if data.get("bill_scheduled_monthly") else False

        
        debit = Debit.objects.create(
            accountNumDebit=account,
            DebitName=DebitName,
            DebitFinalDate=DebitFinalDate,
            DebitAmount=DebitAmount,
            DebitInstallmentMonthly=DebitInstallmentMonthly
            
        )
        debit.save()
        stat=DebitName+", "+DebitAmount+". "
        Statement=statement.objects.create(userId=user[0]['UserId'],statements=stat)
        Statement.save()
        schedule_reminder(user_id=user[0]['UserId'], reminder_text="Take out the trash")

        print(DebitAmount)
        return JsonResponse({'message': 'debit added successfully'}, safe=False, status=200)

    else:
        return JsonResponse({'error': 'couldn not process your request'}, safe=False, status=400)

# API
# @login_required
def credit_card_details(request):
    ccds = CreditCardDetail.objects.all()
    if request.method == "GET":
        return JsonResponse([ccd.serialize() for ccd in ccds], safe=False)

@csrf_exempt
def login_view_flutter(request):
    if request.method == 'POST':
        # scheduler.start()
        data = json.loads(request.body)
        print(data)
        username = data.get('username')
        password = data.get('password')
        # print(username)
        # print(password)
        user = authenticate(request, username=username, password=password)
        
        user1=[]
        if user is not None:
            login(request, user)
            user=user.serialize()
            print(user["Privilege"])
            token = str(generate_tokens(user))
            user1.append(user)
            user1.append(token)
            # return JsonResponse({'message': 'success'} , status=200)
            # return JsonResponse({'token': token}, status=200) #,{'token': token} ,[ user.serialize()]
            return JsonResponse([ user1], safe=False, status=200)

        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)

@csrf_exempt
def registration_view_flutter(request,called_from):
    # if request.method == 'POST':
        data = json.loads(request.body)
        print("called view")
        # print(request.body)
        username = data.get('username')
        phone_number = data.get('phonenumber')
        dateOfBirth = data.get('dateofbirth')
        # privilege = "Main"
        privilege = data.get('privilege')
        print(phone_number)
        if called_from == "register":
            account = CreditCardDetail.objects.get(phoneNumber=phone_number)
    
        elif called_from == "family":
            print(request.user.account.phoneNumber)
            account = CreditCardDetail.objects.get(phoneNumber = request.user.account.phoneNumber)
        else:
            pass

        try:
            # Attempt to create new user
            user = User.objects.create_user(
                username, 
                EMAIL, 
                PASSWORD,
                account = account,
                dateOfBirth = dateOfBirth,
                privilege = privilege
                )
            user.save()
        except IntegrityError:
            """
            Handle possible error here, like:
                Username already taken
            """    
            # return render(request, "hotel/register.html", {
            #     "message": "Username already taken."
            # }) 
        return user


        # if user is not None:
        #     login(request, user)
        #     token = str(generate_tokens(user))
        #     return JsonResponse({'token': token}, status=500)
        # else:
        #     return JsonResponse({'error': 'Invalid credentials'}, status=400)

def statement(request):

    data = json.loads(request.body)
    user=data.get('user')
    if user[0]['Privilege'] == "Main":
        statement = statement.objects.filter(userId=user[0]['UserId'])
        return JsonResponse({'message': str(statement)}, safe=False, status=200)

    else:
        bills = Bill.objects.filter(billUser=request.user)

    return JsonResponse({'error': 'Invalid credentials'}, status=400)
def bday_voucher(request):
    pass