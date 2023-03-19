import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import firebase_admin
from firebase_admin import credentials, messaging
from django.conf import settings


# cred = credentials.Certificate(settings.FIREBASE_SERVICE_ACCOUNT_KEY)
# firebase_admin.initialize_app(cred)

# def send_reminder(user_id, reminder_text):
#     # Send the reminder push notification using OneSignal
#     sdk = OneSignalSdk(settings.ONESIGNAL_APP_ID, settings.ONESIGNAL_API_KEY)
#     notification = {
#         "contents": {"en": reminder_text},
#         "include_external_user_ids": [str(user_id)],
#     }
#     response = sdk.create_notification(notification)
#     print(response)

# def schedule_reminder(user_id, reminder_text, schedule):
#     # Create a scheduler instance
#     scheduler = BackgroundScheduler()

#     # Define the job that will run the reminder function
#     trigger_time = datetime.combine(schedule)
#     scheduler.add_job(
#         send_reminder,
#         trigger=CronTrigger(hour=22, minute=0, second=0, start_date=trigger_time),
#         args=[user_id, f'Reminder': reminder_text],
#         id=f'reminder-{user_id}'
#     )

#     # Start the scheduler
#     scheduler.start()



def send_reminder(user_id, reminder_text):
    # Send the reminder to the user, e.g. using email or push notification
    print(f"Sending reminder to user {user_id}: {reminder_text}")
def schedule_reminder(user_id, reminder_text):
    # Create a scheduler instance
    scheduler = BackgroundScheduler()

    # Define the job that will run the reminder function
    scheduler.add_job(
        send_reminder,
        trigger=CronTrigger(hour=22, minute=14, second=0),
        args=[user_id, reminder_text],
        id=f'reminder-{user_id}'
    )

    # Start the scheduler
    scheduler.start()
