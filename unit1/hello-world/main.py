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

form = """
<form method = "post">
What is your birthday?
<br>
<label>
    Month
    <input type = "text" name = "month" value = %(month)s>
</label>
<label>
    Day
    <input type = "text" name = "day">
</label>
<label>
    Year
    <input type = "text" name = "year">
</label>
<div style = 'color: red'>%(error)s</div>
<br>
<input type = "submit">
</form>
"""

def valid_month(month):
	if month.isdigit() and int(month) in range(1,32):
		return int(month)
	else:
		return None

def escape_html(s):
	return cgi.escape(s, quote = True)

class MainPage(webapp2.RequestHandler):
    def write_form(self, error = '', month = ''):
    	self.response.write(form % {"error": error, 
    								"month": escape_html(month)})

    def get(self):
        self.write_form()

    def post(self):
        user_month = self.request.get('month')
        month = valid_month(user_month)

        if not month:
        	self.write_form(error = 'Sorry - not a valid month...', month = user_month)
        else:
        	self.redirect("/thanks")

class Thanks(webapp2.RequestHandler):
	def get(self):
		self.response.write('Thanks!')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/thanks', Thanks),
], debug=True)
