import json
import keepa
import frappe
from frappe import _
import re
from frappe.utils import today



def update_item(doc, event):
	accesskey = '4i9vbmksc3d9o67p6fd3s9aitdaaer17c604f3qrh93auu67fnh6pfucqvqltmjm'
	api = keepa.Keepa(accesskey)
	ASIN = [row.custom_asin for row in doc.items if row.custom_asin]
	if ASIN:
		try:
			products = api.query(ASIN, stats=30, update=0, domain="IN", history=1)
			for i in range(len(ASIN)):
				item = frappe.get_doc("Item", {"custom_asin": ASIN[i]})
				if item:

					# frappe.log_error(f'products[i]["title"]: {products[i]["title"]}')
					# item.item_name = products[i]["title"]
					# item.item_name = "test name"

					# frappe.log_error(f'len products[i]["title"]: {len(products[i]["title"])}')
					if products[i]["imagesCSV"]:
						item.image = "https://images-na.ssl-images-amazon.com/images/I/" + products[i]["imagesCSV"].split(',')[0]
					item.manufacturer = products[i]["manufacturer"]
					item.listed_since = products[i]['listedSince']
					# item.sales_rank = json.dumps(products[i]['salesRanks'])
					item.sales_rank_ref = products[i]['salesRankReference']
					item.reviews_count = products[i]['csv'][17]  # 1
					# item.title = products[i]['title']
					category_tree = []
					category_tree_dict = {}
					if products[i].get('categoryTree'):
						category_tree = [i.get("name") for i in products[i].get('categoryTree')]
						category_tree_dict = {i["catId"]:i["name"] for i in products[i]['categoryTree']}

					if category_tree:
						item.category_sub = category_tree[-1]
						item.categories_tree = ", ".join(category_tree)
					if category_tree_dict:
						item.category_root = category_tree_dict.get(products[0].get('rootCategory'))
					
					# item.ean =  re.findall('[0-9]+', json.dumps(products[i]['eanList'][0]))[0] if products[i]['eanList'] is not None else ''
					item.ean =  products[i]['eanList'][0] if products[i]['eanList'] else ''

					item.upc = json.dumps(products[i]['upcList'])
					item.launchpad = products[i]['launchpad']  # currently a data field, should be checkbox
					item.partnumber = products[i]['partNumber']
					frequently_bought_together = products[i]['frequentlyBoughtTogether']
					if isinstance(frequently_bought_together, (list, tuple)):
						item.freq_brought_together = ", ".join(frequently_bought_together)
					else:
						item.freq_brought_together = ""

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
					item.size = products[i]['size']
					item.color = products[i]['color']
					item.desc_feature = products[i]["description"]
					if products[0]['features'] and len(products[0]['features']) >= 5:
						item.desc_feature_1 = products[0]['features'][0]
						item.desc_feature_2 = products[0]['features'][1]
						item.desc_feature_3 = products[0]['features'][2]
						item.desc_feature_4 = products[0]['features'][3]
						item.desc_feature_5 = products[0]['features'][4]
					stats_parsed = products[i].get("stats_parsed")
					if stats_parsed:
						current = stats_parsed.get("current")
						avg30 = stats_parsed.get("avg30")
						avg90 = stats_parsed.get("avg90")
						avg180 = stats_parsed.get("avg180")
						if current:
							item.current_price = current.get("SALES")
							item.last_price = current.get("LISTPRICE")
							item.new_current = current.get("NEW")
						if avg30:
							item.custom_sales_30days = avg30.get("SALES")
							item.list_price_30days = avg30.get("LISTPRICE")
							item.new_30days = avg30.get("NEW")
						if avg90:
							item.custom_sales_90days = avg90.get("SALES")
							item.list_price_90days = avg90.get("LISTPRICE")
							item.new_90days = avg90.get("NEW")
						if avg180:
							item.custom_sales_180days = stats_parsed.get("avg180").get("SALES")
							item.list_price_180days = stats_parsed.get("avg180").get("LISTPRICE")
							item.new_180days = stats_parsed.get("avg180").get("NEW")

					item.save()
					frappe.db.set_value("Item", item.name, "title", products[i]['title'])
					frappe.db.set_value("Item", item.name, "item_name", products[i]["title"])

			frappe.msgprint(_("Items have been updated"))
		except Exception as e:
			frappe.throw(_("Found invalid ASIN"))
	

def sync_keepa_item(doc, event):
	accesskey = '4i9vbmksc3d9o67p6fd3s9aitdaaer17c604f3qrh93auu67fnh6pfucqvqltmjm'
	api = keepa.Keepa(accesskey)
	if doc.custom_asin:
		ASIN = [doc.custom_asin]
		try:
			products = api.query(ASIN, stats=30, update=0, domain="IN", history=1)
			for i in range(len(ASIN)):
				if products[i]["imagesCSV"]:
					doc.image = "https://images-na.ssl-images-amazon.com/images/I/" + products[i]["imagesCSV"].split(',')[0]
				doc.manufacturer = products[i]["manufacturer"]
				doc.listed_since = products[i]['listedSince']
				doc.sales_rank_ref = products[i]['salesRankReference']
				doc.reviews_count = products[i]['csv'][17]  # 1
				category_tree = []
				category_tree_dict = {}
				if products[i].get('categoryTree'):
					category_tree = [i.get("name") for i in products[i].get('categoryTree')]
					category_tree_dict = {i["catId"]:i["name"] for i in products[i]['categoryTree']}

				if category_tree:
					doc.category_sub = category_tree[-1]
					doc.categories_tree = ", ".join(category_tree)
				if category_tree_dict:
					doc.category_root = category_tree_dict.get(products[0].get('rootCategory'))
				
				# doc.ean =  re.findall('[0-9]+', json.dumps(products[i]['eanList'][0]))[0] if products[i]['eanList'] is not None else ''
				doc.ean =  products[i]['eanList'][0] if products[i]['eanList'] else ''

				doc.upc = json.dumps(products[i]['upcList'])
				doc.launchpad = products[i]['launchpad']  # currently a data field, should be checkbox
				doc.partnumber = products[i]['partNumber']
				frequently_bought_together = products[i]['frequentlyBoughtTogether']
				if isinstance(frequently_bought_together, (list, tuple)):
					doc.freq_brought_together = ", ".join(frequently_bought_together)
				else:
					doc.freq_brought_together = ""

				doc.product_group = products[i]['productGroup']
				doc.number_of_items = products[i]['numberOfItems']
				doc.package_height = products[i]['packageHeight']
				doc.package_length = products[i]['packageLength']
				doc.package_width = products[i]['packageWidth']
				doc.package_weight = products[i]['packageWeight']
				doc.package_quantity = products[i]['packageQuantity']
				doc.model = products[i]['model']
				doc.length_length = products[i]['itemLength']
				doc.length_height = products[i]['itemHeight']
				doc.length_weight = products[i]['itemWeight']
				doc.size = products[i]['size']
				doc.color = products[i]['color']
				doc.desc_feature = products[i]["description"]
				shortened_title = products[i]['title'][:140] if products[i]['title'] is not None else ""
				doc.title = shortened_title
				doc.item_name = shortened_title
				if products[0]['features'] and len(products[0]['features']) >= 5:
					doc.desc_feature_1 = products[0]['features'][0]
					doc.desc_feature_2 = products[0]['features'][1]
					doc.desc_feature_3 = products[0]['features'][2]
					doc.desc_feature_4 = products[0]['features'][3]
					doc.desc_feature_5 = products[0]['features'][4]
				stats_parsed = products[i].get("stats_parsed")
				if stats_parsed:
					current = stats_parsed.get("current")
					avg30 = stats_parsed.get("avg30")
					avg90 = stats_parsed.get("avg90")
					avg180 = stats_parsed.get("avg180")
					if current:
						doc.current_price = current.get("SALES")
						doc.last_price = current.get("LISTPRICE")
						doc.new_current = current.get("NEW")
					if avg30:
						doc.custom_sales_30days = avg30.get("SALES")
						doc.list_price_30days = avg30.get("LISTPRICE")
						doc.new_30days = avg30.get("NEW")
					if avg90:
						doc.custom_sales_90days = avg90.get("SALES")
						doc.list_price_90days = avg90.get("LISTPRICE")
						doc.new_90days = avg90.get("NEW")
					if avg180:
						doc.custom_sales_180days = stats_parsed.get("avg180").get("SALES")
						doc.list_price_180days = stats_parsed.get("avg180").get("LISTPRICE")
						doc.new_180days = stats_parsed.get("avg180").get("NEW")

			frappe.msgprint(_("Item has been synced with keepa"))
		except Exception as e:
			frappe.throw(_(f"Invalid ASIN: {doc.custom_asin}"))

def create_selling_price(doc, event):
	for item in doc.items:
		if item.rate > 0:
			item_price_exists = frappe.db.get_all("Item Price", {"item_code": item.item_code, "selling": 1, "price_list": "Standard Selling"})
			if not item_price_exists:
				item_master = frappe.get_doc("Item", item.item_code)
				item_price = frappe.new_doc("Item Price")
				item_price.item_code = item.item_code
				item_price.price_list = "Standard Selling"
				item_price.selling = 1
				item_price.item_name = item_master.item_name
				item_price.uom = item_master.stock_uom
				item_price.valid_from = today()
				item_price.currency = frappe.db.get_value("Company", doc.company, "default_currency")
				selling_rate = item.rate + ( 0.05 * item.rate)  # Calculate selling rate with a 5% margin
				item_price.price_list_rate = round(selling_rate, 9) # Format the selling rate to end with 9
				item_price.save()


def create_item_price(doc, event):
	if frappe.db.exists("Item", {"name": doc.name}):
		if doc.custom_mrp != frappe.db.get_value("Item", doc.name, "custom_mrp"):
			item_price = frappe.new_doc("Item Price")
			item_price.item_code = doc.item_code
			item_price.price_list = "Standard Selling"
			item_price.selling = 1
			item_price.item_name = doc.item_name
			item_price.uom = doc.stock_uom
			item_price.valid_from = today()
			item_price.price_list_rate = float(doc.custom_mrp) -  (0.05 * float(doc.custom_mrp))  # Calculate selling rate with a 5% margin
			item_price.save()