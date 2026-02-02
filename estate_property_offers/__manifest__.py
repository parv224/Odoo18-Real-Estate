{
    "name": "Estate Property Offers",
    "summary": "Manage property listings and offers",
    "version": "18.0.1.0",
    "author": "Odoo PS",
    "website": "http://www.odoo.com",
    "license": "LGPL-3",
    "category": "Sales",
    "depends": ["base"],
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_type_views.xml",
        "views/estate_property_tags_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_views.xml",
        "views/estate_menus.xml",
        
        "static/description/icon.png"
        "static/description/cover.png"
        "static/description/index.html"
    
    ],
    "demo": [
        "demo/demo.xml"
    ],
    "installable": True,
}
