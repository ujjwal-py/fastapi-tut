from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Annotated, Optional

class Patient(BaseModel):
    name : Annotated[str, Field(max_length=20, title="Patient's Name", description="keep it under 20 words")]
    email:EmailStr
    age : int = Field(gt=0, lt=120)
    weight: Annotated[float, Field(gt=0, strict=True)]
    married: Annotated[bool, Field(default=False)]
    allergies: Annotated[Optional[List[str]], Field(default=None, max_length=5)]
    contact: Dict[str, str]
    arogya_link : AnyUrl


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

patient_info = {"name" : "arav", "email": "blahblah@gmail.com", "age" : 100, "weight" : 56.5, "contact" : {"phone" : "23432423", "second_phone" : "324234234"}, "arogya_link" : "https://google.com"}
Patient1 = Patient(**patient_info)

insert_patient(Patient1)
# update_patient(Patient1)
