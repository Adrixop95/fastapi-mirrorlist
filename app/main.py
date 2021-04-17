import ast
import os

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv

from helpers.containers import get_host_from_traefik

app = FastAPI()
load_dotenv(verbose=True)

traefik_hosts = os.environ.get('traefik_hosts')
provided_hosts = os.environ.get('provided_hosts')


@app.get("/", response_class=PlainTextResponse)
async def root(release: str = "", repo: str = "", arch: str = "x86_64"):
    final_url = ""
    url_list = list(provided_hosts.split(","))

    if ast.literal_eval(traefik_hosts):
        url_list.extend(get_host_from_traefik())

    if repo and release:
        for mirror_url in url_list:
            # not the best way to generate url, ikr
            nginx_url = "http://" + mirror_url + "/" + release + "/" + repo + "/" + arch + "/os/"

            final_url = final_url + nginx_url + "\n"
        return final_url

    else:
        return "Please provide correct data!"
