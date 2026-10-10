from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Student Management API")

class StudentBase(BaseModel):
    name: str
    age: int
    course: str

class StudentCreate(StudentBase):
    pass 

class Student(StudentBase):
    id: int 

students_db = {}
current_id = 1

# 1.GET (Retrieve all student)
@app.get("/students", response_model=List[Student])
def get_student():
    return list(students_db.values())

# 2.GET (Retrieve a specific student)
@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Studen not found")
    return students_db[student_id]

# 3.POST (Create a new student)
@app.post("/student", response_model=Student, status_code=201)
def create_student(student: StudentCreate):
    global current_id
    new_student = Student(id=current_id, **student.model_dump())
    students_db[current_id] = new_student
    current_id += 1
    return new_student

# 4.PUT (Update an existing student)
@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, student: StudentCreate):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")

    update_student = Student(id=student_id, **student.model_dump())
    students_db[student_id] = update_student
    return update_student

# 5.DELETE (Delete a student) 
@app.delete("/student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")

    delete_student = students_db.pop(student_id)
    return{
        "message": "Student deleted successfully", 
        "deleted_student": delete_student
    }
