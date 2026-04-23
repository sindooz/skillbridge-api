🧱 STEP 2: Paste this content

Copy this fully 👇

# SkillBridge Attendance System API

## 🔹 Project Overview
SkillBridge Attendance System API built using Django REST Framework.

## 🔹 Flow
Trainer creates batch → generates invite → student joins → trainer creates session → student marks attendance.

## 🔹 Test Users

Trainer:
trainer@gmail.com / 1234

Student:
stud@gmail.com / 1234

Programme Manager:
program@gmail.com / 1234

Monitoring Officer:
moniter@gmail.com / 1234

## 🔹 How to Run

pip install -r requirements.txt  
python manage.py migrate  
python manage.py runserver  

## 🔹 API Examples

Login:

curl -X POST http://127.0.0.1:8000/auth/login/

-H "Content-Type: application/json"
-d '{"email":"trainer@gmail.com
","password":"1234"}'


Create Batch:

curl -X POST http://127.0.0.1:8000/batches/

-H "Authorization: Bearer YOUR_TOKEN"
-H "Content-Type: application/json"
-d '{"name":"Batch 1"}'


Join Batch:

curl -X POST http://127.0.0.1:8000/batches/join/

-H "Authorization: Bearer STUDENT_TOKEN"
-H "Content-Type: application/json"
-d '{"token":"INVITE_TOKEN"}'


## 🔹 What Works
✔ Authentication  
✔ Batch & Invite System  
✔ Session Creation  
✔ Attendance Tracking  
✔ Role-Based Access  

## 🔹 What Not Perfect
❌ No frontend UI  
❌ Minimal testing  

## 🔹 Improvements
- Add better validations  
- Add refresh token rotation  
- Add frontend interface  

👉 Save file