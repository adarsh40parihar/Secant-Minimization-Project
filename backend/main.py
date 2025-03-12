from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel  #Used to validate and structure API request data
from secant import secant_minimization, generate_graph

app = FastAPI()

# Enable CORS (Cross-Origin Resource)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["POST","GET"],
    allow_headers=["*"],
)

# Define request model
class SecantInput(BaseModel):
    fx: str
    a: float
    b: float
    tol: float

@app.post("/minimize")
def minimize(input_data: SecantInput):
    result = secant_minimization(input_data.fx, input_data.a, input_data.b, input_data.tol)
    
    # Generate the final function graph
    final_graph = generate_graph(input_data.fx, result["x_min"])
    result["final_graph"] = f"data:image/png;base64,{final_graph}"

    return result

@app.get("/")
def home():
    return {"message": "Secant Minimization API is running!"}
