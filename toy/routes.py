# from .controllers.example_controllers import example_bp
#
# def routes_list(app):
#     app.register_blueprint(example_bp)
#     return app


def routes_list(api):
    # namespace
    from toy.controllers.example_controllers import example_ns
    from toy.controllers.sign_controller import sign_ns
    api.add_namespace(example_ns)
    api.add_namespace(sign_ns)

