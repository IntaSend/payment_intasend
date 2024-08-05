# Part of Odoo. See LICENSE file for full copyright and licensing details.

# The currencies supported by IntaSend, in ISO 4217 format.
# Last website update: June 2024.
# Last seen online: 24 June 2024.
SUPPORTED_CURRENCIES = [
    'GBP',
    'EUR',
    'KES',
    'USD',
]

# Mapping of transaction states to IntaSend payment statuses.
PAYMENT_STATUS_MAPPING = {
    'pending': ['pending auth'],
    'done': ['successful'],
    'cancel': ['cancelled'],
    'error': ['failed'],
}

# The codes of the payment methods to activate when IntaSend is activated.
DEFAULT_PAYMENT_METHODS_CODES = [
    # Primary payment methods.
    'card',
    'mpesa',
    # Brand payment methods.
    'visa',
    'mastercard',
]

PAYMENT_METHODS_MAPPING = {
    'bank_transfer': 'banktransfer',
}
