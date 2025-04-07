#!/bin/bash


echo "Running crontab" >> crontabLog.txt

python3 /Users/dhurgadharani/Fashion/IGScraping.py
python3 /Users/dhurgadharani/Fashion/IGCleaning.py
python3 /Users/dhurgadharani/Fashion/articleScraping.py
python3 /Users/dhurgadharani/Fashion/articleCleaning.py
python3 /Users/dhurgadharani/Fashion/frequencyDatabase.py

echo "Crontab ran" >> crontabLog.txt
