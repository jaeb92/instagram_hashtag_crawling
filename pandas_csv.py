
import os
import datetime
from datetime import datetime, timedelta
import configparser
import glob
import pandas as pd
config = configparser.ConfigParser()


def to_csv(data):
    pathlink="./"

    if not os.path.isdir(pathlink):
        os.mkdir(pathlink)

    present_data = str(datetime.utcnow() + timedelta(hours=9))[:10]

    if len(glob.glob(pathlink + "/" + present_data + ".csv")) == 1:
        cnt = len(pd.read_csv(pathlink + "/" + present_data + ".csv", index_col = 0).index)
        time_pd = pd.DataFrame(data, index=[cnt])
        time_pd.to_csv(pathlink + "/" + present_data + ".csv", mode='a', header=False, encoding='utf-8-sig')
    else:
        cnt = 0
        time_pd = pd.DataFrame(data, index=[cnt])
        time_pd.to_csv(pathlink + "/" + present_data + ".csv", mode='a', encoding='utf-8-sig')