from pydantic import BaseModel, EmailStr, Field, computed_field
from typing import List


class Contact(BaseModel):
    phone: str = Field(..., description="Patient contact number", example="9876543210")
    email: EmailStr = Field(..., description="Patient email address", example="user@example.com")


class Vitals(BaseModel):
    blood_pressure: str = Field(..., description="Blood pressure in mmHg", example="120/80")
    heart_rate: int = Field(..., description="Heart rate in beats per minute", example=72)
    temperature_c: float = Field(..., description="Body temperature in Celsius", example=36.6)


class PatientCreate(BaseModel):
    patient_id: str = Field(
    ...,
    description="Unique patient ID",
    example="P006"
)
    name: str = Field(..., description="Full name of the patient", example="Ajinkya Temgire")
    age: int = Field(..., ge=0, le=120, description="Age of the patient", example=25)
    gender: str = Field(..., description="Gender of the patient", example="Male")
    
    height_cm: float = Field(..., gt=0, description="Height in centimeters", example=170)
    weight_kg: float = Field(..., gt=0, description="Weight in kilograms", example=70)
    
    blood_group: str = Field(..., description="Blood group", example="B+")
    
    contact: Contact
    address: str = Field(..., description="Residential address", example="Pune, Maharashtra")
    
    medical_history: List[str] = Field(default_factory=list, description="Past medical conditions")
    allergies: List[str] = Field(default_factory=list, description="Known allergies")
    current_medications: List[str] = Field(default_factory=list, description="Ongoing medications")
    
    vitals: Vitals
    
    last_visit: str = Field(..., description="Last visit date (YYYY-MM-DD)", example="2026-04-25")

    @computed_field
    @property
    def bmi(self) -> float:
        height_m = self.height_cm / 100
        return round(self.weight_kg / (height_m ** 2), 2)

    @computed_field
    @property
    def bmi_category(self) -> str:
        bmi = self.bmi
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"