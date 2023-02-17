from api.v1.inventory_management.queries.inventory_query import create_inventory_query
from api.v1.inventory_management.schema.inventory_schema import (
    GetInventoryResponse,
    InventoryGetResp,
)
from configuration.base_activity import ActivityBase
from configuration.constants import Common
from configuration.contexts import GenericContextBase
from numerize.numerize import numerize
from storage.db import DbManager


class GetInventory(ActivityBase):

    context_class: GenericContextBase = GenericContextBase

    def _execute(self):
        # initialize the database instance
        db = DbManager()

        # create queries using filter
        inventory_query = create_inventory_query(db.session(), self.context.filter)

        # paginate the query
        obj = db.paginate(
            inventory_query, self.context.page_number, self.context.page_limit
        )

        # curate the response
        response = GetInventoryResponse()
        count = obj.get(Common.COUNT.value)
        if count:
            response.count = count
            for val in obj.get(Common.DATA.value):
                response.items.append(
                    InventoryGetResp(
                        brand=val.brand,
                        additionalInfo=val.additionalInfo,
                        original_price=val.original_price,
                        discounted_price=val.discounted_price,
                        discount_percentage=val.discount_percentage,
                        rating=val.rating,
                        review_count=numerize(val.review_count),
                        out_of_stock=val.out_of_stock,
                    )
                )

        # respond
        return response
