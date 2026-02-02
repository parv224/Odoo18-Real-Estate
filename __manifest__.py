{
    "name": "Real Estate",
    "summary": "Simple real estate property and offer management",
    "version": "18.0.1.0",
    "author": "Odoo PS",
    "website": "http://www.odoo.com",
    "license": "LGPL-3",
    "category": "Sales",
    "depends": ["base", "crm"],
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_type_views.xml",
        "views/estate_property_tags_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_views.xml",
        "views/estate_menus.xml",
    ],
    "demo": [
        "demo/demo.xml"
    ],
    "installable": True,
}
