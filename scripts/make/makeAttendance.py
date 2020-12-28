# Reads Attendance and guest list file, deterines in person, skype, live
# also adds original air date of episode to episode column

import csv


def readAttendance(reader):
    from campaigns.models import Campaign
    from episodes.models import Episode, Attendance, AttendanceType
    from players.models import Player
    from datetime import datetime

    header = next(reader)
    players = {
        2: Player.objects.get(full_name__contains=header[2]),
        3: Player.objects.get(full_name__contains=header[3]),
        4: Player.objects.get(full_name__contains=header[4]),
        5: Player.objects.get(full_name__contains=header[5]),
        6: Player.objects.get(full_name__contains=header[6]),
        7: Player.objects.get(full_name__contains=header[7]),
        8: Player.objects.get(full_name__contains=header[8])
    }

    if header[9] == "Orion":
        players[9] = Player.objects.get(full_name__contains=header[9])

    next(reader)

    NORMAL = AttendanceType.objects.get(name='normal')

    for row in reader:
        camp = Campaign.objects.get(num=int(row[0][1]))
        ep = Episode.objects.get(campaign=camp, num=int(row[0][3:]))
        date = datetime.strptime(row[1], '%Y/%m/%d')
        # ep.air_date = date.date()
        # ep.save()

        if camp.num == 1:
            COLEND = 9
        else:
            COLEND = 8

        end = COLEND + 1

        for col in range(2, end):
            if row[col] == "1":
                atten = Attendance.objects.get_or_create(episode=ep, player=players[col], attendance_type=NORMAL)
                if atten[1]:
                    print("CREATED: ", players[col].full_name, " in ", ep.title)


# will add guest, live episodes, and update player apperance to skype
def readGuests(reader):
    from episodes.models import Episode, Attendance, AttendanceType, Live
    from campaigns.models import Campaign
    from players.models import Player

    SKYPE = AttendanceType.objects.get(name='Skype')
    GUEST = AttendanceType.objects.get(name='Guest')

    next(reader)
    for row in reader:
        camp = Campaign.objects.get(num=int(row[0][1]))
        ep = Episode.objects.get(campaign=camp, num=int(row[0][3:]))

        if row[1] == "1":
            # get the duests ,4,5,6
            for col in range(4, 7):
                if row[col] != "":
                    guest = Player.objects.get(full_name=row[col])
                    attendance = Attendance.objects.get_or_create(episode=ep, player=guest, attendance_type=GUEST)
                    if attendance[1]:
                        print("CREATED: ", guest.full_name, " in ", ep.title)

        if row[2] == "1":
            # get the skype players and update og attendance,7,8
            for col in range(7, 9):
                if row[col] != "":
                    skyper = Player.objects.get(full_name=row[col])
                    currAtten = Attendance.objects.update_or_create(episode=ep, player=skyper,
                                                                    defaults={'attendance_type': SKYPE})
                    if currAtten[1]:
                        print("CREATED: ", skyper.full_name)

        if row[3] == "1":
            liveEp = Live.objects.get_or_create(episode=ep, venue=row[9])
            if liveEp[1]:
                print("CREATED LIVE EP:", ep.title, " @ ", liveEp[0].venue)


C1A = "/home/lightbulb/CritRoleDB/zdata/C1/C1 Times + Attendance/TD CR Attendance.csv"
C1G = "/home/lightbulb/CritRoleDB/zdata/C1/C1 Times + Attendance/TD guest list .csv"
C2A = "/home/lightbulb/CritRoleDB/zdata/C2/C2 Times + Attendance/WM CR Attendance.csv"
C2G = "/home/lightbulb/CritRoleDB/zdata/C2/C2 Times + Attendance/WM guest list.csv"

C1Areader = csv.reader(open(C1A))
C2Areader = csv.reader(open(C2A))
C1Greader = csv.reader(open(C1G))
C2Greader = csv.reader(open(C2G))

# readAttendance(C1Areader)
# readAttendance(C2Areader)

# readGuests(C1Greader)
# readGuests(C2Greader)
