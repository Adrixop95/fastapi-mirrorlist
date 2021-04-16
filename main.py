from fastapi import FastAPI
import urllib

app = FastAPI()


@app.get("/")
async def root(package: str = "", release: str = ""):
    final_url = []
    if package and release:

        for i in range(2):
            nginx_url = "https://nginx" + str(i + 1) + ".localhost/public/" + release + "/" + package

            # Here you should check if a given URl exists, then add it to the list, code:
            # import requests
            # nginx_request = requests.get(nginx_url, stream=True, verify=False)
            #     if nginx_request.status_code == 200:
            #         final_url.append(nginx_url)

            final_url.append(nginx_url)

        return final_url

    else:
        return "Please provide correct data!"
