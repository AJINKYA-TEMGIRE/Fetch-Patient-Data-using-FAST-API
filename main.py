# Building the API's

from fastapi import FastAPI , HTTPException , Path, Query
from data_loader import load_data 

app = FastAPI()

# home routing
@app.get("/")
def home():
    return {"message" : "Hii, I am here for your help."}

# all records routing
@app.get("/records")
def records():
    data = load_data()
    return data

# specific patient routing
@app.get("/records/{patient_id}")
def records_patientid(patient_id : str = Path(... , description="Patient Number",
                                              example="P001")):
    data = load_data()
    for i in data:
        if i["patient_id"] == patient_id:
            return i
    raise HTTPException(status_code=404 , detail="Patient Not found")

@app.get("/blood/{group}")
def blood_group(group : str = Path(...,  description="Blood group of the patient",
                                   example="O+")):
    data = load_data()
    answer = []
    for i in data:
        if i["blood_group"] == group:
            answer.append(i)
    if len(answer) > 0:
        return answer 
    raise HTTPException(status_code=404, detail="No such patient with this blood group")

@app.get("/sort")
def sort(by : str = Query(... , description="Which basis you need to sort"),
         order : str = Query("asc" , description="asc or desc")):
    data = load_data()
    fields = ["height_cm", "weight_kg", "bmi"]
    if by not in fields:
        raise HTTPException(status_code=404,detail=f"Column not from {fields}")
    if order not in ["asc" , "desc"]:
        raise HTTPException(status_code=404,detail="order can be asc or desc")
    if order == "asc":
        sorted_patients = sorted(data, key=lambda x: x[f"{by}"])
        return sorted_patients
    else:
        sorted_patients = sorted(data, key=lambda x: x[f"{by}"] ,reverse=True)
        return sorted_patients

