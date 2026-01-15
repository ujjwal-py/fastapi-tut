from pydantic import BaseModel, EmailStr, AnyUrl, Field, model_validator
from typing import List, Dict, Annotated, Optional

class Patient(BaseModel):
    name : str
    email:EmailStr
    age : int 
    weight: float
    married: Annotated[bool, Field(default=False)]
    allergies: Annotated[Optional[List[str]], Field(default=None, max_length=5)]
    contact: Dict[str, str]
    arogya_link : AnyUrl

    @model_validator(mode="after")
    def emergency_check(cls, model):
        if (model.age >= 60 and "emergency" not in model.contact):
            raise ValueError("Emergency Number must be present for patients with age 60 or older")
        else:
            return model
    



def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.allergies)
    print(patient.contact)
    print(patient.arogya_link)
    print("Inserted")

def update_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("Inserted")

patient_info = {"name" : "arav", "email": "blahblah@gmail.com", "age" : '100', "weight" : 56.5, "contact" : {"phone" : "23432423", "emergency" : "324234234"}, "arogya_link" : "https://google.com"}
Patient1 = Patient(**patient_info)

insert_patient(Patient1)
# update_patient(Patient1)
