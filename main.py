from fastapi import FastAPI 
from fastapi.responses import RedirectResponse 

app = FastAPI(title="Redirector Service")

@app.post("/short-urls")
def create_short_url():

    return {"status": "not implemented yet"}

@app.get("/{shortened_url}")
def redirect_short_url(shortened_url: str):

    return {"status": "not implemented yet"}


