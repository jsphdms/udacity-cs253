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

form = """
<form method = "post">
<h1>Enter some text to ROT13:</h1>

<textarea rows="4" cols="50" name = "text">%(text)s</textarea>

<br>
<input type = "submit">
</form>
"""

def escape_html(s):
    return cgi.escape(s, quote = True)

def rot13(s):
    return codecs.encode(s, 'rot_13')

class MainPage(webapp2.RequestHandler):
    def write_form(self, text = ''):
        self.response.write(form % {"text": escape_html(text)})

    def get(self):
        self.write_form()

    def post(self):
        user_text = self.request.get('text')
        text = rot13(user_text)
        self.write_form(text = text)

app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)