# Invoice Reminder
Automatic reminder for unpaid invoices 7 days after the due date has passed. Note that crons in Odoo are called Scheduled Actions.

**Author:** Enzo Hp

## Overview
This project contains two main files:
1. `cron_invoice_reminder.xml` - Defines a scheduled job (cron job) for sending invoice reminders.
2. `invoice_reminder_email_template.xml` - Describes the email template used for these reminders.

## Files and Details

### 1. cron_invoice_reminder.xml
**Overview:** This XML file defines a cron job in Odoo, responsible for sending reminders for unpaid or partially paid invoices. It runs daily by default and can be modified in the Settings module under Technical > Scheduled Actions.

**Structure:**
- **Root Element:** The root element encapsulates the data.
- **Data Element:** Indicates records within this block should not be updated automatically during module updates.
- **Cron Job Record:**
  - `ID`: `cron_invoice_reminder` - uniquely identifies this cron job.
  - `name`: "Invoice Reminder".
  - `model_id`: Links to `account.move`, related to accounting moves (invoices).
  - `state`: Set to `code`, indicating action in code form.
  - `code`: Contains Python code for calculating dates, filtering invoices, and sending reminder emails.
  - `active`: Indicates the cron job is active.
  - `interval_number`, `interval_type`: Schedules the job to run every day.
  - `numbercall`: `-1` for indefinite running.
  - `doall`: Set to `False`, avoiding runs for missed times if the server was down.

#### Python Code Analysis:
- **Calculate Date 7 Days Ago:**
  ```python
  seven_days_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).date()
Computes the date seven days before the current date using the datetime module.

- **Filter Invoices:**

pending_invoices = env["account.move"].search([
  "&", "&", 
  ("move_type", "=", "out_invoice"), 
  ("payment_state", "in", ["partial", "not_paid"]), 
  ("invoice_date_due", "<", seven_days_ago)])
Retrieves invoices that are customer invoices, either partially paid or not paid, and due earlier than seven days ago.

- **Email Template Lookup and Sending Emails:**

template = env.ref('invoice_reminder.invoice_reminder_email_template', raise_if_not_found=False)
if template:
    for pending_invoice in pending_invoices:
        template.send_mail(pending_invoice.id, force_send=False, raise_exception=False)
Looks up an email template and sends emails to each filtered invoice using the template.

### 2. invoice_reminder_email_template.xml
**Overview:** Defines the email template for sending payment reminders, editable in Settings > Technical > Email Templates.

**Structure:**
- **Root Element:** Root of the XML.
- **Data Element:** Can be updated.
- **Email Template Record:**
  - `ID`: `invoice_reminder_email_template` - uniquely identifies this email template.
  - `Model`: `mail.template` - specifies the type of the record.
  - `Fields`: Includes key fields of the email template.
    - `name`: The name of the template.
    - `model_id`: Refers to the `account.move` model, linking the template to invoices.
    - `subject`: Subject line of the email.
    - `email_from`: Sender's email address, set dynamically.
    - `body_html`: HTML content of the email.
    - `lang`: Language of the email template, set based on the recipient's language.
    - `auto_delete`: Set to `False`, emails are not deleted after sending.


##Installation: Ensure these XML files are correctly placed in your Odoo addons directory and that the invoice_reminder module is properly installed.

##Customization: Feel free to duplicate and adjust the Python code and email template to fit your business logic and branding, as per the instructions in each file's overview.





