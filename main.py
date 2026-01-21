from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Annotated, Literal, Optional
import json
from fastapi.middleware.cors import CORSMiddleware
import re





#pydantic models
class Patient(BaseModel):
    id : Annotated[str, Field(..., title="Patient ID", description="Unique ID of the Patient")]
    name : Annotated[str, Field(..., title="Patient Name", description="Name of the patient under 30 chars", max_length=30, )]
    city : Annotated[str, Field(..., description="Where the patient lives")]
    age : Annotated[int, Field(..., description="Age of the patient must be between 0 and 120", gt=0, lt=120)]
    gender : Annotated[Literal['male', 'female','other'], Field(..., description="Select Gender from [male, female, other]")]
    height : Annotated[float, Field(..., description="Height of the patient must be greater than 0", gt=0)]
    weight : Annotated[float, Field(..., description="Weight of the patients must be greater than 0", gt=0)]

    @computed_field
    @property
    def bmi(self) -> float:
        return round((self.weight/self.height**2), 2)
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 24.9:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"
        
    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str):
        if not v.strip():
            raise ValueError("Name cannot be empty")

        if v.isdigit():
            raise ValueError("Name cannot be numbers")

        if not re.match(r"^[A-Za-z ]+$", v):
            raise ValueError("Name must contain only letters and spaces")

        return v

class PatientUpdated(BaseModel):
    name : Annotated[Optional[str], Field(default=None, title="Patient Name", description="Name of the patient under 30 chars", max_length=30)]
    city : Annotated[Optional[str], Field(default=None, description="Where the patient lives")]
    age : Annotated[Optional[int], Field(default=None, description="Age of the patient must be between 0 and 120", gt=0, lt=120)]
    gender : Annotated[Optional[Literal['male', 'female','other']], Field(default=None, description="Select Gender from [male, female, other]")]
    height : Annotated[Optional[float], Field(default=None, description="Height of the patient must be greater than 0", gt=0)]
    weight : Annotated[Optional[float], Field(default=None, description="Weight of the patients must be greater than 0", gt=0)]

#app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # allow all origins (dev only)
    allow_methods=["*"],     # GET, POST, PUT, DELETE
    allow_headers=["*"],
)

def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
        return data

def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f)


@app.get("/")
def hello_world():
    return {"message" : "Patient Record Managamenet System"}

@app.get("/about")
def about_page():
    return {"message":"A fully functional API to record patients data"}

@app.get("/view-all")
def view_all():
    data = load_data()
    return data

@app.get("/view/{id}")
def view_patient(id: str = Path(..., description="Unique Patient ID", example="P001")):
    data = load_data()
    if id in data:
        return data[id]
    else:
        raise HTTPException(status_code=404, detail="Patient ID not found")
    
@app.get("/sort")
def sort_patients(sorted_by: str = Query(..., description="Sort patients from Height,BMI,Weight"), sorted_order: str=Query("asc", description="The order for output either asc or desc")):
    valid_field = ["height", 'weight', "bmi"]
    if sorted_by not in valid_field:
        raise HTTPException(status_code=400, detail=f"Invalid feild, Choose from {valid_field}")
    if sorted_order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid Sorting Order")
    
    order = True if sorted_order == "desc" else False
    
    data = load_data()
    sorted_data = sorted(data.values(), key=lambda x:x.get(sorted_by, 0), reverse=order)
    return sorted_data

@app.post("/create")
def new_patient(patient: Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")
    
    data[patient.id] = patient.model_dump(exclude=["id"])

    save_data(data)

    return JSONResponse(status_code=200, content={"message" : "Patient Created SUcessfully"})

@app.put("/update/{patient_id}")
def update_patient(patient_id : str, patient_update:PatientUpdated):

    data = load_data()
    # check if patient doesnt exists
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # get the existing and upated patient data
    existing_patient_data = data[patient_id]
    updated_patient_data = patient_update.model_dump(exclude_unset=True)


    #update the raw data
    for key,value in updated_patient_data.items():
        existing_patient_data[key] = value

    #create pydantic object for updated data to get the calculated field in case if changed
    if "height" in updated_patient_data or "weight" in updated_patient_data:
        existing_patient_data['id'] = patient_id
        patient_pydantic_object = Patient(**existing_patient_data)
        existing_patient_data = patient_pydantic_object.model_dump(exclude=["id"])

    #finally update in json
    data[patient_id] = existing_patient_data
    save_data(data)
    return JSONResponse(status_code=200, content={"message" : "patient sucessfully udpated"})

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    data = load_data()  
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    del data[patient_id]
    save_data(data)

    return JSONResponse(status_code=200, content={"message" : "patient data deleted sucessfully"})

    
    






