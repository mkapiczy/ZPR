from main.models import NewProjectTeamRequest, UserInbox, Message, Course
from student.models import ProjectTeam, StudentUser


def createProjectTeam(project):
    projectTeam = ProjectTeam()
    projectTeam.project = project
    projectTeam.course = project.course
    projectTeam.save()
    return projectTeam


def createNewProjectTeamRequest(project_team):
    new_team_request = NewProjectTeamRequest()
    new_team_request.project_team = project_team
    new_team_request.save()
    return new_team_request


def clear_project_signed_users_set(project):
    for student in project.studentuser_set.all():
        student.signed_project = None
        student.save()


def createNewProjectTeamMessage(project_team):
    title = 'Zaproszenie do grupa projektowa';
    text = 'Czy chcesz zaakceptować zaproszenie do grupy projektu: ' + project_team.project.name + '\n';
    text += "Członkowie grupy: \n";
    for student in project_team.studentuser_set.all():
        text += student.profile.first_name + ' ' + student.profile.last_name + '\n'
    message = Message(title=title, text=text)
    message.save()
    return message


def chosenStudentsAreValid(chosen_students, project):
    if (len(chosen_students) >= project.minimum_students_number
        and len(chosen_students) <= project.allowed_students_number):
        return True
    else:
        return False


def getChosenStudentsFromRequest(request):
    students = request.POST.getlist('students')
    chosen_students = []
    for student_id in students:
        chosen_students.append(StudentUser.objects.get(id=student_id))
    return chosen_students

def tutorAllowedTeamsNumberNotExceeded(project):
    tutor = project.tutor
    tutorAllowedTeamsNumber = tutor.getTutorAllowedTeamsNumberByCourseId(project.course_id)
    tutorTeams = tutor.getAllTeamsAssignedToTutorForCourse(project.course_id)
    if len(tutorTeams) < tutorAllowedTeamsNumber:
        return True
    else:
        return False
