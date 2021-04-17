from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from helpers.containers import get_host_from_traefik

app = FastAPI()


@app.get("/", response_class=PlainTextResponse)
async def root(release: str = "", repo: str = "", arch: str = "x86_64"):

    final_url = ""

    if repo and release:

        for traefik_url in get_host_from_traefik():
            nginx_url = "http://" + traefik_url + "/public/" + release + "/" + arch + "/" + repo

            # Here you should check if a given URl exists, then add it to the list, code:
            # import requests
            # nginx_request = requests.get(nginx_url, stream=True, verify=False)
            #     if nginx_request.status_code == 200:
            #         final_url.append(nginx_url)

            final_url = final_url+nginx_url+"\n"
        return final_url

    else:
        return "Please provide correct data!"
