from rest_framework.generics import CreateAPIView, ListAPIView, \
                                    UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
from django.template.defaultfilters import slugify

from meetings.models import Meeting
from projects.models import Project
from users.models import User

from meetings.api.serializers import MeetingSerialize

class MeetingListView(ListAPIView):

    serializer_class = MeetingSerialize
    queryset = Meeting.objects.all()

class MeetingDetailView(RetrieveAPIView):

    serializer_class = MeetingSerialize
    queryset = Meeting.objects.all()
    lookup_field = 'slug'

class MeetingDeleteView(DestroyAPIView):

    serializer_class = MeetingSerialize
    queryset = Meeting.objects.all()

class MeetingCreateView(CreateAPIView):

    serializer_class = MeetingSerialize
    queryset = Meeting.objects.all()

    def post(self, request, *args, **kwargs):

        meeting = Meeting()

        project = Project.objects.get(id = request.data.get('project'))
        meeting_leader = User.objects.get(id = request.data.get('meeting_leader'))

        meeting.title = request.data.get('title')
        meeting.status = request.data.get('status')
        meeting.slug = slugify(meeting.title)
        meeting.initial_date = request.data.get('initial_date')
        meeting.initial_hour = request.data.get('initial_hour')
        meeting.subject_matter = request.data.get('subject_matter')
        meeting.project = project
        meeting.meeting_leader = meeting_leader
        meeting.final_date = None
        meeting.final_hour = None

        meeting.save()
        serializer = MeetingSerialize(instance = meeting, data = request.data)
        serializer.is_valid(raise_exception = True)

        return Response(serializer.data)

class MeetingUpdateView(UpdateAPIView):

    serializer_class = MeetingSerialize
    queryset = Meeting.objects.all()

    def put(self, request, *args, **kwargs):

        meeting = Meeting.objects.get(id = request.data.get('meetingID'))
        project = Project.objects.get(id = request.data.get('projectID'))
        meeting_leader = User.objects.get(id = request.data.get('userID'))
        final_date = request.data.get('final_date')
        final_hour = request.data.get('final_hour')

        meeting.title = request.data.get('title')
        meeting.status = request.data.get('status')
        meeting.slug = slugify(meeting.title)
        meeting.initial_date = request.data.get('initial_date')
        meeting.initial_hour = request.data.get('initial_hour')
        meeting.subject_matter = request.data.get('subject_matter')
        meeting.project = project
        meeting.meeting_leader = meeting_leader

        if final_hour == '' or final_hour == None:
            meeting.final_hour = None
        else:
            meeting.final_hour = final_hour

        if final_date == '' or final_date == None:
            meeting.final_date = None
        else:
            meeting.final_date = final_date

        meeting.save()
        serializer = MeetingSerialize(instance = meeting, data = request.data)
        serializer.is_valid(raise_exception = True)

        return Response(serializer.data)

class MeetingsListView(ListAPIView):

    serializer_class = MeetingSerialize

    def get_queryset(self):
        project_slug = self.kwargs['slug']
        project = Project.objects.get(slug = project_slug)
        queryset = Meeting.objects.filter(project = project)

        return queryset

class MeetingAddUsers(UpdateAPIView):

    serializer_class = MeetingSerialize
    queryset = Meeting.objects.all()

    def put(self, request, *args, **kwargs):

        meeting = Meeting.objects.get(id = request.data.get('meetingID'))
        project = Project.objects.get(id = request.data.get('projectID'))
        meeting_leader = User.objects.get(id = request.data.get('userID'))
        final_date = request.data.get('final_date')
        final_hour = request.data.get('final_hour')

        meeting.title = request.data.get('title')
        meeting.status = request.data.get('status')
        meeting.slug = slugify(meeting.title)
        meeting.initial_date = request.data.get('initial_date')
        meeting.initial_hour = request.data.get('initial_hour')
        meeting.subject_matter = request.data.get('subject_matter')
        meeting.project = project
        meeting.meeting_leader = meeting_leader

        if final_hour == '' or final_hour == None:
            meeting.final_hour = None
        else:
            meeting.final_hour = final_hour

        if final_date == '' or final_date == None:
            meeting.final_date = None
        else:
            meeting.final_date = final_date

        for users in request.data.get('users'):
            new_user = User.objects.get(id = users['id'])
            meeting.users.add(new_user)

        meeting.save()
        serializer = MeetingSerialize(instance = meeting, data = request.data)
        serializer.is_valid(raise_exception = True)

        return Response(serializer.data)

class MeetingRemoveUsers(UpdateAPIView):

    serializer_class = MeetingSerialize
    queryset = Meeting.objects.all()

    def put(self, request, *args, **kwargs):

        meeting = Meeting.objects.get(id = request.data.get('meetingID'))
        project = Project.objects.get(id = request.data.get('projectID'))
        meeting_leader = User.objects.get(id = request.data.get('userID'))
        final_date = request.data.get('final_date')
        final_hour = request.data.get('final_hour')

        meeting.title = request.data.get('title')
        meeting.status = request.data.get('status')
        meeting.slug = slugify(meeting.title)
        meeting.initial_date = request.data.get('initial_date')
        meeting.initial_hour = request.data.get('initial_hour')
        meeting.subject_matter = request.data.get('subject_matter')
        meeting.project = project
        meeting.meeting_leader = meeting_leader

        if final_hour == '' or final_hour == None:
            meeting.final_hour = None
        else:
            meeting.final_hour = final_hour

        if final_date == '' or final_date == None:
            meeting.final_date = None
        else:
            meeting.final_date = final_date

        for users in request.data.get('users'):
            delete_user = User.objects.get(id = users['id'])
            meeting.users.remove(delete_user)

        meeting.save()
        serializer = MeetingSerialize(instance = meeting, data = request.data)
        serializer.is_valid(raise_exception = True)

        return Response(serializer.data)