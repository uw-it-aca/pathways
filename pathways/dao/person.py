# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from uw_person_client.models import Person


def get_person_by_uwnetid(uwnetid):
    kwargs = {"include_student": True, "include_student_transcripts": True}
    return Person.objects.get_person_by_uwnetid(uwnetid, **kwargs)
