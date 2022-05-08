from literadar import start_libradar
import time
import json
import sys
import random
import requests
import os
import subprocess
from tqdm import tqdm 


def get_apk_name_from_path(apk_path):
    # Get file name
    head, tail = os.path.split(apk_path)
    apk_name = tail
    # Remove .apk
    if tail.endswith(".apk"):
        apk_name = apk_name[:-4]
    return apk_name

def noti(msg):
    url =  "https://hooks.slack.com/services/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"
    message = (msg)
    title = (f":zap:")
    slack_data = {
        "username": "NotificationBot",
        "icon_emoji": ":satellite:",
        #"channel" : "#somerandomcahnnel",
        "attachments": [
            {
                "color": "#9733EE",
                "fields": [
                    {
                        "title": title,
                        "value": message,
                        "short": "false",
                    }
                ]
            }
        ]
    }
    byte_length = str(sys.getsizeof(slack_data))
    headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
    response = requests.post(url, data=json.dumps(slack_data), headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)

def run_by_cat(path_to_apks, out_path, cat):
    apks = [ _ for  _ in os.listdir(path_to_apks) if _.endswith(r".apk")]
    for a in tqdm(apks):
        a_path = path_to_apks + a
        name = get_apk_name_from_path(a_path)

        res = start_libradar(a_path)
        json_str = json.dumps({name:res})

        timestr = time.strftime("%Y-%m-%d")
        file_name = out_path + name + "-" + timestr + ".json"
        with open(file_name, 'w') as out:
            out.write(json_str)
        
    msg = cat + " is done"
    noti(msg)
    return 0

def run_all_cats(path_to_all_cats):
    raw_cats = [ _ for  _ in os.listdir(path_to_all_cats) if _.startswith("TOP-FREE")]
    cats = sorted(raw_cats)

    for cat in tqdm(cats):
        if cat == 'TOP-FREE_APPLICATION':
            continue
        outdir = "/home/seb5923/small-world/libradar-out/"+cat
        subprocess.run(["mkdir",outdir])
        run_by_cat(path_to_all_cats+cat+"/", outdir, cat)
    msg = "DEEJAYY KHALEDDDDDD"
    noti(msg)