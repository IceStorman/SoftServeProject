

class BaseDAL:
    def get_base_query(self, model):
        return self.session.query(model)

    def execute_query(self, query):
        return query.all()