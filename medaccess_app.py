from flask import Flask, request, render_template, g
import json
import sqlite3
import pandas as pd

DATABASE = '/var/www/html/medaccess/db/pharm_data.db'


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    DEBUG=True,
))

conn = sqlite3.connect(app.config['DATABASE'], check_same_thread=False)


global_vars = {
    "prc": None,
    "meds": []
}

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
                                    upper(STRENGTH) like '%"+strength.upper()+"%'\
                             limit 10").fetchall())
    else:
        result = map(list,conn.execute("select * \
                              from RXCUI_DATA \
                              where (upper(PSN) like '%"+drug.upper()+"%' or \
                                    upper(BRAND_NAME) like '%"+drug.upper()+"%') \
                              limit 10").fetchall())
    for i in range(len(result)):
        for j in range(len(result[i])):
            result[i][j] = result[i][j].encode('ascii','ignore')
    dropdown = '<div class="results"><select id="drug_list">'
    for i in result: dropdown += '<option value ="%s">%s</option>'%(i[0] if i[1]=='' else i[1],i[3])
    dropdown += '</select><button id="add_drug" type="button" onclick="add_drug();">SAVE</button></div>'
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

@app.route("/save_rxcui")
def save_rxcui():
    global_vars['meds'].append(request.args['rxcui'])
    return json.dumps({"status":"ok"})

@app.route("/formularies")
def send_formularies():
    out = pd.read_sql("select \
                    PLAN_INFO.CONTRACT_NAME, \
                    PLAN_INFO.PLAN_NAME, \
                    PLAN_INFO.CONTRACT_ID, \
                    PLAN_INFO.PLAN_ID, \
                    PLAN_INFO.SEGMENT_ID, \
                    PLAN_INFO.FORMULARY_ID, \
                    PLAN_INFO.PREMIUM, \
                    PLAN_INFO.DEDUCTIBLE \
            from \
                FORMULARY_DATA join PLAN_INFO \
                on substr(FORMULARY_DATA.FORMULARY_ID, 4) = PLAN_INFO.FORMULARY_ID \
            where \
                  PLAN_INFO.PDP_REGION_CODE is '"+str(global_vars['prc'])+"' and \
                  PLAN_INFO.CONTRACT_ID like 'S%'\
            order by PLAN_INFO.FORMULARY_ID",conn)\
    .drop_duplicates(subset='FORMULARY_ID',keep='first')\
    .reset_index(drop=True)
    for med in global_vars['meds']:
            out = pd.concat([out,
               pd.read_sql(" ".join(("select \
                        PLAN_INFO.CONTRACT_NAME, \
                        PLAN_INFO.PLAN_NAME, \
                        PLAN_INFO.CONTRACT_ID, \
                        PLAN_INFO.PLAN_ID, \
                        PLAN_INFO.SEGMENT_ID, \
                        PLAN_INFO.FORMULARY_ID, \
                        PLAN_INFO.PREMIUM, \
                        PLAN_INFO.DEDUCTIBLE, \
                        FORMULARY_DATA.RXCUI as MED_"+med+", \
                        FORMULARY_DATA.PRIOR_AUTHORIZATION_YN as PA_"+med+", \
                        FORMULARY_DATA.TIER_LEVEL_VALUE as TIER_"+med+", \
                        BENEFICIARY_COST.COST_AMT_PREF as CAP_"+med+" \
                from \
                    FORMULARY_DATA join PLAN_INFO \
                        on substr(FORMULARY_DATA.FORMULARY_ID, 4) = PLAN_INFO.FORMULARY_ID \
                    join BENEFICIARY_COST \
                        on PLAN_INFO.CONTRACT_ID = BENEFICIARY_COST.CONTRACT_ID and \
                           PLAN_INFO.PLAN_ID = BENEFICIARY_COST.PLAN_ID and \
                           cast(FORMULARY_DATA.TIER_LEVEL_VALUE as integer) = \
                                                    cast(BENEFICIARY_COST.TIER as integer) \
                where \
                      PLAN_INFO.PDP_REGION_CODE is '"+str(global_vars['prc'])+"' and \
                      FORMULARY_DATA.RXCUI like '%"+med+"' and \
                      PLAN_INFO.CONTRACT_ID like 'S%' and \
                      (cast(BENEFICIARY_COST.COVERAGE_LEVEL as integer) = 0 or \
                      cast(BENEFICIARY_COST.COVERAGE_LEVEL as integer) = 1) and \
                      BENEFICIARY_COST.DAYS_SUPPLY = 1 and \
                      cast(BENEFICIARY_COST.COST_TYPE_PREF as integer) = 1\
                order by PLAN_INFO.FORMULARY_ID").split()),conn)\
            .drop_duplicates(subset='FORMULARY_ID',keep='first')\
            .reset_index(drop=True)\
            [['MED_'+med,
              'PA_'+med,
              'TIER_'+med,
              'CAP_'+med]]],axis=1)
    #ADD IN COST COLUMN
            if 'ANNUAL_TOTAL_COST' in out.columns:
                del out['ANNUAL_TOTAL_COST']
            if 'MONTHLY_COPAY' in out.columns:
                del out['MONTHLY_COPAY']
            out['ANNUAL_TOTAL_COST'] = (out[[c for c in out.columns if c[:3] == 'CAP']]*12).sum(axis=1) + out['PREMIUM']*12 + out['DEDUCTIBLE']
            out['MONTHLY_COPAY'] = out[[c for c in out.columns if c[:3] == 'CAP']].sum(axis=1)
            out = out.sort_values(by='ANNUAL_TOTAL_COST').reset_index(drop=True)
    return json.dumps({"results":out.to_html()})



if __name__ == "__main__":
    app.run()
