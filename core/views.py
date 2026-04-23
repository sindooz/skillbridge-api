from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from rest_framework.permissions import IsAuthenticated
from .permissions import IsTrainer
from .models import User
from .permissions import IsStudent

from .models import Batch
from .serializers import BatchSerializer
from .permissions import IsTrainer

import uuid
from django.utils import timezone
from datetime import timedelta
from .models import BatchInvite

from .models import BatchStudent

from .models import Session, Batch,Attendance
from .serializers import SessionSerializer
from .serializers import AttendanceSerializer

from .permissions import IsInstitution

from .permissions import IsProgrammeManager

import jwt
from datetime import datetime, timedelta
from django.conf import settings
from .permissions import IsMonitoringOfficer

class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=201)

        return Response(serializer.errors, status=400)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        # 🔥 Find user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=401)

        # 🔐 Authenticate using username internally
        user = authenticate(username=user.username, password=password)

        if user is None:
            return Response({"error": "Invalid credentials"}, status=401)

        # 🎟️ Generate JWT
        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })
    


# Only Trainer Can Create Session

class CreateSessionView(APIView):
    permission_classes = [IsAuthenticated, IsTrainer]

    def post(self, request):
        return Response({"message": "Session created"})


# Only Student Can Mark Attendance

class MarkAttendanceView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request):
        return Response({"message": "Attendance marked"})


# Multiple Roles Allowed

class CreateBatchView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role not in ["trainer", "institution"]:
            return Response({"error": "Forbidden"}, status=403)

        return Response({"message": "Batch created"})
    

# Create Batch (Trainer / Institution only)

class CreateBatchView(APIView):
    permission_classes = [IsAuthenticated, IsTrainer]

    def post(self, request):
        serializer = BatchSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(institution=request.user)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=422)    


# to generate invite token

class GenerateInviteView(APIView):
    permission_classes = [IsAuthenticated, IsTrainer]

    def post(self, request, batch_id):
        try:
            batch = Batch.objects.get(id=batch_id)
        except Batch.DoesNotExist:
            return Response({"error": "Batch not found"}, status=404)

        token = str(uuid.uuid4())

        invite = BatchInvite.objects.create(
            batch=batch,
            token=token,
            created_by=request.user,
            expires_at=timezone.now() + timedelta(days=1)
        )

        return Response({
            "invite_token": invite.token
        })


# Student Joins Batch

class JoinBatchView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request):
        token = request.data.get("token")

        try:
            invite = BatchInvite.objects.get(token=token, used=False)
        except BatchInvite.DoesNotExist:
            return Response({"error": "Invalid token"}, status=400)

        if invite.expires_at < timezone.now():
            return Response({"error": "Token expired"}, status=400)

        # Add student to batch
        BatchStudent.objects.create(
            batch=invite.batch,
            student=request.user
        )

        invite.used = True
        invite.save()

        return Response({"message": "Joined batch successfully"})
    


# create join batch view

class JoinBatchView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request):
        token = request.data.get("token")

        if not token:
            return Response({"error": "Token is required"}, status=422)

        try:
            invite = BatchInvite.objects.get(token=token, used=False)
        except BatchInvite.DoesNotExist:
            return Response({"error": "Invalid or already used token"}, status=400)

        # Check expiry
        if invite.expires_at < timezone.now():
            return Response({"error": "Token expired"}, status=400)

        # Check already joined (important)
        if BatchStudent.objects.filter(batch=invite.batch, student=request.user).exists():
            return Response({"error": "Already joined this batch"}, status=400)

        # Add student to batch
        BatchStudent.objects.create(
            batch=invite.batch,
            student=request.user
        )

        # Mark token as used
        invite.used = True
        invite.save()

        return Response({"message": "Joined batch successfully"})


# to create session view


class CreateSessionView(APIView):
    permission_classes = [IsAuthenticated, IsTrainer]

    def post(self, request):
        batch_id = request.data.get("batch")

        # Check batch exists
        try:
            batch = Batch.objects.get(id=batch_id)
        except Batch.DoesNotExist:
            return Response({"error": "Batch not found"}, status=404)

        serializer = SessionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(
                trainer=request.user,
                batch=batch
            )
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)
    


# marking attendance

class MarkAttendanceView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request):
        session_id = request.data.get("session")
        status_value = request.data.get("status")

        # Check session exists
        try:
            session = Session.objects.get(id=session_id)
        except Session.DoesNotExist:
            return Response({"error": "Session not found"}, status=404)

        # Check student belongs to batch
        is_enrolled = BatchStudent.objects.filter(
            batch=session.batch,
            student=request.user
        ).exists()

        if not is_enrolled:
            return Response({"error": "You are not part of this batch"}, status=403)

        # Prevent duplicate attendance
        if Attendance.objects.filter(session=session, student=request.user).exists():
            return Response({"error": "Attendance already marked"}, status=422)

        # Save attendance
        attendance = Attendance.objects.create(
            session=session,
            student=request.user,
            status=status_value
        )

        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data, status=201)    
    


# to view attendance

class SessionAttendanceView(APIView):
    permission_classes = [IsAuthenticated, IsTrainer]

    def get(self, request, session_id):
        # Check session exists
        try:
            session = Session.objects.get(id=session_id)
        except Session.DoesNotExist:
            return Response({"error": "Session not found"}, status=404)

        attendance_records = Attendance.objects.filter(session=session)

        data = []
        for record in attendance_records:
            data.append({
                "student": record.student.username,
                "status": record.status,
                "marked_at": record.marked_at
            })

        return Response({
            "session": session.title,
            "attendance": data
        })  



# for the batch summary

class BatchSummaryView(APIView):
    permission_classes = [IsAuthenticated, IsInstitution]

    def get(self, request, batch_id):
        try:
            batch = Batch.objects.get(id=batch_id)
        except Batch.DoesNotExist:
            return Response({"error": "Batch not found"}, status=404)

        total_students = BatchStudent.objects.filter(batch=batch).count()
        total_sessions = Session.objects.filter(batch=batch).count()

        total_attendance = Attendance.objects.filter(session__batch=batch).count()
        present_count = Attendance.objects.filter(
            session__batch=batch,
            status="present"
        ).count()

        return Response({
            "batch": batch.name,
            "total_students": total_students,
            "total_sessions": total_sessions,
            "total_attendance_records": total_attendance,
            "present_count": present_count
        })      



# institution summary

class InstitutionSummaryView(APIView):
    permission_classes = [IsAuthenticated, IsProgrammeManager]

    def get(self, request, institution_id):
        batches = Batch.objects.filter(institution_id=institution_id)

        total_batches = batches.count()
        total_sessions = Session.objects.filter(batch__in=batches).count()
        total_attendance = Attendance.objects.filter(session__batch__in=batches).count()

        return Response({
            "institution_id": institution_id,
            "total_batches": total_batches,
            "total_sessions": total_sessions,
            "total_attendance_records": total_attendance
        })



# program summary

class ProgrammeSummaryView(APIView):
    permission_classes = [IsAuthenticated, IsProgrammeManager]

    def get(self, request):
        total_batches = Batch.objects.count()
        total_sessions = Session.objects.count()
        total_attendance = Attendance.objects.count()

        return Response({
            "total_batches": total_batches,
            "total_sessions": total_sessions,
            "total_attendance_records": total_attendance
        })



# monitoring a token

class MonitoringTokenView(APIView):
    permission_classes = [IsAuthenticated, IsMonitoringOfficer]

    def post(self, request):
        api_key = request.data.get("key")

        if api_key != settings.MONITORING_API_KEY:
            return Response({"error": "Invalid API key"}, status=401)

        payload = {
            "user_id": request.user.id,
            "role": "monitoring_officer",
            "exp": datetime.utcnow() + timedelta(hours=1)
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        return Response({"monitoring_token": token})
    


# monitoring attendance

class MonitoringAttendanceView(APIView):

    def get(self, request):
        token = request.headers.get("Authorization")

        if not token:
            return Response({"error": "Token missing"}, status=401)

        try:
            token = token.split(" ")[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            if payload.get("role") != "monitoring_officer":
                return Response({"error": "Invalid role"}, status=401)

        except jwt.ExpiredSignatureError:
            return Response({"error": "Token expired"}, status=401)
        except Exception:
            return Response({"error": "Invalid token"}, status=401)

        # Return all attendance
        data = Attendance.objects.all().values()

        return Response({
            "attendance": list(data)
        })
    