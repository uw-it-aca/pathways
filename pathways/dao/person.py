# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.db.models.functions import JSONObject
from uw_person_client.models import Person, Major
from uw_person_client.exceptions import PersonNotFoundException


def get_major_name_by_code(code):
    query = Major.objects.filter(major_abbr_code=code).values(
        json=JSONObject(
            major_abbr_code='major_abbr_code',
            major_name='major_name'
        )
    ).order_by('-major_last_yr').first()

    try:
        return query.get('json')
    except AttributeError:
        pass


def get_person_by_uwnetid(uwnetid):
    person = Person.objects.get_person_by_uwnetid(
        uwnetid, include_student=True, include_student_transcripts=True)

    person_data = {
        'uwnetid': person.uwnetid,
        'display_name': person.display_name,
        'preferred_first_name': person.preferred_first_name,
        'preferred_surname': person.preferred_surname,
    }

    if not person.student or not person.student.transcripts:
        return person_data

    latest_transcript = person.student.transcripts.last()

    intended_majors = []
    for code in person.student.intended_majors:
        json = get_major_name_by_code(code)
        if json:
            intended_majors.append(json)

    person_data.update({
        'student_number': person.student.student_number,
        'class_desc': person.student.class_desc,
        'scholarship_desc': latest_transcript.scholarship_desc if (
            latest_transcript is not None) else "",
        'total_credits': person.student.total_credits,
        'cumulative_gpa': person.student.cumulative_gpa,
        'quarters_completed': person.student.transcripts.count(),
        'majors': [{
                'major_abbr_code': m.major_abbr_code,
                'major_name': m.major_name,
            } for m in person.student.majors
        ],
        'intended_majors': intended_majors,
        'advisers': [{
                'uwnetid': a.employee.person.uwnetid,
                'display_name': a.employee.person.display_name,
                'email': f'{a.employee.person.uwnetid}@uw.edu',
                'home_department': a.employee.home_department,
            } for a in person.student.advisers.all()
        ],
    })

    return person_data


def valid_uwnetid(username):
    error_msg = None
    if username is not None and len(username) > 0:
        try:
            person = Person.objects.get_person_by_uwnetid(username)
            if username.lower() == person.uwnetid:
                pass
            else:
                error_msg = (
                    f"Current UWNetID: {person.uwnetid}, Prior UWNetID: ")
        except PersonNotFoundException:
            error_msg = f"Not a valid UWNetID: "
    else:
        error_msg = "No override user supplied, please enter a UWNetID"
    return error_msg
