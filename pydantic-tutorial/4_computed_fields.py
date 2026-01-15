from pydantic import BaseModel, EmailStr, AnyUrl, Field, computed_field
from typing import List, Dict, Annotated, Optional

class Patient(BaseModel):
    name : str
    email:EmailStr
    age : int 
    weight: float
    height:float
    married: Annotated[bool, Field(default=False)]
    allergies: Annotated[Optional[List[str]], Field(default=None, max_length=5)]
    contact: Dict[str, str]
    arogya_link : AnyUrl

    @computed_field
    @property
    def bmi(self) -> float:
        return round((self.weight/self.height**2),2)



def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.allergies)
    print(patient.contact)
    print(patient.arogya_link)
    print(f"BMI = {patient.bmi}")
    print("Inserted")

def update_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("Inserted")

patient_info = {"name" : "arav", "email": "blahblah@gmail.com", "age" : '100', "weight" : 56.5, "height": 1.56, "contact" : {"phone" : "23432423", "second_phone" : "324234234"}, "arogya_link" : "https://google.com"}
Patient1 = Patient(**patient_info)

insert_patient(Patient1)
# update_patient(Patient1)
