from api.v1.inventory_management.controller.inventory import Inventory
from configuration.constants import Common
from flask import Blueprint
from flask_restful import Api

api_v1_bp = Blueprint(
    f"api_v{Common.VERSION.value}", __name__, url_prefix=f"/api/v{Common.VERSION.value}"
)
api_v1 = Api(api_v1_bp)


# inventory
api_v1.add_resource(Inventory, "/search/men-tshirts")
