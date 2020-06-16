#!/bin/bash
python manage.py migrate && gunicorn ippe.wsgi:application