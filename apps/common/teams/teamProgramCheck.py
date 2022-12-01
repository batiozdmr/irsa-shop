from django.db.models import Q

from apps.parameter.models import TeamMember, Program, ProgramCriterion, Team, Application
from apps.stakeholders.models import Profile, User
from django.utils.translation import gettext_lazy as _

class TeamProgramCheck:
    def __init__(self, pk, user, team=None):
        self.app = self.getApp(pk)
        if team == None:
            self.teams = self.getTeamList(user)
        else:
            self.teams = self.getTeam(team)
        self.criterion = self.getCriterion(pk)
        self.endStatus = self.getCheckTeamAll()

    def getTeam(self, getTeam):
        contenTeam = Team.objects.filter(id=getTeam)
        return contenTeam

    def getApp(self, pk):
        contenProgram = Program.objects.filter(pk=pk).first()
        return contenProgram

    def getTeamList(self, user):
        contenTeamMember = TeamMember.objects.filter(member=user).values_list('team_id', flat=True)
        contenTeam = Team.objects.filter(id__in=contenTeamMember)

        return contenTeam

    def getCriterion(self, pk):
        contenProgram = Program.objects.filter(pk=pk).first()

        return ProgramCriterion.objects.filter(pk=contenProgram.criterion_id).first()

    def getTeamsCount(self, team):
        number = TeamMember.objects.filter(team=team).filter(Q(memberType_id=1) | Q(memberType_id=3))
        numberCount=number.count()
        return numberCount

    def getCheckTeamAll(self):
        for team in self.teams:
            if self.getMinNumberOfMembers(team) == False: return _(
                "Takımınız yarışmanın minumum üye kriterine uymadığı için başvuru yapamamaktasınız.")
            if self.getMaxNumberOfMembers(team) == False: return _(
                "Takımınız yarışmanın maximum üye kriterine uymadığı için başvuru yapamamaktasınız.")
            if self.getConsultant(team) == False: return _(
                "Yarışma kriteri doğrultusunda takımınızda en az  bir danışman olmalıdır.")
            if self.getCaptain(team) == False: return _(
                "Yarışma kriterine göre takımınızda en az bir kaptan olmalıdır.")
            if self.getConsultantMaxTeam(team) == False: return _(
                "Takım danışmanının bu yarışma içerisinde başka bir takımda bulunması yarışma kriterine uygun değildir.")
            if self.getTeamMemberMultiTeam(team) == False: return _(
                "Takım üyelerinin bu yarışma içerisinde başka bir takımda bulunması yarışma kriterine uygun değildir.")
            if self.getAllEducationStatus(team) == False: return _(
                "Takım üyelerinin eğitim durumları yarışmanın eğitim seviyesi kriterine uygun değildir.")
            if self.getAtLeastOneEducationStatus(team) == False: return _(
                "Takım üyelerinin eğitim durumları yarışmanın eğitim seviyesi kriterine uygun değildir.")

        return True

    def getMinNumberOfMembers(self, team):

        if self.criterion.minNumberOfMembers:

            if self.getTeamsCount(team) >= self.criterion.minNumberOfMembers:
                return True
            else:
                return False
        else:
            return True

    def getMaxNumberOfMembers(self, team):

        if self.criterion.maxNumberOfMembers:
            if self.getTeamsCount(team) <= self.criterion.maxNumberOfMembers:
                return True
            else:
                return False
        else:
            return True

    def getConsultant(self,team):

        if self.criterion.consultant == True:
            checkTeamConsultant=TeamMember.objects.filter(team=team).filter(memberType_id=2)
            if checkTeamConsultant:
                return True
            else:
                return False
        else:
            return True

    def getCaptain(self,team):

        if self.criterion.captain == True:
            checkTeamCaptain=TeamMember.objects.filter(team=team).filter(memberType_id=3)
            if checkTeamCaptain:
                return True
            else:
                return False
        else:
            return True

    def getConsultantMaxTeam(self,team):
        if self.criterion.consultantMaxTeam:
            contenProgram = self.app
            checkAppyl=Application.objects.filter(program=contenProgram).values_list('applicantTeam_id', flat=True)
            checkTeamConsultant = TeamMember.objects.filter(team=team).filter(memberType_id=2).first()
            checkTeamConsultantTeam = TeamMember.objects.filter(member=checkTeamConsultant.member,team_id__in=checkAppyl).count()
            if checkTeamConsultantTeam <= self.criterion.consultantMaxTeam:
                return True
            else:
                return False
        else:
            return True

    def getTeamMemberMultiTeam(self,team):
        if self.criterion.teamMemberMultiTeam == True:
            contenProgram = self.app
            checkAppyl=Application.objects.filter(program=contenProgram).values_list('applicantTeam_id', flat=True)
            thisTeamMember = TeamMember.objects.filter(team=team).filter(Q(memberType_id=1) | Q(memberType_id=3)).values_list('member_id', flat=True)
            appylTeamMember = TeamMember.objects.filter(team_id__in=checkAppyl).filter(member_id__in=thisTeamMember)

            if appylTeamMember:
                return False
            else:
                return True
        else:
            return True

    def getAllEducationStatus(self, team):
        if self.criterion.atLeastOneEducationStatus.all():
            teamMember = TeamMember.objects.filter(team=team).filter(Q(memberType_id=1) | Q(memberType_id=3))
            for i in teamMember:
                a = Profile.objects.filter(user_id=i.member.id).first()
                if a.educationLevel not in self.criterion.allEducationStatus.all():
                    return False
            return True
        else:
            return True

    def getAtLeastOneEducationStatus(self, team):
        if self.criterion.atLeastOneEducationStatus.all():
            teamMember = TeamMember.objects.filter(team=team).filter(Q(memberType_id=1) | Q(memberType_id=3))
            for i in teamMember:
                a = Profile.objects.filter(user_id=i.member.id).first()
                if a.educationLevel in self.criterion.atLeastOneEducationStatus.all():
                    return True
            return False
        else:
            return True
