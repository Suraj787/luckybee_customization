import json
import keepa
import frappe
from frappe import _



def update_item(doc, event):
	accesskey = '4i9vbmksc3d9o67p6fd3s9aitdaaer17c604f3qrh93auu67fnh6pfucqvqltmjm'
	api = keepa.Keepa(accesskey)
	ASIN = [row.item_code for row in doc.items]
	products = api.query(ASIN)
	for i in range(len(ASIN)):
		item = frappe.get_doc("Item", ASIN[i])
		item.manufacturer = products[i]["manufacturer"]
		item.listed_since = products[i]['listedSince']
		item.sales_rank = json.dumps(products[i]['salesRanks'])
		item.sales_rank_ref = products[i]['salesRankReference']
		# item.sales_rank_sub
		item.reviews_count = products[i]['csv'][17]  # 1
		item.title = products[i]['title']
		item.categories_tree = json.dumps(products[i]['categoryTree'])
		item.ean = json.dumps(products[i]['eanList'])
		item.upc = json.dumps(products[i]['upcList'])
		item.launchpad = products[i]['launchpad']  # currently a data field, should be checkbox
		item.partnumber = products[i]['partNumber']
		item.freq_brought_together = json.dumps(products[i]['frequentlyBoughtTogether'])
		item.product_group = products[i]['productGroup']
		item.number_of_items = products[i]['numberOfItems']
		item.package_height = products[i]['packageHeight']
		item.package_length = products[i]['packageLength']
		item.package_width = products[i]['packageWidth']
		item.package_weight = products[i]['packageWeight']
		item.package_quantity = products[i]['packageQuantity']
		item.model = products[i]['model']
		item.length_length = products[i]['itemLength']
		# item.length_breadth = products[i]['packageQuantity']   # ?
		item.length_height = products[i]['itemHeight']
		item.length_weight = products[i]['itemWeight']
		# item.parent_asin = products[i]['parentAsin']  # 3
		item.category_root = products[i]['rootCategory']
		item.size = products[i]['size']
		item.color = products[i]['color']
		# products[1]['variations']   # dimension, attributes, variation_asins
		# item.variation_asins
		# category_sub
		# amazon_url
		item.save()

	frappe.msgprint(_("Items have been updated"))
	
