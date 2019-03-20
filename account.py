# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval

__all__ = ['InvoiceLine']


class InvoiceLine(metaclass=PoolMeta):
    __name__ = 'account.invoice.line'

    customer_shipments = fields.Function(fields.One2Many('stock.shipment.out',
            None, 'Customer Shipments', states={
                'invisible': Eval('invoice_type', '') != 'out',
                }),
        'get_customer_shipments', searcher='search_customer_shipments')
    customer_shipment_returns = fields.Function(fields.One2Many(
            'stock.shipment.out.return', None, 'Customer Shipment Returns',
            states={
                'invisible': Eval('invoice_type', '') != 'out',
                }),
        'get_customer_shipment_returns',
        searcher='search_customer_shipment_returns')
    supplier_shipments = fields.Function(fields.One2Many('stock.shipment.in',
            None, 'Supplier Shipments', states={
                'invisible': Eval('invoice_type', '') != 'in',
                }),
        'get_supplier_shipments', searcher='search_supplier_shipments')
    supplier_shipment_returns = fields.Function(fields.One2Many(
            'stock.shipment.in.return', None, 'Supplier Shipment Returns',
            states={
                'invisible': Eval('invoice_type', '') != 'in',
                }),
        'get_supplier_shipment_returns',
        searcher='search_supplier_shipment_returns')

    def get_shipments(model_name):
        '''
        Computes line's stock moves shipments
        '''
        def method(self, name):
            Model = Pool().get(model_name)
            shipments = set()
            for move in self.stock_moves:
                if isinstance(move.shipment, Model):
                    shipments.add(move.shipment.id)
            return list(shipments)
        return method

    get_customer_shipments = get_shipments('stock.shipment.out')
    get_customer_shipment_returns = get_shipments('stock.shipment.out.return')
    get_supplier_shipments = get_shipments('stock.shipment.in')
    get_supplier_shipment_returns = get_shipments('stock.shipment.in.return')

    def search_shipments(model_name):
        '''
        Search on shipments
        '''
        def method(self, name, clause):
            fieldname = 'stock_moves.shipment.'
            if '.' in clause[0]:
                fieldname += '.'.join(clause[0].split('.')[1:])
            else:
                fieldname += 'rec_name'
            return [
                (fieldname,) + tuple(clause[1:]) + (model_name,),
                ]
        return classmethod(method)

    search_customer_shipments = search_shipments('stock.shipment.out')
    search_customer_shipment_returns = search_shipments(
        'stock.shipment.out.return')
    search_supplier_shipments = search_shipments('stock.shipment.in')
    search_supplier_shipment_returns = search_shipments(
        'stock.shipment.in.return')
