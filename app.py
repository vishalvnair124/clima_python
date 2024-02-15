from fastapi import FastAPI, HTTPException
import userfetch

app = FastAPI()

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

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
