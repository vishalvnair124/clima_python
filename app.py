from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import userfetch
import weatherfetch

app = FastAPI()

# Allowing all origins for demonstration purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def hello_world():
    return {"message": "Hello World"}

@app.get("/users/{user_id}")
def get_user(user_id: str):
    user_data = userfetch.get_user_data(user_id)
    if user_data:
        return user_data
    else:
        raise HTTPException(status_code=404, detail="User not found")
@app.get("/latest_weather")
def get_latest_weather():
    latest_weather = weatherfetch.get_latest_weather()
    if latest_weather:
        return latest_weather
    else:
        raise HTTPException(status_code=404, detail="Weather data not found")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, port=8000)
