

class BaseDAL:
    def get_query(self, model):
        return self.session.query(model)

    def execute_query(self, query):
        return query.all()