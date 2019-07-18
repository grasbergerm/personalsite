from flask import Flask, request, render_template
from urllib.parse import quote_plus

app = Flask(__name__, static_url_path='', static_folder='')
app.jinja_env.filters['quote_plus'] = lambda u: quote_plus(u)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/blogs")
def blogs():
	return render_template('blogs.html')

@app.route("/blog")
def blog():
	google_doc_iframe = generate_iframe(request.args.get('doc_string', ''))
	return render_template('blog.html', google_doc=google_doc_iframe)

def generate_iframe(google_doc_url):
	return '<iframe id="google-doc" src="https://docs.google.com/{}" frameborder="0"></iframe>'.format(google_doc_url)

if __name__ == "__main__":
    app.run()
