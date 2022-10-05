from persistent_message.models import Message
import datetime


def get_message_json():
    user_msgs = []
    for msg in Message.objects.all().order_by('begins'):
        user_msgs.append(_to_json(msg))
        # if msg.is_active(datetime.datetime.now()):
        #     user_msgs.append(_to_json(msg))
    return user_msgs

def _to_json(msg, include_tags=False):
    json_data = {
        'id': msg.pk,
        'content': msg.content,
        'level': msg.level,
        'level_name': msg.get_level_display(),
        'start': msg.begins.isoformat() if (
            msg.begins is not None) else None,
        'end': msg.expires.isoformat() if (
            msg.expires is not None) else None
    }
    if include_tags:
        for tag in msg.tags.all():
            json_data[tag.name] = True
    return json_data
