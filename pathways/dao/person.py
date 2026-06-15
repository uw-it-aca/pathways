# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from uw_person_client.models import Person
from uw_person_client.exceptions import PersonNotFoundException


def get_person_by_uwnetid(uwnetid):
    person = Person.objects.get_person_by_uwnetid(
        uwnetid, include_student=True, include_student_transcripts=True)

    if not person.student or not person.student.transcripts:
        return {}

    latest_transcript = person.student.transcripts.last()

    return {
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
        'advisers': [{
                    'uwnetid': a.employee.person.uwnetid,
                    'display_name': a.employee.person.display_name,
                    'email': f'{a.employee.person.uwnetid}@uw.edu',
                    'home_department': a.employee.home_department,
                } for a in person.student.advisers.all()
            ],
    }
