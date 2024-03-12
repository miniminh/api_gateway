from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from starlette.background import BackgroundTask
import httpx
import uvicorn
import configparser

config = configparser.ConfigParser()
config.read('gateway.ini')

services_port = config['gateway']

ip = config['ip']['current_ip']

app = FastAPI()

@app.get("/{services}/{path:path}")
async def get_reverse_proxy(request: Request, services: str, path: str, scheme: str = "http"):
    port = services_port[services]
    url = f"{scheme}://10.133.52.105:{port}/{path}"
    print(url)
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=request.headers, params=request.query_params)
    return HTMLResponse(content=response.text, status_code=response.status_code)

@app.post("/{services}/{path:path}")
async def post_reverse_proxy(request: Request, services: str, path: str):
    port = services_port[services]
    client = httpx.AsyncClient() 
    print(f'http://{ip}:{port}' + request.url.path.replace(services + '/', ''))
    url = httpx.URL(f'http://{ip}:{port}' + request.url.path.replace(services + '/', ''))
    
    req = client.build_request(
        request.method, url, headers=request.headers.raw, content=request.stream(), timeout=60.0
    )
    r = await client.send(req, stream=True)
    return StreamingResponse(
        r.aiter_raw(),
        status_code=r.status_code,
        headers=r.headers,
        background=BackgroundTask(r.aclose)
    )

def main():
    uvicorn.run("reverse:app", host="0.0.0.0", port=14024)

if __name__ == "__main__":
    main()
