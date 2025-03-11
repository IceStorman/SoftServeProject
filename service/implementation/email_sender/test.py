from api.routes.__init__ import app

def test():
    with app.app_context():
        from api.container.container import Container
        subscription_manager = Container.email_manager()
        subscription_manager.try_add_subscribers_to_temp_table(1)

test()