#!/bin/sh
python3 main.py --data "data/pfden.txt" --save "results_selfmade/pfden_results_12.txt" --min_sup 12
python3 main.py --data "data/pfden.txt" --save "results_selfmade/pfden_results_16.txt" --min_sup 16
python3 main.py --data "data/pfden.txt" --save "results_selfmade/pfden_results_20.txt" --min_sup 20

python3 main.py --data "data/bike.txt" --save "results_selfmade/bike_results_500.txt" --min_sup 500
python3 main.py --data "data/bike.txt" --save "results_selfmade/bike_results_750.txt" --min_sup 750
python3 main.py --data "data/bike.txt" --save "results_selfmade/bike_results_1000.txt" --min_sup 1000

python3 main.py --data "data/online_retail.txt" --save "results_selfmade/online_retail_results_1500.txt" --min_sup 1500
python3 main.py --data "data/online_retail.txt" --save "results_selfmade/online_retail_results_1600.txt" --min_sup 1600
python3 main.py --data "data/online_retail.txt" --save "results_selfmade/online_retail_results_1700.txt" --min_sup 1700

