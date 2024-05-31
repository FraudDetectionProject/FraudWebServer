import uvicorn
from fastapi import FastAPI
from views import yh
app = FastAPI(
    debug=True,
    version='0.0.1',
)

app.include_router(yh.router)

@app.get('/')
def root():
    result = {
        'version' : '0.0.1',
        'message' : 'Audio Fraud Detection Serivce'
    }
    return result

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
