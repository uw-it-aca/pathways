# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from persistent_message.models import Message


def persistent_messages(request):
    ret = {"messages": []}
    for message in Message.objects.active_messages():
        if "message_level" not in ret:
            ret["message_level"] = message.get_level_display().lower()
        ret["messages"].append(message.render())

    return ret
