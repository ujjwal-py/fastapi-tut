from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
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

    @field_validator("email")
    @classmethod
    def email_validator(cls, value):
        valid_domains = ["gmail.com", "yahoo.com", "outlook.com"]
        value_domain = value.split("@")[-1]
        if value_domain not in valid_domains:
            raise ValueError(f"Invalid Email Domain\nCorrect Domains are {valid_domains}")
        else:
            return value
        
    @field_validator("age", mode="after")
    @classmethod
    def age_validator(cls, value):
        if 0 < value < 120:
            return value
        else:
            raise ValueError("Invalid Age, must be between 0 and 120")



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

patient_info = {"name" : "arav", "email": "blahblah@gmail.com", "age" : '100', "weight" : 56.5, "contact" : {"phone" : "23432423", "second_phone" : "324234234"}, "arogya_link" : "https://google.com"}
Patient1 = Patient(**patient_info)

insert_patient(Patient1)
# update_patient(Patient1)
