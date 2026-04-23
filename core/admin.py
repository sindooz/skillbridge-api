from django.contrib import admin
from .models import User, Batch, BatchTrainer, BatchStudent, BatchInvite, Session, Attendance

admin.site.register(User)
admin.site.register(Batch)
admin.site.register(BatchTrainer)
admin.site.register(BatchStudent)
admin.site.register(BatchInvite)
admin.site.register(Session)
admin.site.register(Attendance)
