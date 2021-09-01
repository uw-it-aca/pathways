from pathways.views.api import RESTDispatch


class MajorList(RESTDispatch):
    def get(self, request, args, **kwargs):
        pass


class Major(RESTDispatch):
    def get(self, request, major_id, args, **kwargs):
        pass
