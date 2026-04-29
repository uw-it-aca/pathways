# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


class UWPersonRouter():
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'uw_person_client':
            return 'uw_person'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'uw_person_client':
            return 'uw_person'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'uw_person_client':
            return db == 'uw_person'
        elif db == 'uw_person':
            return False
        return None
