# import time
from piazza_api.rpc import PiazzaRPC
from imgurpython import ImgurClient
import json
import glob
import sys
import time


def post_to_piazza(n, config, title, content, is_test):
    if is_test:
        nid = config['test_nid']
    else:
        nid = config['nid']
    piazza_client = PiazzaRPC(nid)
    piazza_client.user_login(config['email'], config['password'])
    params = {
        "type": "note",  # note, question, followup
        "anonymous": "no",  # "no", "stud", "full"
        "config": {},
        "content": content,
        "folders": [f"hw{n}"],
        "nid": nid,
        "status": "active",
        "subject": title,
    }
    return piazza_client.content_create(params)


def main(n, is_test):
    with open('config.json', 'r') as f:
        config = json.load(f)

    imgur_client = ImgurClient(config['client_id'], config['client_secret'])

    for index, img_path in enumerate(sorted(glob.glob(f'rendered/hw{n}/hw{n}-img*.png'))):
        response = imgur_client.upload_from_path(img_path)
        url = f'https://i.imgur.com/{response["id"]}.png'
        title = f'HW{n} Q{index + 1}'
        content = f'<img src="{url}">#pin'
        post_to_piazza(n, config, title, content, is_test)
        time.sleep(2)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] == 'true')
