# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import account


def register():
    Pool.register(
        account.InvoiceLine,
        module='account_invoice_line_search_by_shipment', type_='model')
