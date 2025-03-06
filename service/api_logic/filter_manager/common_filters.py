from sqlalchemy.orm import Query

class CommonFilters():

    def apply_order_by(self, query: Query, model, order, field) -> Query:
        return query.order_by(order(getattr(model, field)))