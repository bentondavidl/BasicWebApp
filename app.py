from backend import app, routes

app.register_blueprint(routes.index.bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0')