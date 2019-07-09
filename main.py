from flask import Flask, render_template

app = Flask(__name__)

debug = True

if debug:
    import population
    population.main()

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
