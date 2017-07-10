import locale
from flask import Flask, render_template, redirect
from flask_wtf.csrf import CSRFProtect
from flask import request
import json

app = Flask(__name__)
csrf = CSRFProtect(app)


data = json.load(open("static/data.json"))
wastes_data = json.load(open("static/wastes.json"))
provider_data = json.load(open("static/providers.json"))

def price_to_int(v):
    return int(v[1:].replace(',', ''))


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
                s = 0
                d = {}
                for rec_id in rec_ids:
                    idx = rec_id - 1
                    rank = int(wastes_data[idx][0])
                    savings = wastes_data[idx][1]
                    # s += float(rank)
                    d[rank] = data['data'][idx][1:] + [savings]
                for k in sorted(d.keys()):
                    v = d[k][:-1] + [price_to_int(d[k][-1])]
                    r = [k] + v
                    s += v[-1]
                    res.append(r)
                res2 = []
                percent_cum = 0
                locale.setlocale(locale.LC_ALL, '')
                for r in res:
                    percent = r[-1]/s * 100
                    percent_cum += percent
                    r[-1] = locale.currency(int(r[-1]), grouping=True)
                    r[-1] = "{}".format(r[-1][:-3])
                    res2.append(r + ["{0:.1f}".format(percent), "{0:.1f}".format(percent_cum)])
                s = locale.currency(s, grouping=True)
                result = {"res": res2, "total": "{0}".format(s[:-3])}
            result["prov"] = provider_data
    return render_template('page.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    # app.run(port=5555, debug=True)