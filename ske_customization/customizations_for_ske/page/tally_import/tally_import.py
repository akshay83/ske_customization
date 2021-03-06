import frappe
import json
import xmltodict
import lzstring
from xmltodict import ParsingInterrupted
from ske_customization.customizations_for_ske.page.tally_import.import_modules.currency_items import TallyImportCurrencyItems
from ske_customization.customizations_for_ske.page.tally_import.import_modules.godown_items import TallyImportGodownItems
from ske_customization.customizations_for_ske.page.tally_import.import_modules.stockgroup_items import TallyImportStockGroupItems
from ske_customization.customizations_for_ske.page.tally_import.import_modules.stockcategory_items import TallyImportStockCategoryItems
from ske_customization.customizations_for_ske.page.tally_import.import_modules.stock_items import TallyImportStockItems
from ske_customization.customizations_for_ske.page.tally_import.import_modules.sundrydebtors import TallyImportSundryDebtors
from ske_customization.customizations_for_ske.page.tally_import.import_modules.units import TallyImportUnits

overwrite_existing = True
opening_date = None

@frappe.whitelist()
def read_uploaded_file(filedata=None,decompress_data=0,overwrite=False,open_date=None,brand=None):
	if not filedata:
		return

	lx = lzstring.LZString()

	if (int(decompress_data)>0):
		frappe.publish_realtime("tally_import_progress", {
				"message": "Decompressing"
				}, user=frappe.session.user)

		filedata = lx.decompressFromUTF16(filedata)

		frappe.publish_realtime("tally_import_progress", {
				"message": "Decompression Complete"
				}, user=frappe.session.user)

	params = json.loads(frappe.form_dict.get("params") or '{}')

	if params.get("overwrite"):
		overwrite = params.get("overwrite")
	if params.get("open_date"):
		open_date = params.get("open_date")
	if params.get("brand"):
		brand = params.get("brand")

	global overwrite_existing
	overwrite_existing = overwrite

	global opening_date
	opening_date = open_date

	brand = brand.replace(" ","") + ","
	global brand_category
	brand_category = brand.upper().rstrip(",").split(",") 

	try:
		xmltodict.parse(filedata, item_depth=5, item_callback=process)
	except ParsingInterrupted:
		frappe.db.rollback()
		return {"messages": ["There was a Problem Importing" + ": " + "HG"], "error": True}

	frappe.db.commit()
	frappe.publish_realtime("tally_import_progress", {
						"message": "Processed Batch"
					}, user=frappe.session.user)

	return {"messages": "Import Successful", "error": False}


def document_import(item):
	if (item.has_key('UNIT')):
		TallyImportUnits(value=item['UNIT'],ow=overwrite_existing)
	elif (item.has_key('CURRENCY')):
		TallyImportCurrencyItems(value=item['CURRENCY'],ow=overwrite_existing)
	elif (item.has_key('GODOWN')):
		TallyImportGodownItems(value=item['GODOWN'],ow=overwrite_existing)
	elif (item.has_key('STOCKCATEGORY')):
		TallyImportStockCategoryItems(value=item['STOCKCATEGORY'],ow=overwrite_existing)	
	elif (item.has_key('STOCKGROUP')):
		TallyImportStockGroupItems(value=item['STOCKGROUP'],ow=overwrite_existing)
	elif (item.has_key('STOCKITEM')):
		TallyImportStockItems(value=item['STOCKITEM'],ow=overwrite_existing, od=opening_date, bc=brand_category)
	elif (item.has_key('LEDGER')):
		TallyImportSundryDebtors(value=item['LEDGER'],ow=overwrite_existing, od=opening_date)
	else: 
		return 'Skipped'
	return 'Success'

def process(path, item):
	if (isinstance(item, (dict, set)) and len(item)>0):	

		test_item = item[item.keys()[0]]

		if (isinstance(test_item, dict) and test_item.has_key('@NAME')):
			message = document_description = item.keys()[0] + " <> " + test_item['@NAME']
		else:
			message = document_description = ''.join(test_item)

		try:
			status = document_import(item)
			if (status == 'Skipped'):				
				message = 'Skipped : ' + message
		except Exception, e:
			print e
			message = 'Failed to Import : ' + message
			frappe.publish_realtime("tally_import_progress", {
				"message": message, 
				"error":True,
				"error_desc": e,
				}, user=frappe.session.user)
			return True

		if (message[:7] != 'Skipped'):
			message = 'Successfully Imported : ' + message

	return True

