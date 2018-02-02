from flask import Flask, request, render_template
import json
import sqlite3
import pandas as pd

conn = sqlite3.connect("db/pharm_data.db", check_same_thread=False)

global_vars = {
    "prc": None,
    "med_count": None
}

app = Flask(__name__)
app.config.update(dict(
    DEBUG=True,
))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    drug = request.args['dname'].encode('ascii','ignore')
    strength = request.args['dstrength'].encode('ascii','ignore')
    if strength != "empty":
        result = map(list,conn.execute("select * \
                              from RXCUI_DATA \
                              where (upper(PSN) like '%"+drug.upper()+"%' or \
                                    upper(BRAND_NAME) like '%"+drug.upper()+"%') and \
                                    upper(STRENGTH) like '%"+strength.upper()+"%' \
                              limit 10").fetchall())
    else:
        result = map(list,conn.execute("select * \
                              from RXCUI_DATA \
                              where upper(PSN) like '%"+drug.upper()+"%' or \
                                    upper(BRAND_NAME) like '%"+drug.upper()+"%' \
                              limit 10").fetchall())
    for i in range(len(result)):
        for j in range(len(result[i])):
            result[i][j] = result[i][j].encode('ascii','ignore')
    dropdown = '<div class="results"><select>'
    for i in result: dropdown += '<option value ="%s">%s</option>'%(i,i[3])
    dropdown += '</select></div>'
    return json.dumps({"results":dropdown})

@app.route("/pdp_region_code")
def get_region_code():
    text = request.args['searchCode']
    user_state = pd.read_sql("select COUNTY,STATENAME\
                          from ZIP_STATE_COUNTY\
                          where ZIPCODE is '" + text + "'", conn)\
            ['STATENAME'].values[0].rstrip()
    global_vars["prc"] = pd.read_sql("select distinct PDP_REGION_CODE\
                          from GEOGRAPHIC_LOCATOR\
                          where STATENAME is '"+user_state+"'",conn)\
             ['PDP_REGION_CODE'].values[0]

    return json.dumps({"results":global_vars["prc"]})

if __name__ == "__main__":
    app.run()
