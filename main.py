from flask import Flask, render_template, redirect


app = Flask(__name__)


def main():
    app.run()


@app.route('/')
def index():
    return render_template('base.html')


if __name__ == '__main__':
    main()
