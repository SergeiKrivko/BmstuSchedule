from app import domain, models
from app.api import schemas


def create_concrete_pair(
    pair: domain.SchedulePair,
    concrete_times: domain.TimeSlot,
) -> schemas.SchedulePairRead:
    return schemas.SchedulePairRead(
        time_slot=concrete_times,
        discipline=_create_discipline_base(pair.discipline),
        teachers=[_create_teacher_base(t) for t in pair.teachers],
        rooms=[_create_room_base(a) for a in pair.audiences],
        groups=[_create_group_base(g) for g in pair.groups],
    )


def _create_discipline_base(discipline: models.Discipline) -> schemas.DisciplineBase:
    return schemas.DisciplineBase(
        id=discipline.id,
        abbr=discipline.abbr,
        full_name=discipline.full_name,
        short_name=discipline.short_name,
        act_type=discipline.act_type,
    )


def _create_teacher_base(teacher: models.Teacher) -> schemas.TeacherBase:
    return schemas.TeacherBase(
        id=teacher.id,
        first_name=teacher.first_name,
        middle_name=teacher.middle_name,
        last_name=teacher.last_name,
        departments=[],
    )


def _create_room_base(audience: models.Audience) -> schemas.RoomBase:
    return schemas.RoomBase(
        id=audience.id,
        name=audience.name,
        building=audience.building,
        map_url=audience.map_url,
    )


def _create_group_base(group: models.Group) -> schemas.GroupBase:
    return schemas.GroupBase(
        id=group.id,
        abbr=group.abbr,
        course_id=group.course_id,
        semester_num=group.semester_num,
    )
