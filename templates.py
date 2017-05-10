import os
import re
import codecs
import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape = True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class MainPage(Handler):
	def get(self):
		items = self.request.get_all("food")
		self.render("shopping_list.html", items = items)

class FizzBuzz(Handler):
	def get(self):
		n = self.request.get('n', 0)
		n = n and int(n)
		self.render('fizzbuzz.html', n = n)

class ROT13(Handler):
	def get(self):
		self.render("rot13.html")

	def post(self):
		rot13 = ''
		text = self.request.get('text')
		if text:
			rot13 = text.encode('rot13')

		self.render("rot13.html",text = rot13)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
	return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
	return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r'^[\S]+@[\S]+.[\S]+$')
def valid_email(email):
	return not email or EMAIL_RE.match(email)

class SignUp(Handler):
	def get(self):
		self.render("signup.html")

	def post(self):
		has_error = False
		username = self.request.get('username')
		password = self.request.get('password')
		verify = self.request.get('verify')
		email = self.request.get('email')

		params = dict(username = username,
						email = email)

		if not valid_username(username):
			params['error_username'] = "Be a good chap and enter a valid username!"
			has_error = True

		if not valid_password(password):
			params['error_password'] = "Be a good chap and enter a valid password!"
			has_error = True
		elif password != verify:
			params['error_verify'] = "Make 'em match!"
			has_error = True

		if not valid_username(email):
			params['error_email'] = "Be a good chap and enter a valid email address!"
			has_error = True

		if has_error:
			self.render('signup.html', **params)
		else:
			self.redirect('welcome.html' + username)

class Welcome(Handler):
	def get(self):
		username = self.request.get('username')
		if valid_username(username):
			self.render('welcome.html', username = username)
		else:
			self.redirect('/signup')

app = webapp2.WSGIApplication([('/', MainPage),
								('/fizzbuzz', FizzBuzz),
								('/rot13', ROT13),
								('/signup', SignUp),
								('/welcome', Welcome)
								],
								debug=True)