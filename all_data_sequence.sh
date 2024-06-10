#!/bin/sh
echo "For min_sup equal $1"
python3 main.py --data "data/pfden.txt" --save "results/pfden_results.txt" --min_sup $1
python3 main.py --data "data/bike.txt" --save "results/bike_results.txt" --min_sup $1
python3 main.py --data "data/e_shop.txt" --save "results/e_shop_results.txt" --min_sup $1
python3 main.py --data "data/online_retail.txt" --save "results/online_retail_results.txt" --min_sup $1
