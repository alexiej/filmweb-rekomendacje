from server import app
import sys

if __name__ == '__main__':
    debug = False
    if "debug" in sys.argv:
        print("TURN ON DEBUG")
        debug = True
    app.run(debug=debug, use_reloader=True, host='0.0.0.0',port=80)
