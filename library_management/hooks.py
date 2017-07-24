# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe.utils import datediff, nowdate, format_date, add_days
from . import __version__ as app_version

app_name = "library_management"
app_title = "Library Management"
app_publisher = "Frappe"
app_description = "App for managing Articles, Members, Memberships and Transact for Libraries"
app_icon = "octicon octicon-book"
app_color = "#589494"
app_email = "shreyashah115@gmail.com"
app_license = "GNU General Public License"

def daily():
	loan_period = frappe.db.get_value("Library Management Settings",
		None, "loan_period")
	overdue = get_overdue(loan_period)
	for member, items in overdue.iteritems():
		content = """<h2> Following Items are Overdue</h2>
		<p> Please return them as soon as possible </p><ol>"""
		for i in items:
			content += "<li>{0} ({1}) due on {2} </li>".format(i.article_name, i.article, format_date(add_days(i.transaction_date, loan_period)))
		content += "</ol>"

		recipient = frappe.db.get_value("Library Member", member, "email_id")
		frappe.sendmail(recipients = [recipient],
			sender = "test@example.com",
			subject = "Library Articles Overdue", content = content, bulk = True)

def get_overdue(loan_period):
	#check for overdue articles
	today = nowdate()

	overdue_by_member = {}
	articles_transacted = []

	for d in frappe.db.sql("""select name, article, article_name, library_member, member_name
		from `tabLibrary Transaction`
		order by transaction_date desc, modified desc""", as_dict=1):

		if d.article in articles_transacted:
			continue

		if d.transaction_type=="Issue" and \
			datediff(today, d.transaction_date) > loan_period:
			overdue_by_member.setdefault(d.library_member,[])
			overdue_by_member[d.library_member].append(d)
			
		articles_transacted.append(d.article)

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/library_management/css/library_management.css"
# app_include_js = "/assets/library_management/js/library_management.js"

# include js, css files in header of web template
# web_include_css = "/assets/library_management/css/library_management.css"
# web_include_js = "/assets/library_management/js/library_management.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "library_management.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "library_management.install.before_install"
# after_install = "library_management.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "library_management.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
# 	"all": [
# 		"library_management.tasks.all"
# 	],
	"daily": [
		"library_management.tasks.daily"
	],
}
# 	"hourly": [
# 		"library_management.tasks.hourly"
# 	],
# 	"weekly": [
# 		"library_management.tasks.weekly"
# 	]
# 	"monthly": [
# 		"library_management.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "library_management.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "library_management.event.get_events"
# }

