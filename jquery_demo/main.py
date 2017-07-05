from flask import Flask, render_template, redirect
from flask_wtf.csrf import CSRFProtect
from flask import request
import json

app = Flask(__name__)
csrf = CSRFProtect(app)


data = json.load(open("static/data.json"))
wastes_data = json.load(open("static/wastes.json"))


@app.route('/', methods=['GET'])
def submit():
    rec_ids = None
    result = {"res": None}
    if request.query_string:
        s = str(request.query_string)
        print(s)
        ids = s.split('&')
        if ids:
            for rec_id in ids:
                if 'id' == rec_id[:2]:
                    row_id = (rec_id.split('=')[1])
                    row_id = row_id.replace("'", "")
                    row_id = int(row_id)
                    if not rec_ids:
                        rec_ids = [row_id]
                    else:
                        rec_ids.append(row_id)
            res = []
            if rec_ids:
                s = 0.0
                for rec_id in rec_ids:
                    idx = rec_id - 1
                    waste = wastes_data[idx]
                    s += float(waste)
                    r = [waste] + data['data'][idx][1:]
                    res.append(r)
                result = {"res": res, "total": "{0:.2f}".format(s)}
    return render_template('page.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    # app.run(port=5555, debug=True)