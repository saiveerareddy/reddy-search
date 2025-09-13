# web_app.py
from flask import Flask, render_template_string, request, jsonify
import asyncio
from main import run_ip, run_email, run_phone, run_name

app = Flask(__name__)

TEMPLATE = """
<!doctype html>
<title>Reddy Search</title>
<h1>Reddy Search</h1>
<form method="post">
  <label>Type:
    <select name="type">
      <option value="ip">IP</option>
      <option value="email">Email</option>
      <option value="phone">Phone</option>
      <option value="name">Full name</option>
    </select>
  </label><br>
  <input name="value" placeholder="value" style="width:400px" required><br><br>
  <button type="submit">Search</button>
</form>
{% if result %}
<hr>
<h2>Result (summary)</h2>
<pre>{{result | tojson(indent=2)}}</pre>
{% endif %}
"""

@app.route("/", methods=["GET","POST"])
def index():
    result = None
    if request.method == "POST":
        t = request.form["type"]
        v = request.form["value"]
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        if t == "ip":
            res = loop.run_until_complete(run_ip(v))
        elif t == "email":
            res = loop.run_until_complete(run_email(v))
        elif t == "phone":
            res = loop.run_until_complete(run_phone(v))
        else:
            res = loop.run_until_complete(run_name(v))
        result = res
    return render_template_string(TEMPLATE, result=result)

if __name__ == "__main__":
    app.run(debug=True)
