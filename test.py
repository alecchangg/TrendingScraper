import requests
import pandas as pd
from datetime import date

BASE = "http://127.0.0.1:5000/"


response = requests.delete(BASE + "staging/out/")
print(response)