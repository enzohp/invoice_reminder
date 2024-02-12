# invoice_reminder
Automatic reminder for unpaid invoices 7 days after due date has passed. Note that crons in Odoo are called Scheduled Actions.

Author: Enzo Hp

The first file, cron_invoice_reminder.xml, defines a scheduled job (cron job) for sending invoice reminders. The second file, invoice_reminder_email_template.xml, describes the email template used for these reminders.

File: cron_invoice_reminder.xml
Overview:
This XML file defines a cron job in Odoo that is responsible for sending reminders for unpaid or partially paid invoices. It is scheduled to run daily by default but can be changed by going to the Settings module with Developer mode on, clicking on Technical > Scheduled Actions and searching for "Invoice Reminder".

Structure:
Root Element: <odoo> is the root element that encapsulates the data.
Data Element: <data noupdate="1"> signifies that the records within this block should not be updated automatically during module updates.
Cron Job Record:
ID: cron_invoice_reminder uniquely identifies this cron job.
name: Name of the cron job ("Invoice Reminder").
model_id: Links to the account.move model, indicating that the cron job is related to accounting moves (invoices).
state: Set to code, indicating that the action to be executed is in code form.
code: Contains the Python code executed by the cron job. This code calculates the date 7 days ago, filters invoices that are due, unpaid or partially paid, and then sends reminder emails using a specified template.
active: Indicates that the cron job is active.
interval_number, interval_type: Schedules the cron job to run every 1 day.
numbercall: -1 implies that the job should run indefinitely.
doall: Set to False, meaning the job won't run for past missed times if the server was down.

Python Code Analysis:


Calculate Date 7 Days Ago:
seven_days_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).date()
This line computes the date that is seven days prior to the current date. It uses the datetime module, subtracts 7 days from the current date and time (datetime.datetime.now()), and then converts the result into a date object.

Filter Invoices:
pending_invoices = env["account.move"].search([
    "&", "&", 
    ("move_type", "=", "out_invoice"), 
    ("payment_state", "in", ["partial", "not_paid"]), 
    ("invoice_date_due", "<", seven_days_ago)])
This segment filters and retrieves invoices that meet specific criteria:
1)move_type = "out_invoice": Selects customer invoices (excluding vendor bills).
2)payment_state in ["partial", "not_paid"]: Filters invoices that are either partially paid or not paid at all.
3)invoice_date_due < seven_days_ago: Ensures that only invoices with a due date earlier than seven days ago are selected.


Email Template Lookup and Sending Emails:
template = env.ref('invoice_reminder.invoice_reminder_email_template', raise_if_not_found=False)
if template:
    for pending_invoice in pending_invoices:
        template.send_mail(pending_invoice.id, force_send=False, raise_exception=False)
The script then looks up an email template (identified by 'invoice_reminder.invoice_reminder_email_template') within the Odoo system.
If the template is found (if template:), the script iterates over each of the filtered invoices (for pending_invoice in pending_invoices:).
For each invoice, it sends an email using the identified template. The send_mail function is called with the ID of the invoice, with parameters force_send and raise_exception set to False. These settings mean that the email sending will be queued (not forced immediately) and exceptions during email sending won't raise errors (which is useful for avoiding interruption of the cron job due to email sending issues).

File: invoice_reminder_email_template.xml
Overview
This file defines the email template used by the aforementioned cron job to send payment reminders to customers with outstanding invoices and can be edited by going to the Settings module with Developer mode on, clicking on Technical > Email Templates and searching for "Payment Reminder".

Structure:
Root Element: <odoo> as the root.
Data Element: <data> without the noupdate attribute, implying these records can be updated.
Email Template Record:
ID: invoice_reminder_email_template for identification.
Model: mail.template indicates that this is an email template.
Fields:
name: The name of the template ("Payment Reminder").
model_id: Refers to the account.move model, tying the template to invoices.
subject: The subject line of the email.
email_from: Email sender address, dynamically set to the email of the user responsible for the invoice, with a fallback to 'noreply@example.com'.
body_html: The HTML content of the email, which includes dynamic content like customer name, outstanding balance, and a link to view the invoice.
lang: Language of the template, dynamically set based on the recipient's language.
auto_delete: Set to False, meaning the email won't be automatically deleted after sending.
Integration
These files work together within an Odoo environment. The cron job regularly triggers the email sending process using the defined template, thus automating the process of reminding customers about their outstanding invoices.

For effective use, ensure that these XML files are correctly placed in your Odoo addons's directory and that the invoice_reminder module is properly installed in your Odoo instance. Additionally, feel free to duplicate and adjust the Python code and email template according to your business logic and branding requirements through the instructions provided in the Overview of each file.





