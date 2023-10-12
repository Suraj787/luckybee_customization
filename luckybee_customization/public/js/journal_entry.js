frappe.ui.form.on('Journal Entry', {
	onload: function (frm) {
		frm.fields_dict['voucher_type'].df.onchange = function () {
			if (frm.doc.voucher_type === 'Contra Entry') {
				contra_entry(frm);
			} else {
				not_contra_entry(frm);
			}
			// frm.fields_dict['accounts'].refresh();
		};
	}
});

function contra_entry(frm) {
	console.log("contra");
	frm.fields_dict['accounts'].grid.get_field('account').get_query = function (doc, cdt, cdn) {
		return {
			filters: [
				['Account', 'account_type', 'in', ['Bank', 'Cash']]
			]
		};
	};
}

function not_contra_entry(frm) {
	console.log("non contra");
	// frm.fields_dict['accounts'].refresh();

	if (frm.fields_dict['accounts'] && frm.fields_dict['accounts'].grid) {
	frm.fields_dict['accounts'].grid.get_field('account').get_query = function (doc, cdt, cdn) {

	}

	frm.set_query("account", "accounts", function(doc) {
		var filters = {
			company: frm.doc.company,
			is_group: 0
		};
		if (!frm.doc.multi_currency) {
			$.extend(filters, {
				account_currency: frappe.get_doc(":Company", frm.doc.company).default_currency
			});
		}
		console.log("filters", filters)
		return { filters: filters };
	});
	
	}
	else {
		console.log('accounts table not found');
        setTimeout(function() {
            not_contra_entry(frm);
        }, 500); // Retry after a short delay if the grid is not yet available
    }

}