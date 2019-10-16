# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

from flask import Flask, render_template, request
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler

from flask_wtf import csrf

from forms import *
from forms import LoginForm, RegisterForm, AssetForm, PortfolioForm, AssetBaseForm, CompareAssetForm, \
    PramsTxMatrixInputForm

# from application import app,db
import numpy as np
from flask import render_template, json, request, Response, redirect, flash, url_for
from wtforms import Form, FormField, FieldList
import io, random
import json
from bokeh.client import pull_session
from bokeh.embed import components, server_session
from bokeh.embed import json_item, server_document, server_session, server
from bokeh.plotting import figure
from bokeh.resources import CDN
# from bokeh.sampledata.iris import flowers

from flask import Flask
from jinja2 import Template

# from holoviews.operation.timeseries import rolling, rolling_outlier_std
from financeLib.Portfolio import Portfolio
from financeLib.Asset import Asset
from analysis import getFinalDistribution, getCompareFinalDistribution
import os
import subprocess
import atexit
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect, CSRF
from localBokeh.transition_graphviz import generate_digraph

app = Flask(__name__)
app.config.from_object('config')
Bootstrap(app)
csrf = CSRFProtect(app)
# db = SQLAlchemy(app)
# bokeh_process = subprocess.Popen(['python', '-m', 'bokeh',
#                                   'serve', 'localBokeh', '--port 5050', '--allow-websocket-origin=localhost:5000',
#                                   ], stdout=subprocess.PIPE)

# bokeh serve bokeh_server.py --allow-websocket-origin=127.0.0.1:5000

# ----------------------------------------------------------------------------#
# starting bokeh server as a subprocess.
# ----------------------------------------------------------------------------#

# bokeh_process = subprocess.Popen(['python', '-m', 'bokeh',
#                                   'serve', 'bokehchartapp.py', '--port 5050', ], stdout=subprocess.PIPE)
#
# @atexit.register
# def kill_server():
#     bokeh_process.kill()
#

# Automatically tear down SQLAlchemy.bokehchartapp
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''


# ----------------------------------------------------------------------------#
# Helpers.
# ----------------------------------------------------------------------------#

# def make_plot(x, y):
#     colormap = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
#     colors = [colormap[x] for x in flowers['species']]
#     p = figure(title = "Iris Morphology", sizing_mode="fixed", plot_width=400, plot_height=400)
#     p.xaxis.axis_label = x
#     p.yaxis.axis_label = y
#     p.circle(flowers[x], flowers[y], color=colors, fill_alpha=0.2, size=10)
#     return p


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/index', methods=["GET", "POST"])
@app.route('/', methods=["GET", "POST"])
def home():
    form = AssetForm()
    # if request.method == 'POST' and form.validate_on_submit():
    if request.method == 'POST':
        # [('Distribution', 'exponential'), ('assetName', 'aa'), ('entryVal', '100'), ('ownPercent', '0.2'),
        #  ('periodYears', '10'), ('growthRate', '0.25'), ('sigma', ''), ('samples', '100'), ('submit', '')]
        modelData = dict(
            dist=request.form.get('Distribution'),
            assetName=request.form.get('assetName'),
            entryVal=float(request.form.get('entryVal')),
            ownPercent=float(request.form.get('ownPercent')),
            periodYears=int(request.form.get('periodYears')),
            growthRate=float(request.form.get('growthRate')),
            sigma=float(request.form.get('sigma') if request.form.get('sigma') != '' else 0),
            samples=int(request.form.get('samples')),
        )
        chart = getFinalDistribution(modelData)
        script, div = components(chart)
        return render_template("pages/Asset.html", form=form, script=script, div=div, asset=True)
        # print(30 * "=")
        # print(modelData)
        # print(30 * "=")

    return render_template('pages/Asset.html', asset=True, form=form)
    # return render_template('pages/Asset.html')


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)


@app.route("/portfolio", methods=["GET", "POST"])
def portfolio():
    form = PortfolioForm()

    if request.method == 'POST':
        num_assets = int(request.form.get('num_assets'))
        num_samples = int(request.form.get('num_samples'))
        portfolioName = request.form.get('portfolioName')
        dist = request.form.get('dist')
        return redirect(url_for('portfolioAssets', num_assets=num_assets, dist=dist,
                                num_samples=num_samples, portfolioName=portfolioName))

    return render_template('pages/Portfolio.html', form=form, portfolio=True)

@app.route("/PortfolioAssets", methods=['GET', 'POST'])
@app.route("/PortfolioAssets/<int:num_assets>", methods=['GET', 'POST'])
def portfolioAssets(num_assets=1):
    print(num_assets)
    num_assets = request.args.get('num_assets')
    dist = request.args.get('dist')
    num_samples = request.args.get('num_samples')
    portfolioName = request.args.get('portfolioName')
    form = FieldList(FormField(AssetBaseForm), min_entries=num_assets, max_entries=num_assets)

    print(request.args)
    return render_template("pages/portfolioAssets.html", index=False, num_assets=num_assets, form=form)

@app.route("/PramAnalysis", methods=['GET', 'POST'])
@app.route("/pram", methods=['GET', 'POST'])
def pram_analysis():
    form = PramsTxMatrixInputForm();
    if request.method == "POST":
        print(request.form)
        txMatrix_dict = dict(
            initial_population=request.form.get('initial_population'),
            round_seed_a=request.form.get('round_seed_a'),
            round_seed_failure=request.form.get('round_seed_failure'),
            round_a_b=request.form.get('round_a_b'),
            round_a_failure=request.form.get('round_a_failure'),
            round_b_c=request.form.get('round_b_c'),
            round_b_failure=request.form.get('round_b_failure'),
            round_c_success=request.form.get('round_c_success'),
            round_c_failure=request.form.get('round_c_failure'),
            round_success_success=request.form.get('round_success_success'),
            round_success_failure=request.form.get('round_success_failure'),
            round_failure_success=request.form.get('round_failure_success'),
            round_failure_failure=request.form.get('round_failure_failure'),
        )
        print(txMatrix_dict)
        #  Here we work on simulation:
        print("Working on simulation here")
        bokeh_script = server_document(url="http://localhost:5006/main", arguments=txMatrix_dict)
        return render_template("pages/PramAnalysis.html", form=form, bokeh_script = bokeh_script)

    return render_template("pages/PramAnalysis.html", form=form)

@app.route("/PramExitValuation", methods=['GET', 'POST'])
@app.route("/pramexitval", methods=['GET', 'POST'])
@csrf.exempt
def pram_exit_valuation_analysis():
    print("Working on simulation here")
    bokeh_script = server_document(url="http://localhost:5006/pram_startup")
    return render_template('pages/pramExitVal.html', bokeh_script=bokeh_script)


@app.route("/asset", methods=["GET", "POST"])
def asset():
    form = AssetForm()
    # if request.method == 'POST' and form.validate_on_submit():
    if request.method == 'POST':
        # [('Distribution', 'exponential'), ('assetName', 'aa'), ('entryVal', '100'), ('ownPercent', '0.2'),
        #  ('periodYears', '10'), ('growthRate', '0.25'), ('sigma', ''), ('samples', '100'), ('submit', '')]
        modelData = dict(
            dist=request.form.get('Distribution'),
            assetName=request.form.get('assetName'),
            entryVal=float(request.form.get('entryVal')),
            ownPercent=float(request.form.get('ownPercent')),
            periodYears=int(request.form.get('periodYears')),
            growthRate=float(request.form.get('growthRate')),
            sigma=float(request.form.get('sigma') if request.form.get('sigma') != '' else 0),
            samples=int(request.form.get('samples')),
        )
        chart = getFinalDistribution(modelData)
        script, div = components(chart)
        return render_template("pages/Asset.html", form=form, script1=script, div=div, asset=True)
        # print(30 * "=")
        # print(modelData)
        # print(30 * "=")

    return render_template('pages/Asset.html', asset=True, form=form)

@app.route("/viewAssetDistribution")
def viewAssetDistribution():
    return render_template('pages/viewAssetDistribution.html', chart=True)

@app.route('/comparepram', methods=['GET','POST'])
@csrf.exempt
def compare_pram():
    print("Working on simulation here")
    bokeh_script = server_document(url="http://localhost:5006/compare")
    return render_template("pages/compareExitVal.html", bokeh_script=bokeh_script)

@app.route("/compare", methods=["GET", "POST"])
def compare():
    form = CompareAssetForm()
    if request.method == 'POST':
        print(request.form)
        modelData = dict(
            a_dist=request.form.get('a_dist'),
            a_assetName=request.form.get('a_assetName'),
            a_entryVal=float(request.form.get('a_entryVal')),
            a_ownPercent=float(request.form.get('a_ownPercent')),
            a_periodYears=int(request.form.get('a_periodYears')),
            a_growthRate=float(request.form.get('a_growthRate')),
            a_sigma=float(request.form.get('a_sigma') if request.form.get('a_sigma') != '' else 0),
            b_dist=request.form.get('b_dist'),
            b_assetName=request.form.get('b_assetName'),
            b_entryVal=float(request.form.get('b_entryVal')),
            b_ownPercent=float(request.form.get('b_ownPercent')),
            b_periodYears=int(request.form.get('b_periodYears')),
            b_growthRate=float(request.form.get('b_growthRate')),
            b_sigma=float(request.form.get('b_sigma') if request.form.get('a_sigma') != '' else 0),
            samples=int(request.form.get('samples')),
        )
        print(modelData)
        chart, stats = getCompareFinalDistribution(modelData)
        a_script, div = components(chart)
        print(stats)
        return render_template("pages/compare.html", form=form, script=a_script, div=div, asset=True, stats=stats)
        # print(30 * "=")

    #     num_assets = int(request.form.get('num_assets'))
    #     num_samples = int(request.form.get('num_samples'))
    #     portfolioName = request.form.get('portfolioName')
    #     dist = request.form.get('dist')
    #     return redirect(url_for('portfolioAssets', num_assets=num_assets, dist=dist,
    #                             num_samples=num_samples, portfolioName=portfolioName))

    return render_template('pages/compare.html', form=form, portfolio=True, stats=False)
    # return render_template("pages/compare.html", form=form, script=script, div=div, asset=True)
    # print(30 * "=")
    # print(modelData)
    # print(30 * "=")

    # return render_template('pages/compare.html', asset=True, form=form)
    # return render_template('pages/compare.html')

# Test Page for Proof of Concept

@app.route("/test", methods=["POST","GET"])
def test():
    chart = generate_digraph()
    return render_template("pages/test.html", chart = chart)

    # if request.method == 'POST':
    #     print(request.form)
    #     return render_template("pages/test.html",form = form)

# Error handlers.

@app.errorhandler(500)
def internal_error(error):
    # db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')





# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

# ----------------------------------------------------------------------------#
# Trash.
# ----------------------------------------------------------------------------#



# @app.route("/api/")
# @app.route("/api/<idx>")
# def api(idx=None):
#     if idx == None:
#         jdata = data
#     else:
#         jdata = data[int(idx)]
#     return Response(json.dumps(jdata),mimetype="application/json")

#
# @app.route("/compare")
# def compare():
#     # pull a new session from a running Bokeh server
#     with pull_session(url="http://localhost:5006/sliders") as session:
#
#         # update or customize that session
#         # session.document.roots[0].children[1].title.text = "Special Sliders For A Specific User!"
#
#         # generate a script to load the customized session
#         script = server_session(session_id=session.id, url='http://localhost:5006/sliders')
#
#         # session2 = pull_session(url="http://localhost:5007/dash")
#         # script2 = server_session(session_id=session2.id, url="http://localhost:5007/dash")
#         # script2 = script2,
#
#         # use the script in the rendered page
#         return render_template("pages/compare.html", script=script, template="Flask")
#     return render_template('pages/compare.html')

#
# txMatrix_dict = dict(
#             initial_population=float(request.form.get('initial_population')),
#             round_seed_a=float(request.form.get('round_seed_a')),
#             round_seed_failure=float(request.form.get('round_seed_failure')),
#             round_a_b=float(request.form.get('round_a_b')),
#             round_a_failure=float(request.form.get('round_a_failure')),
#             round_b_c=float(request.form.get('round_b_c')),
#             round_b_failure=float(request.form.get('round_b_failure')),
#             round_c_success=float(request.form.get('round_c_success')),
#             round_c_failure=float(request.form.get('round_c_failure')),
#             round_success_success=float(request.form.get('round_success_success')),
#             round_success_failure=float(request.form.get('round_success_failure')),
#             round_failure_success=float(request.form.get('round_failure_success')),
#             round_failure_failure=float(request.form.get('round_failure_failure')),
#         )


# @app.route("/PramExitValuation", methods=['GET', 'POST'])
# @app.route("/pramexitval", methods=['GET', 'POST'])
# @csrf.exempt
# def pram_exit_valuation_analysis():
#     form = PramsTxMatrixInputFormLarge()
#
#     if not form.validate_on_submit():
#         print("Form invalid")
#
#         return render_template("pages/exitval.html", form=form)
#
#
#     if request.method == "POST":
#         print(request.form)
#         txMatrix_dict = dict(
#             initial_population=request.form.get('initial_population'),
#             round_seed_a=request.form.get('round_seed_a'),
#             round_seed_failure=request.form.get('round_seed_failure'),
#             round_a_b=request.form.get('round_a_b'),
#             round_a_failure=request.form.get('round_a_failure'),
#             round_b_c=request.form.get('round_b_c'),
#             round_b_failure=request.form.get('round_b_failure'),
#             round_c_success=request.form.get('round_c_success'),
#             round_c_failure=request.form.get('round_c_failure'),
#             round_success_success=request.form.get('round_success_success'),
#             round_success_failure=request.form.get('round_success_failure'),
#             round_failure_success=request.form.get('round_failure_success'),
#             round_failure_failure=request.form.get('round_failure_failure'),
#             round_a_a=request.form.get('round_a_a'),
#             round_b_b=request.form.get('round_b_b'),
#             round_c_c=request.form.get('round_c_c'),
#             growth_a=request.form.get('growth_a'),
#             growth_b=request.form.get('growth_b'),
#             growth_c=request.form.get('growth_c'),
#             growth_success=request.form.get('growth_success'),
#         )
#
#         print(txMatrix_dict)
#         #  Here we work on simulation:
#         print("Working on simulation here")
#         bokeh_script = server_document(url="http://localhost:5006/exitvalchart", arguments=txMatrix_dict)
#         return render_template("pages/exitval.html", form=form, bokeh_script = bokeh_script)
#
#     return render_template("pages/exitval.html", form=form)

