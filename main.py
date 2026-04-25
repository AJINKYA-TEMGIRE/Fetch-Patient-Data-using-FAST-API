from fastapi import FastAPI, HTTPException, Path, Query
from data_loader import load_data, save_data
from pydantic_validator import PatientCreate

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hii, I am here for your help."}

@app.get("/records")
def records():
    return load_data()

@app.get("/records/{patient_id}")
def records_patientid(
    patient_id: str = Path(..., description="Patient Number", example="P001")
):
    data = load_data()
    for i in data:
        if i["patient_id"] == patient_id:
            return i
    raise HTTPException(status_code=404, detail="Patient Not found")

@app.get("/blood/{group}")
def blood_group(
    group: str = Path(..., description="Blood group of the patient", example="O+")
):
    data = load_data()
    answer = [i for i in data if i["blood_group"].lower() == group.lower()]
    if answer:
        return answer
    raise HTTPException(status_code=404, detail="No such patient with this blood group")

@app.get("/sort")
def sort(
    by: str = Query(..., description="Which basis you need to sort"),
    order: str = Query("asc", description="asc or desc")
):
    data = load_data()
    fields = ["height_cm", "weight_kg", "bmi"]

    if by not in fields:
        raise HTTPException(status_code=400, detail=f"Column not from {fields}")

    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="order can be asc or desc")

    return sorted(
        data,
        key=lambda x: x.get(by, 0),
        reverse=(order == "desc")
    )

@app.post("/create")
def create(p: PatientCreate):
    data = load_data()

    for i in data:
        if p.patient_id == i["patient_id"]:
            raise HTTPException(status_code=400, detail="Patient id already exists")

    data.append(p.model_dump())
    save_data(data)

    return {
        "message": "Patient Created Successfully",
        "patient_id": p.patient_id
    }