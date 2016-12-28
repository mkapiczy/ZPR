def get_student_messages(student):
    messages = []
    if student.profile.inbox and student.profile.inbox.newprojectteammessage_set:
        for msg in student.profile.inbox.newprojectteammessage_set.all():
            messages.append(msg)
    return messages

def refresh_inbox_status(request, student):
    inbox = get_student_messages(student)
    request.session['inbox'] = inbox
    request.session['unread_messages_size'] = len(inbox)