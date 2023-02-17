from sqlalchemy import and_
from storage.db_models import MenTshirt


def create_inventory_query(session, filter):
    and_conditions = []
    if filter.get("brand"):
        and_conditions.append(MenTshirt.brand.in_(filter.get("brand", [])))
    if filter.get("rating"):
        and_conditions.append(
            MenTshirt.rating >= filter.get("rating", 0),
        )
    if filter.get("review_count"):
        and_conditions.append(
            MenTshirt.review_count >= filter.get("review_count", 0),
        )
    and_conditions.append(
        MenTshirt.out_of_stock == filter.get("out_of_stock", False),
    )
    return session.query(
        MenTshirt.brand,
        MenTshirt.additionalInfo,
        MenTshirt.original_price,
        MenTshirt.discounted_price,
        MenTshirt.discount_percentage,
        MenTshirt.rating,
        MenTshirt.review_count,
        MenTshirt.out_of_stock,
    ).filter(and_(*and_conditions))
