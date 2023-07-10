import pandas as pd
import datetime
import smtplib
from email.message import EmailMessage


def send_contract_end_reminders(property_data, user_data, one_month_from_now, sender_email, sender_password):
    for index, row in property_data.iterrows():
        users = row['Users']
        matching_users = user_data[user_data['Users'] == users]
        if matching_users.empty:
            continue

        email = matching_users.iloc[0]['Email']
        electricity_contract_end_date = row['Electricity contract end date'].date()
        gas_contract_end_date = row['Gas contract end date'].date()
        broadband_contract_end_date = row['Broadband contract end date'].date()
        home_insurance_contract_end_date = row['Home Insurance contranct end date'].date()
        waste_contract_end_date = row['Waste contract end date'].date()
        homesecure_contract_end_date = row['Homesecure contract end date'].date()

        if (
                electricity_contract_end_date <= one_month_from_now or
                gas_contract_end_date <= one_month_from_now or
                broadband_contract_end_date <= one_month_from_now or
                home_insurance_contract_end_date <= one_month_from_now or
                waste_contract_end_date <= one_month_from_now or
                homesecure_contract_end_date <= one_month_from_now
        ):
            # Send email to the user
            message = EmailMessage()
            message["From"] = sender_email
            message["To"] = email
            message["Subject"] = "Reminder: Contract End Date Approaching"

            body = f"Dear User,\n\nThis is a reminder that one or more of your contracts is approaching the end date. Please take the necessary actions.\n\nRegards,\nYour Company"

            message.set_content(body)

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(message)

            print(f"Email sent successfully to User: {users} ({email})")


def send_due_date_reminders(vehicle_data, user_data, one_month_from_now, three_months_from_now, sender_email, sender_password):
    for index, row in vehicle_data.iterrows():
        users = row['Users']
        matching_users = user_data[user_data['Users'] == users]
        if matching_users.empty:
            continue
        email = matching_users.iloc[0]['Email']
        nct_due_date = row['NCT due date'].date()
        insurance_due_date = row['Insurance due date'].date()
        road_tax_due_date = row['Road Tax due date'].date()
        services_due_date = row['Services due date'].date()

        if (
                nct_due_date <= three_months_from_now or
                insurance_due_date <= one_month_from_now or
                road_tax_due_date <= one_month_from_now or
                services_due_date <= three_months_from_now
        ):
            # Send email to the user
            message = EmailMessage()
            message["From"] = sender_email
            message["To"] = email
            message["Subject"] = "Reminder: Due Date Approaching"

            body = f"Dear User,\n\nThis is a reminder that one or more of your due dates is approaching. Please take the necessary actions.\n\nRegards,\nLiving Assistant"

            message.set_content(body)

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(message)

            print(f"Email sent successfully to User: {users} ({email})")


# Read the user information from the "User info" sheet
## Read in the Data from MongoDB - User Info; Using excel file show examples here.

# Read the property information from the "Asset - Property" sheet
## Read in the Data from MongoDB - Asset - Property

# Read the vehicle information from the "Asset - Vehicle" sheet
## Read in the Data from MongoDB - Asset - Vehicles

# Get the current system date
current_date = datetime.date.today()

# Calculate the date one month from now
one_month_from_now = current_date + datetime.timedelta(days=30)

# Calculate the date three months from now
three_months_from_now = current_date + datetime.timedelta(days=91)

# Provide your email credentials
sender_email = "xxxx"
sender_password = "xxxx"

# Call the function to send contract end reminders
send_contract_end_reminders(property_data, user_data, one_month_from_now, sender_email, sender_password)

# Call the function to send due date reminders
send_due_date_reminders(vehicle_data, user_data, one_month_from_now, three_months_from_now, sender_email, sender_password)

