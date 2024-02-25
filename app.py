from fastapi import FastAPI, HTTPException,Request
from fastapi.middleware.cors import CORSMiddleware
import userfetch
import weatherfetch
import user
import login
import mail
import check

app = FastAPI()


@app.post("/check_email/")
async def check_email(request: Request):
    data = await request.json()
    user_email = data.get("user_email")
    if not user_email:
        raise HTTPException(status_code=400, detail="Email is missing in request data")
    exists = check.email_exists(user_email)
    # Return 200 if email does not exist
    if not exists:
        return {"exists": False}
    return {"exists": True}


@app.post("/send_email/")
async def send_email(email_data: mail.EmailData):
    if mail.send_email(email_data.user_email, email_data.otp):
        return {"message": "Email sent successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to send email")

# Allowing all origins for demonstration purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/login/")
async def user_login(request: Request):
    data = await request.json()
    email = data.get("user_email")
    password = data.get("user_password")

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email or password missing")

    if login.authenticate_user(email, password):
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
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
# POST endpoint to add a new user
@app.post("/add_user/")
async def create_user(request: Request):
    data = await request.json()
   
    user_name = data.get("user_name")
    user_email = data.get("user_email")
    user_password = data.get("user_password")
    if not user_password or not user_name or not user_email:
        raise HTTPException(status_code=400, detail="User data is incomplete")
    return user.add_user( user_name, user_email,user_password)

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
