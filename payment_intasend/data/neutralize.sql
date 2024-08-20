-- disable intasend payment provider
UPDATE payment_provider
   SET intasend_public_key = NULL,
       intasend_secret_key = NULL,
       intasend_webhook_secret = NULL;
