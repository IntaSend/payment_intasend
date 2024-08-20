# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Payment Provider: IntaSend",
    'version': '1.0',
    'category': 'Accounting/Payment Providers',
    'sequence': 350,
    'website': 'https://intasend.com',
    'author': 'IntaSend Team',
    'installable': True,
    'summary': "Payment gateway provider for the Kenyan market. Get M-Pesa, PesaLink, and card payments.",
    'description': """
        <p><strong>Payment Provider:</strong> IntaSend</p>
        <p>Payment gateway provider for the Kenyan market. Get M-Pesa, PesaLink, and card payments.</p>
        <ul>
            <li><strong>Version:</strong> 1.0</li>
            <li><strong>License:</strong> LGPL-3</li>
            <li><strong>Website:</strong> <a href="https://intasend.com">https://intasend.com</a></li>
        </ul>
    """,
    'depends': ['base', 'payment'],
    'data': [
        'views/payment_templates.xml',
        'views/payment_provider_views.xml',
        'data/payment_provider_data.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'license': 'LGPL-3',
    'images': ['static/description/cover_image.jpeg'],  # Add this line
}
