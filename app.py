from backend import app, routes

app.register_blueprint(routes.index.bp)
app.register_blueprint(routes.login.bp)
app.register_blueprint(routes.data_process.bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0')