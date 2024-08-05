import logging
import pprint
import requests
from pprint import pformat
from werkzeug import urls
from odoo import _, models
from odoo.exceptions import UserError, ValidationError
from odoo.addons.payment import utils as payment_utils
from odoo.addons.payment_intasend import const
from odoo.addons.payment_intasend.controllers.main import IntaSendController

_logger = logging.getLogger(__name__)

class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        """ Override of payment to return IntaSend-specific rendering values.

        Note: self.ensure_one() from `_get_processing_values`

        :param dict processing_values: The generic and specific processing values of the transaction
        :return: The dict of provider-specific processing values.
        :rtype: dict
        """
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'intasend':
            return res
        
        # _logger.info("DATA IN SELF XXXXXXXXXXXXXXXXXXXXXXXXXXXXX: %s", pformat(self.read()[0]))

        partner_country = self.partner_country_id[1] if self.partner_country_id and len(self.partner_country_id) > 1 else None
        partner_state = self.partner_state_id[1] if self.partner_state_id and len(self.partner_state_id) > 1 else None
        

        # Extract data from self
        first_name, last_name = payment_utils.split_partner_name(self.partner_name)
        base_url = self.provider_id.get_base_url()
        payload = {
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": self.partner_phone,
            "email": self.partner_email,
            "country": partner_country,
            "address": self.partner_address,
            "city": self.partner_city,
            "state": partner_state,
            "zipcode": self.partner_zip,
            "api_ref": self.reference,
            "method": "CARD-PAYMENT",
            "redirect_url": urls.url_join(base_url, IntaSendController._return_url),
            "amount": str(self.amount),
            "currency": self.currency_id.name,
            "mobile_tarrif": "BUSINESS-PAYS",
            "card_tarrif": "BUSINESS-PAYS",
            "bitcoin_tarrif": "BUSINESS-PAYS",
            "ach_tarrif": "BUSINESS-PAYS"
        }

        # _logger.info("Payload for IntaSend: %s", payload)

        # Make the request to IntaSend
        response = self.provider_id._intasend_make_request('checkout', payload=payload)

        # Check the response and handle errors
        # if response.status_code != 200:
        #     raise ValidationError("IntaSend: " + _("Error in the response from IntaSend API."))

        # _logger.info("Response from IntaSend: %s", response)

        rendering_values = {
            'api_url': response['url'],
        }
        return rendering_values

    def _send_payment_request(self):
        """ Override of payment to send a payment request to IntaSend.

        Note: self.ensure_one()

        :return: None
        :raise UserError: If the transaction is not linked to a token.
        """
        super()._send_payment_request()
        if self.provider_code != 'intasend':
            return

        if not self.token_id:
            raise UserError("IntaSend: " + _("The transaction is not linked to a token."))

        first_name, last_name = payment_utils.split_partner_name(self.partner_name)
        data = {
            'token': self.token_id.provider_ref,
            'email': self.token_id.intasend_customer_email,
            'amount': self.amount,
            'currency': self.currency_id.name,
            'country': self.company_id.country_id.code,
            'tx_ref': self.reference,
            'first_name': first_name,
            'last_name': last_name,
            'ip': payment_utils.get_customer_ip_address(),
        }

        response_content = self.provider_id._intasend_make_request('tokenized-charges', payload=data)
        # _logger.info(
        #     "Payment request response for transaction with reference %s:\n%s",
        #     self.reference, pprint.pformat(response_content)
        # )
        
        self._handle_notification_data('intasend', response_content['data'])

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        # _logger.info("Notification data received: %s", json.dumps(notification_data, indent=4))
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'intasend' or len(tx) == 1:
            # _logger.info("Transaction found: %s", json.dumps(tx, indent=4))
            return tx

        reference = notification_data.get('tracking_id')
        signature = notification_data.get('signature')
        checkout_id = notification_data.get('checkout_id')
        if not reference:
            # _logger.error("Received data with missing reference.")
            raise ValidationError("IntaSend: " + _("Received data with missing reference."))

        # _logger.info("Verification data for IntaSend: checkout_id=%s, signature=%s", checkout_id, signature)
        

        payload = {
            'checkout_id': checkout_id,
            'signature': signature
        }

        intasend_provider = self.env['payment.provider'].search([('code', '=', 'intasend')], limit=1)
        if not intasend_provider:
            raise ValidationError(_("No IntaSend payment provider found."))
        response = intasend_provider._intasend_make_request('checkout/details', payload=payload)

        verification_response_content = response


        # _logger.info("Verification response content: %s", verification_response_content)

        api_ref = verification_response_content.get('api_ref')


        if not api_ref:
            # _logger.error("No api_ref found in the verification response.")
            raise ValidationError("IntaSend: " + _("No api_ref found in the verification response."))

    # Use api_ref to find the transaction
        tx = self.search([('reference', '=', api_ref), ('provider_code', '=', 'intasend')])
        if not tx:
            # _logger.error("No transaction found matching reference %s.", reference)
            raise ValidationError(
                "IntaSend: " + _("No transaction found matching reference %s.", reference)
            )

        return tx

    def _process_notification_data(self, notification_data):
        # _logger.info("Processing notification data: %s", pprint(self))
    #     _logger.info(
    #     "Processing Notification Data With Self:\n%s\nNotification Data:\n%s",
    #         pformat(self.read()[0]),
    #         pformat(notification_data)
    # )
        # Comment out or remove the next line to prevent execution
        super()._process_notification_data(notification_data)
        if self.provider_code != 'intasend':
            return

        reference = notification_data.get('tracking_id')
        signature = notification_data.get('signature')
        checkout_id = notification_data.get('checkout_id')
        
        payload = {
            'checkout_id': checkout_id,
            'signature': signature
        }

        intasend_provider = self.env['payment.provider'].search([('code', '=', 'intasend')], limit=1)
        if not intasend_provider:
            raise ValidationError(_("No IntaSend payment provider found."))
        response = intasend_provider._intasend_make_request('checkout/details', payload=payload)

        verification_response_content = response
        # _logger.info("Verification response content for api call 2: %s", verification_response_content)

        paid = verification_response_content.get('paid')

        if paid:
            self._set_done()
        else:
            # Handle cases where payment is not completed
            # _logger.warning(
            #     "Payment not completed for transaction with reference %s.",
            #     self.reference
            # )
            self._set_pending()

        
