# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pprint

import requests
from werkzeug.urls import url_join

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.payment_intasend import const


_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('intasend', "IntaSend")], ondelete={'intasend': 'set default'}
    )
    intasend_public_key = fields.Char(
        string="IntaSend Public Key",
        help="The key solely used to identify the account with IntaSend.",
        required_if_provider='intasend',
    )
    intasend_secret_key = fields.Char(
        string="IntaSend Secret Key",
        required_if_provider='intasend',
        groups='base.group_system',
    )
    intasend_webhook_secret = fields.Char(
        string="IntaSend Webhook Secret",
        required_if_provider='intasend',
        groups='base.group_system',
    )

    #=== COMPUTE METHODS ===#

    def _compute_feature_support_fields(self):
        """ Override of `payment` to enable additional features. """
        super()._compute_feature_support_fields()
        self.filtered(lambda p: p.code == 'intasend').update({
            'support_tokenization': True,
        })

    # === BUSINESS METHODS ===#

    @api.model
    def _get_compatible_providers(self, *args, is_validation=False, **kwargs):
        """ Override of `payment` to filter out IntaSend providers for validation operations. """
        providers = super()._get_compatible_providers(*args, is_validation=is_validation, **kwargs)

        if is_validation:
            providers = providers.filtered(lambda p: p.code != 'intasend')

        # _logger.info("Compatible providers: %s", providers)
        return providers

    def _get_supported_currencies(self):
        """ Override of `payment` to return the supported currencies. """
        supported_currencies = super()._get_supported_currencies()
        if self.code == 'intasend':
            supported_currencies = supported_currencies.filtered(
                lambda c: c.name in const.SUPPORTED_CURRENCIES
            )
        # _logger.info("Supported currencies for provider %s: %s", self.code, supported_currencies)
        return supported_currencies

    def _intasend_make_request(self, endpoint, payload=None, method='POST'):
        """ Make a request to IntaSend API at the specified endpoint.

        Note: self.ensure_one()

        :param str endpoint: The endpoint to be reached by the request.
        :param dict payload: The payload of the request.
        :param str method: The HTTP method of the request.
        :return The JSON-formatted content of the response.
        :rtype: dict
        :raise ValidationError: If an HTTP error occurs.
        """
        if not self.exists():
            raise ValueError("No payment provider record found.")
        elif len(self) > 1:
            raise ValueError("Expected singleton: multiple payment provider records found.")

        # Add debugging information
        # _logger.info(f"Found payment provider records: {len(self)}")

        
        self.ensure_one()

        url = url_join('https://api.intasend.com/api/v1/', endpoint + '/')
        headers = {
            'X-IntaSend-Public-API-Key': f'{self.intasend_public_key}',
            'accept': 'application/json',
            'content-type': 'application/json',
        }
        # _logger.info("Request URL: %s", url)
        # _logger.info("Request method: %s", method)
        # _logger.info("Request headers: %s", headers)
        # _logger.info("Request payload: %s", payload)
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            response.raise_for_status()  # This will raise an HTTPError for bad responses
            
        except requests.exceptions.HTTPError as e:
            # _logger.exception(
            #     "Invalid API request at %s with data:\n%s", url, pprint.pformat(payload),
            # )
            # _logger.error("Response content: %s", response.content)
            raise ValidationError("IntaSend: " + _(
                "Something went wrong  when processing the payment"
            ))
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            # _logger.exception("Unable to reach endpoint at %s", url)
            raise ValidationError(
                "IntaSend: " + _("Could not establish the connection to the API.")
            )

        # _logger.info("Response JSON: %s", response.json())
        return response.json()


    def _get_default_payment_method_codes(self):
        """ Override of `payment` to return the default payment method codes. """
        default_codes = super()._get_default_payment_method_codes()
        if self.code != 'intasend':
            return default_codes
        # _logger.info("Default payment method codes for IntaSend: %s", const.DEFAULT_PAYMENT_METHODS_CODES)
        return const.DEFAULT_PAYMENT_METHODS_CODES
