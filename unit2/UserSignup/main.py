# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
import cgi
import codecs
import re

form = """
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

<form method = "post">
<h1>Signup</h1>

<div class="container-fluid">
    <div class="row">
        <div class="col-xs-3 text-right">
            Username
        </div>
        <div class="col-xs-4">
            <input type = "text" name="username" value="%(username)s"></input>
        </div>
        <div class="col-xs-5 text-left" style="color: red">
            %(username_error)s
        </div>
    </div>
    <div class="row">
        <div class="col-xs-3 text-right">
            Password
        </div>
        <div class="col-xs-4">
            <input type = "password" name="password"></input>
        </div>
        <div class="col-xs-5 text-left" style="color: red">
            %(password_error)s
        </div>
    </div>
    <div class="row">
        <div class="col-xs-3 text-right">
            Verify Password
        </div>
        <div class="col-xs-4">
            <input type = "password" name="verify"></input>
        </div>
        <div class="col-xs-5 text-left" style="color: red">
            %(verify_error)s
        </div>
    </div>
    <div class="row">
        <div class="col-xs-3 text-right">
            Email (optional)
        </div>
        <div class="col-xs-4">
            <input type = "text" name="email" value="%(email)s"></input>
        </div>
        <div class="col-xs-5 text-left" style="color: red">
            %(email_error)s
        </div>
    </div>
</div>

<br>
<input type = "submit">
</form>
"""

def escape_html(s):
    return cgi.escape(s, quote = True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username) and username

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return PASS_RE.match(password) and password

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return EMAIL_RE.match(email) or not email

class MainPage(webapp2.RequestHandler):
    def write_form(self, username = '', email = '', username_error = '', password_error = '', verify_error = '', email_error = ''):
        self.response.write(form % {"username": escape_html(username)
                ,"email": escape_html(email)
                ,"username_error": username_error
                ,"password_error": password_error
                ,"verify_error": verify_error
                ,"email_error": email_error
                })

    def get(self):
        self.write_form()

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        v_username = valid_username(username)
        v_password = valid_password(password)
        v_email = valid_email(email) or email == ''
        verified = password == verify

        if v_username and v_password and v_email and verified:
            self.redirect("/unit2/welcome?username=" + username)
        else:
            username_error = ''
            password_error = ''
            email_error = ''
            verify_error = ''
            if v_username is None: username_error = "That's not a valid username."
            if v_password is None: password_error = "That wasn't a valid password."
            if not v_email: email_error = "That's not a valid email"
            if not verified: verify_error = "Your passwords didn't match"
            self.write_form(username = username, email = email, 
                username_error = username_error, password_error = password_error, 
                verify_error = verify_error, email_error = email_error)

class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.response.write("<h1>Welcome, " + username + "</h1>")
        else:
            self.redirect("/unit2/signup")

app = webapp2.WSGIApplication([
    ('/unit2/signup', MainPage),
    ('/unit2/welcome', Welcome),
], debug=True)