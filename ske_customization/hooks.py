# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "ske_customization"
app_title = "Customizations for SKE"
app_publisher = "Akshay Mehta"
app_description = "Customizations Done Specifically for Mehta Automobiles Pvt Ltd"
app_icon = "octicon octicon-file-directory"
app_color = "#589494"
app_email = "mehta.akshay@gmail.com"
app_version = "0.0.1"
app_license = "MIT"

fixtures = ["Custom Field", "Property Setter", "Stock Settings", "Selling Settings","Buying Settings","Custom Script",
		 "Print Format", "Letter Head", "Workflow", "Workflow State", "Workflow Action", "Custom SQL Queries"]

doc_events = {
	"Item" : {
		"validate" : "ske_customization.customizations_for_ske.item_hooks.item_validate"
	},
	"Sales Order": {
		"validate" : "ske_customization.customizations_for_ske.finance_validation.sales_order_validate",
		"before_cancel": "ske_customization.customizations_for_ske.pe_on_sales_order.before_cancel_sales_order",
		"on_submit": "ske_customization.customizations_for_ske.pe_on_sales_order.make_payment_entry_with_sales_order",
		"validate": "ske_customization.customizations_for_ske.pe_on_sales_order.validate"
	},
	"Payment Entry": {
		"validate": "ske_customization.customizations_for_ske.finance_validation.payment_entry_validate",
		"on_update_after_submit":"ske_customization.customizations_for_ske.payment_entry_hooks.payment_entry_on_update_after_submit"		
	},
	"Purchase Receipt" : {
		"on_submit" : "ske_customization.customizations_for_ske.utils.purchase_receipt_on_submit",
		"validate" : "ske_customization.customizations_for_ske.utils.purchase_receipt_validate"
	},
	"Purchase Invoice" : {
		"on_submit" : "ske_customization.customizations_for_ske.utils.purchase_receipt_on_submit",
		"validate" : "ske_customization.customizations_for_ske.utils.purchase_receipt_validate",
		"on_update_after_submit":"ske_customization.customizations_for_ske.purchase_invoice_hooks.purchase_invoice_on_update_after_submit"
	},
	"Sales Invoice" : {
		"validate" : "ske_customization.customizations_for_ske.finance_validation.sales_invoice_validate",
		"before_save": "ske_customization.customizations_for_ske.workflow_hooks.before_save_salesinvoice",
		"on_update_after_submit":"ske_customization.customizations_for_ske.sales_invoice_hooks.sales_invoice_on_update_after_submit"
	},
	"Selling Settings" : {
		"on_update": "ske_customization.customizations_for_ske.workflow_hooks.on_update_selling_settings"
	},
        "Stock Entry" : {
                "validate": "ske_customization.customizations_for_ske.finance_validation.validate_stock_entry_serial_no"
        }
}
app_include_css = "/assets/ske_customization/css/custom_css.css"
app_include_js = ["/assets/ske_customization/js/side_bar.js",
				"/assets/ske_customization/js/form_comments.js",
				"/assets/ske_customization/js/core.js",
				"/assets/ske_customization/js/lz-string.min.js",
				"/assets/ske_customization/js/quick_customer.js"
				]

jenv_filter = [
    'json_load:ske_customization.customizations_for_ske.jinja.json_load'
]

#Monkey Patch
from ske_customization.customizations_for_ske.monkey_patch import do_monkey_patch
do_monkey_patch()

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ske_customization/css/ske_customization.css"
# app_include_js = "/assets/ske_customization/js/ske_customization.js"

# include js, css files in header of web template
# web_include_css = "/assets/ske_customization/css/ske_customization.css"
# web_include_js = "/assets/ske_customization/js/ske_customization.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "ske_customization.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "ske_customization.install.before_install"
# after_install = "ske_customization.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ske_customization.notifications.get_notification_config"

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

# scheduler_events = {
# 	"all": [
# 		"ske_customization.tasks.all"
# 	],
# 	"daily": [
# 		"ske_customization.tasks.daily"
# 	],
# 	"hourly": [
# 		"ske_customization.tasks.hourly"
# 	],
# 	"weekly": [
# 		"ske_customization.tasks.weekly"
# 	]
# 	"monthly": [
# 		"ske_customization.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "ske_customization.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "ske_customization.event.get_events"
# }
