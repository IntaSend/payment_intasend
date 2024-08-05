# Intasend Payment Provider for Odoo

## Overview

This module integrates Intasend, a Kenyan-based online payment provider, with Odoo. It allows merchants to facilitate payments worldwide through their Odoo-powered e-commerce platforms.

## Features

- Seamless integration with Odoo's payment system
- Secure handling of transactions
- Support for multiple currencies
- Easy configuration through Odoo's admin interface

## Requirements

- Odoo 17.0 or later
- An active Intasend account

# Intasend Odoo Integration

## Introduction

Intasend is an online payments provider based in Kenya that enables merchants to facilitate payments worldwide. This guide will walk you through the process of integrating Intasend with your Odoo platform.

## 1. Intasend Dashboard Configuration

1. Log into the [Intasend Dashboard](https://payment.intasend.com).
2. Navigate to the [Integrations](https://payment.intasend.com/account/api-keys/) page.
3. Locate and copy the values of the Public Key and Secret Key fields.
4. Store these keys securely, as you may not be able to access them later.

![Intasend Dashboard](<docs/Screenshot from 2024-08-01 16-33-57.png>)

## 2. Odoo Configuration (Self-Hosted)

1. Locate the `addons` folder in the root directory of your Odoo project.
2. Add the `payment_intasend` folder to the `addons` directory.

![Odoo Addons Folder](<docs/Screenshot from 2024-08-01 16-42-29.png>)


3. Restart the Odoo service to apply the changes:

```bash
systemctl restart odoo17
```
## 3. Activating Intasend in Odoo

1. Log into your Odoo platform.
2. Go to the Apps menu and search for "Intasend".

![Activate Intasend In Odoo](<docs/Screenshot from 2024-08-01 16-58-45.png>)

3. Activate the payment_intasend app.

## 4. Configuring Intasend for Your Site

1. Navigate to the site where you want to configure Intasend.
2. In the configuration options, click on "Payment Providers".

![Intasend Configuration](<docs/Screenshot from 2024-08-02 13-06-22.png>)

3. Find Intasend in the list and click "Activate".

![Activate Intasend](<docs/Screenshot from 2024-08-02 13-09-47.png>)

4. On the Intasend configuration page:

    * Enter the Public Key, Secret Key, and Webhook Key.
    * Toggle the state to "Enabled".
    * Click the "Save" button in the top left corner.

![Enter Intasend Credentials](<docs/Screenshot from 2024-08-02 13-15-23.png>)


## Conclusion
You have now successfully integrated Intasend with your Odoo platform. This will allow you to process payments through Intasend on your Odoo-powered website.
For any issues or further assistance, please consult the Intasend documentation or contact our support team.


## Support

For issues related to this module, please open an issue on this repository.

For Intasend-specific issues, please contact [Intasend Support](https://support.intasend.com).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- Intasend for providing the payment gateway services.
- The Odoo community for their continuous support and contributions.