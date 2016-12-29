def delayErrorAlertFade(request, alert):
    if (request.session.get('delayClearParam') is not None):
        request.session['delayClearParam'] = None
    else:
        request.session[alert] = None