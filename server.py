from server import app
import sys

def application(environ, start_response):
    return app(environ,start_response)

if __name__ == '__main__':
    debug = False
    if "debug" in sys.argv:
        print("TURN ON DEBUG")
        debug = True
    app.run(debug=debug, use_reloader=True, host='0.0.0.0',port=80)
