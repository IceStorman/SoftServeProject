

class BaseDAL:
    def get_base_query(self, model):
        return self.session.query(model)

    def query_output(self, query):
        return query.all()