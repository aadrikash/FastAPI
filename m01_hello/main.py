from fastapi import FastAPI
from datetime import datetime

app = FastAPI(
    title = 'Workbook API',
    description = 'My first FastAPI app',
    version = '0.1.0',
)



@app.get('/')
def read_root():
    return {'message': 'Hello, FastAPI!'}


@app.get('/health')
def health_check():

    return {'status':'ok'}



#EXERCISE1

#Add GET /about returning your name and the API version. Then add GET /time returning the current server time (from datetime import datetime).


@app.get("/about")
def about():
    return{"name": "Aadrika Sharma",
           "api_version":"0.1.0"
           }


#exercise 1.2 create /time

@app.get("/time")
def get_time():
    current_time = datetime.now()
    return {
        "current_time": current_time.isoformat()       

    }



