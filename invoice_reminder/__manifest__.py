{
    'name': 'Invoice Reminder',
    'version': '16.0.0.0',
    'summary': 'Automatic reminder for unpaid invoices 7 days after due date has passed',
    'depends': ['account'],
    'data': [
        'data/cron_invoice_reminder.xml',
        'data/invoice_reminder_email_template.xml',
    ],
    'installable': True,
}
