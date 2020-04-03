import django
import os
import random
import logging

logging.basicConfig(level=logging.DEBUG)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from datacenter.models import (Schoolkid,
                    Teacher,
                    Subject,
                    Lesson,
                    Mark,
                    Chastisement,
                    Commendation)

commendations = [
    'Молодец!',
    'Отлично!',
    'Хорошо!',
    'Гораздо лучше, чем я ожидал!',
    'Ты меня приятно удивил!',
    'Великолепно!'
]


def get_schoolkid(kid_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=kid_name)
    except Schoolkid.DoesNotExist:
        logging.warning('No such schoolkid')
        return None
    except Schoolkid.MultipleObjectsReturned:
        logging.warning('There are several schoolkids with this name')
        return None
    return schoolkid


def fix_marks(kid_name):
    """Change kid_name's grades 2 and 3 to 5."""
    schoolkid = get_schoolkid(kid_name)
    if schoolkid is None:
        return
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__lte=3)
    bad_marks.update(points=5)


def remove_chastisements(kid_name):
    """Remove kid_name's chastisements."""
    schoolkid = get_schoolkid(kid_name)
    if schoolkid is None:
        return
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()


def create_commendation(kid_name, subject_name):
    """Create commendation for kid_name on subject_name.

    Commendation date will be subject_name's last lesson date.
    """
    schoolkid = get_schoolkid(kid_name)
    if schoolkid is None:
        return
    subject = Subject.objects.get(title=subject_name, year_of_study=6)
    lesson = Lesson.objects.filter(subject=subject).order_by('date').last()
    lesson_date = lesson.date
    teacher = lesson.teacher
    commendation = random.choice(commendations)
    Commendation.objects.create(
        text=commendation, created=lesson_date, schoolkid=schoolkid,
        subject=subject, teacher=teacher)
