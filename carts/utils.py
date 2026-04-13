def get_or_create_session(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key