.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
    :alt: License LGPL-3

====================
Purchase Order Block
====================

This module allows you to block the validation of a Purchase Order providing a
block reason.


Configuration
=============

* Go to ‘Purchases / Configuration / Purchase Block Reasons’ and create the
  blocking reasons as needed, providing a name and a description. A field
  ‘Active’ allows you to deactivate the reason if you do not plan to use it
  any more.
* Assign the security group “Release blocked RFQ” to users that should be able
  to release the block.


Usage
=====

Set the purchase block
----------------------
# Go to ‘Purchases / Purchase / Requests for Quotation’
# Create a new RFQ and indicate the blocking reason (found in the right hand
  side of the screen, below the order date). Upon save, the blocking is not
  editable anymore, and a notification has been logged into the chatter,
  indicating ‘Order blocked with reason xyz’, so that all followers can receive
  it.

Search existing RFQ
-------------------
There is a filter ‘Blocked’ to search for orders that are blocked.
It is also possible to search RFQ’s with a specific block reason.

Release the purchase block
--------------------------
# Access to an existing RFQ that is blocked.
# If your user is member of security group ‘Release blocked RFQ’, she/he will
  see a button ‘Release block’. When pressing it a notification will be sent
  to all the followers again, with message ‘Order with block xyz has now been
  released’.
# From this point and on, anyone seeing that RFQ will be able to validate it.

Validate the RFQ
----------------
# Press the button ‘Validate’. If there’s a block, and you do not have
  permissions, you will get an error message indicating that the RFQ is
  blocked, and the reason. You will need to request it to be released by an
  authorized user.


Technical notes
===============

See Sale Delivery Block as an example:
https://github.com/OCA/sale-workflow/tree/9.0/sale_delivery_block


.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/142/10.0


Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/purchase-workflow/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.


Credits
=======

Contributors
------------

* Jordi Ballester Alomar <jordi.ballester@eficent.com>
* Roser Garcia <roser.garcia@eficent.com>
* Darshan Patel <darshan.patel.serpentcs@gmail.com>


Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
