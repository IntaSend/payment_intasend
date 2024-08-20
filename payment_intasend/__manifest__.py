# Part of Odoo. See LICENSE file for full copyright and licensing details.

import os

def get_description():
    with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as readme_file:
        return readme_file.read()

{
    'name': "Payment Provider: IntaSend",
    'version': '1.0',
    'category': 'Accounting/Payment Providers',
    'sequence': 350,
    'website': 'https://intasend.com',
    'author': 'IntaSend Team',
    'installable': True,
    'summary': "Payment gateway provider for the Kenyan market. Get M-Pesa, PesaLink, and card payments.",
    'description': get_description(),  # Load the description from README
    'depends': ['base', 'payment'],
    'data': [
        'views/payment_templates.xml',
        'views/payment_provider_views.xml',
        'data/payment_provider_data.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'license': 'LGPL-3',
    'images': ['static/description/cover_image.jpeg'],
}
