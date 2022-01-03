# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand
import json
import random


class Command(BaseCommand):

    def handle(self, *args, **options):
        currics = ['CHEM', 'CSE', 'MATH', 'B BIO', 'A A', "ANTH", "INFO",
                   "BIOL", "CLAS", "DRAMA", "ECON"]
        used_currics = []
        objs = []
        for n in range(10000):
            curric_num = random.randint(100, 499)
            curric_id = "%s %s" % (random.choice(currics), curric_num)
            if curric_id not in used_currics:
                used_currics.append(curric_id)
                objs.append({"course_id": curric_id,
                             "coi_score": random.randint(0, 50)/10})
        with open('pathways/data/coi_scores.json', "w") as coi_file:
            coi_file.write(json.dumps(objs))
