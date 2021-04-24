import ast
import os
import requests

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv

from helpers.traefik_labels import get_host_from_traefik

app = FastAPI()
load_dotenv(verbose=True)

traefik_hosts = os.environ.get('traefik_hosts')
provided_hosts = os.environ.get('provided_hosts')


@app.get("/", response_class=PlainTextResponse)
async def root(release: str = "", repo: str = "", arch: str = "x86_64"):
    final_url = ""

    url_list = list(provided_hosts.split(","))
    payload = {'release': release, 'arch': arch, 'repo': repo}

    # If traefik_hosts is true from env, add host to list
    if ast.literal_eval(traefik_hosts):
        url_list.extend(get_host_from_traefik())

    # If repo and release are specified in the request,
    # iterate through all URLs,
    # then try to get a request that must be other than 400/500,
    # add checks to the final result
    if repo and release:
        for mirror_url in url_list:
            try:
                # even if served by https, requests will automatically correct final url
                response = requests.get("http://" + mirror_url, params=payload)

                if response.status_code < 400:
                    final_url += response.url + "\n"

            except requests.exceptions.ConnectionError as e:
                print(e)

        return final_url

    else:
        return "Please provide correct request!"
