# Generated by Django 3.0.6 on 2020-08-13 01:18

from django.db import migrations, models, transaction
import django.db.models.deletion
import django_extensions.db.fields
from django.conf import settings
from django_mri.utils.utils import get_subject_model, get_min_distance_session


class Migration(migrations.Migration):
    def scan_subject_to_session(apps, schema_editor):
        Subject = get_subject_model()
        Scan = apps.get_model("django_mri", "Scan")
        Session = apps.get_model("django_mri", "Session")

        for scan in Scan.objects.all():
            subjects = Subject.objects.filter(id_number=scan.dicom.patient.uid)
            subject = None
            if len(subjects) == 0:
                scan.session_id = Session.objects.create(time=scan.time).id
                scan.save()
            else:
                subject = subjects.first()
                sessions = subject.mri_session_set.all()
                if scan.session:
                    sessions = sessions.exclude(id=scan.session_id)
                if len(sessions) == 0:
                    Session.objects.create(subject_id=subject.id, time=scan.time)
                    sessions = subject.mri_session_set.all()
                min_session = get_min_distance_session(scan, sessions)
                if (
                    scan.number
                    in list(min_session.scan_set.values_list("number", flat=True))
                    and scan.session_id != min_session.id
                ):
                    new_session = Session.objects.create(
                        subject_id=subject.id, time=scan.time
                    )
                    scan.session_id = new_session.id
                    scan.save()
                    scan.session.save()
                elif scan.session_id != min_session.id:
                    scan.session_id = min_session.id
                    scan.save()
                    scan.session.save()
                other_sessions = subject.mri_session_set.exclude(id=scan.session_id)
                for session in other_sessions:
                    for other_scan in session.scan_set.all():
                        other_scan.infer_session()

        for subject in Subject.objects.all():
            for session in subject.mri_session_set.all():
                session.save()

    def session_to_scan_subject(apps, schema_editor):
        Scan = apps.get_model("django_mri", "Scan")
        for scan in Scan.objects.all():
            scan.subject = scan.session.subject
            scan.save()

    dependencies = [("django_mri", "0006_auto_20200813_0118")]

    operations = [
        migrations.RunPython(
            scan_subject_to_session, reverse_code=session_to_scan_subject
        ),
    ]
