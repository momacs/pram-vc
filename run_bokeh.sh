#!/bin/bash
#conda activate env_prams
#bokeh serve ./fin-work/FinancialAnalysis/localBokeh/main.py --allow-websocket-origin=127.0.0.1:5000
#bokeh serve ./fin-work/FinancialAnalysis/localBokeh/exitvalchart.py --allow-websocket-origin=127.0.0.1:5000
#bokeh serve ./fin-work/FinancialAnalysis/localBokeh/compare.py --allow-websocket-origin=127.0.0.1:5000
#bokeh serve ./fin-work/FinancialAnalysis/localBokeh/pram_startup.py  --allow-websocket-origin=127.0.0.1:5000
bokeh serve ./localBokeh/pram_startup.py ./localBokeh/compare.py ./localBokeh/exitvalchart.py  ./localBokeh/main.py --allow-websocket-origin="*"

