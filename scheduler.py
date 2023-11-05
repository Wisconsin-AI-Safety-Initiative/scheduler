import random
from enum import Enum
from datetime import time

class Day(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    def __lt__(self, other: 'Day'):
        if isinstance(other, Day):
            return self.value < other.value
        else:
            return False

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.__str__()

class TimeSlot:
    def __init__(self, start_time: time, end_time: time):
        self.start_time = start_time
        self.end_time = end_time
        self.len = (self.end_time.hour - self.start_time.hour) * 60 + (self.end_time.minute - self.start_time.minute)
    
    # Returns length of time slot in minutes
    def __len__(self):
        return self.len
    
    def __lt__(self, other):
        if isinstance(other, TimeSlot):
            return self.start_time < other.start_time
        else:
            return False
    
    def __eq__(self, other):
        if isinstance(other, TimeSlot):
            return self.start_time == other.start_time and self.end_time == other.end_time
        else:
            return False

    def __str__(self):
        return f"{self.start_time.strftime('%I:%M %p')} to {self.end_time.strftime('%I:%M %p')}"

    def __repr__(self):
        return self.__str__()

class DaySchedule:
    def __init__(self, day: Day, time_slots: [TimeSlot]):
        self.day = day
        self.time_slots = time_slots
        self.coalesce_times()

    def coalesce_times(self) -> None:
        self.time_slots.sort()
        i = 0
        while i < (len(self.time_slots) - 1):
            if self.time_slots[i].end_time >= self.time_slots[i + 1].start_time:
                self.time_slots[i].end_time = self.time_slots[i + 1].end_time
                del self.time_slots[i + 1]
            else:
                i += 1
    
    def add_time_slot(self, time_slot: TimeSlot) -> None:
        self.time_slots.append(time_slot)
        self.coalesce_times()
    
    def find_overlap(self, other: 'DaySchedule') -> 'DaySchedule':
        overlap = []
        for time_slot in self.time_slots:
            for other_time_slot in other.time_slots:
                if time_slot.start_time <= other_time_slot.end_time and time_slot.end_time >= other_time_slot.start_time:
                    overlap.append(TimeSlot(max(time_slot.start_time, other_time_slot.start_time), min(time_slot.end_time, other_time_slot.end_time)))
        return DaySchedule(self.day, overlap)

    def __len__(self):
        return sum([len(time_slot) for time_slot in self.time_slots])

    def __str__(self):
        return f"{self.day}: {', '.join([str(slot) for slot in self.time_slots])}"

    def __repr__(self):
        return self.__str__()

class Availability:
    def __init__(self, week: {Day: DaySchedule}):
        self.week = {}
        for day in Day:
            self.week[day] = week[day] if day in week else DaySchedule(day, [])
        self.length = sum([len(day) for day in self.week.values()])
    
    # Find all time slots that are at least duration minutes long
    def find_time_slot(self, duration: int) -> 'Availability':
        slotsFound = {}
        for day in Day:
            slotsFound[day] = DaySchedule(day, [])
            for time_slot in self.week[day].time_slots:
                if len(time_slot) >= duration:
                    slotsFound[day].add_time_slot(time_slot)
        return Availability(slotsFound)
    
    def find_overlap(self, other: 'Availability') -> 'Availability':
        overlap = {}
        for day in Day:
            if self.is_available(day) and other.is_available(day):
                overlap[day] = DaySchedule(day, [])
                overlap[day] = self.week[day].find_overlap(other.week[day])
        return Availability(overlap)
    
    def is_available(self, day: Day) -> bool:
        return len(self.week[day]) > 0

    def __len__(self):
        return self.length

    def __str__(self):
        return '\n'.join([str(day) for day in self.week.values()])

    def __repr__(self):
        return self.__str__()
    
class Student:
    def __init__(self, name: str, email: str, availability: Availability):
        self.name = name
        self.email = email
        self.availability = availability
    
    def find_overlap(self, other: 'Student') -> 'Availability':
        return self.availability.find_overlap(other.availability)

    def __str__(self):
        return f"{self.name} ({self.email})"

    def __repr__(self):
        return self.__str__()

placeholder_names = [
    "Smith",
    "Johnson",
    "Brown",
    "Taylor",
    "Miller",
    "Wilson",
    "Moore",
    "Davis",
    "Anderson",
    "Jones",
    "Garcia",
    "Martinez",
    "Rodriguez",
    "Hernandez",
    "Lopez",
    "Gonzalez",
    "Perez",
    "Sanchez",
    "Torres",
    "Ramirez",
    "Flores",
    "Washington",
    "Lee",
    "Kim",
    "Chen",
    "Patel",
    "Williams",
    "Jones",
    "Jackson",
    "Harris",
    "White",
    "Clark",
    "Lewis",
    "Hall",
    "Young",
    "Turner",
    "Walker",
    "Thomas",
    "Wright",
    "Rodriguez",
    "Scott",
    "Evans",
    "Adams",
    "Baker",
    "Nelson",
    "Green",
    "Hill",
    "King",
    "Mitchell",
    "Carter"
]

placeholder_emails = [
    "smith@wisc.edu",
    "johnson@wisc.edu",
    "brown@wisc.edu",
    "taylor@wisc.edu",
    "miller@wisc.edu",
    "wilson@wisc.edu",
    "moore@wisc.edu",
    "davis@wisc.edu",
    "anderson@wisc.edu",
    "jones@wisc.edu",
    "garcia@wisc.edu",
    "martinez@wisc.edu",
    "rodriguez@wisc.edu",
    "hernandez@wisc.edu",
    "lopez@wisc.edu",
    "gonzalez@wisc.edu",
    "perez@wisc.edu",
    "sanchez@wisc.edu",
    "torres@wisc.edu",
    "ramirez@wisc.edu",
    "flores@wisc.edu",
    "washington@wisc.edu",
    "lee@wisc.edu",
    "kim@wisc.edu",
    "chen@wisc.edu",
    "patel@wisc.edu",
    "williams@wisc.edu",
    "jones@wisc.edu",
    "jackson@wisc.edu",
    "harris@wisc.edu",
    "white@wisc.edu",
    "clark@wisc.edu",
    "lewis@wisc.edu",
    "hall@wisc.edu",
    "young@wisc.edu",
    "turner@wisc.edu",
    "walker@wisc.edu",
    "thomas@wisc.edu",
    "wright@wisc.edu",
    "rodriguez@wisc.edu",
    "scott@wisc.edu",
    "evans@wisc.edu",
    "adams@wisc.edu",
    "baker@wisc.edu",
    "nelson@wisc.edu",
    "green@wisc.edu",
    "hill@wisc.edu",
    "king@wisc.edu",
    "mitchell@wisc.edu",
    "carter@wisc.edu"
]

participants = []

for i in range(5):
    days = list(Day)
    available_days = []
    for _ in range(random.randint(1, 7)):
        available_days.append(days.pop(random.randint(0, len(days) - 1)))
    
    week = {}
    for day in available_days:
        week[day] = DaySchedule(day, [])
        for _ in range(random.randint(1, 5)):
            start_time = time(random.randint(0, 13) + 9, 0)
            end_time = time(random.randint(start_time.hour + 1, 23), 0)
            week[day].add_time_slot(TimeSlot(start_time, end_time))

    participants.append(Student(placeholder_names[i], placeholder_emails[i], Availability(week)))

# facilitators = []

# for _ in range(5):
#     days = list(Day)
#     available_days = []
#     for _ in range(random.randint(1, 7)):
#         available_days.append(days.pop(random.randint(0, len(days) - 1)))
    
#     week = {}
#     for day in available_days:
#         week[day] = DaySchedule(day, [])
#         for _ in range(random.randint(1, 5)):
#             start_time = time(random.randint(0, 13) + 9, 0)
#             end_time = time(random.randint(start_time.hour + 1, 23), 0)
#             week[day].add_time_slot(TimeSlot(start_time, end_time))
    
#     facilitators.append(Availability(week))


GROUP_SIZE_MIN = 2
GROUP_SIZE_MAX = 10
GROUP_TIME = 60

potential_groups = {}

# Only allow time slots that are at least GROUP_TIME minutes long
for participant in participants:
    participant.availability = participant.availability.find_time_slot(GROUP_TIME)

# Find all participants that are available on each day
for day in Day:
    potential_groups[day] = []
    for participant in participants:
        if participant.availability.is_available(day):
            potential_groups[day].append(participant)

for day in Day:
    if len(potential_groups[day]) < GROUP_SIZE_MIN:
        del potential_groups[day]
        continue
    else:
        overlap = potential_groups[day][0].availability
        print(day, len(overlap), overlap.week[day])
        for participant in potential_groups[day]:
            overlap = overlap.find_overlap(participant.availability)
        print(day, len(overlap), overlap.week[day])
        if len(overlap) == 0:
            del potential_groups[day]

with open('output.txt', 'w') as f:
    f.write(str(potential_groups))

        # for facilitator in facilitators:
        #     if facilitator.is_available(day):
        #         potential_groups[day].append(facilitator)
    
        # potential_groups[day] = [group for group in potential_groups[day] if len(group) >= GROUP_SIZE_MIN]
    
        # if len(potential_groups[day]) == 0:
        #     del potential_groups[day]
        #     continue
    
        # potential_groups[day].sort(key=lambda group: len(group), reverse=True)
    
        # for group in potential_groups[day]:
        #     group = group.find_time_slot(GROUP_TIME)
        
        # potential_groups[day] = [group for group in potential_groups[day] if len(group) >= GROUP_TIME]
    
        # if len(potential_groups[day]) == 0:
        #     del potential_groups[day]
    
        # potential_groups[day].sort(key=lambda group: len(group), reverse=True)
    
        # for i in range(len(potential_groups[day])):
        #     for j in range(i + 1, len(potential_groups[day])):
        #         potential_groups[day][i] = potential_groups[day][i].find_overlap(potential_groups[day][j])
        
        # potential_groups[day] = [group for group in potential_groups[day] if len(group) >= GROUP_TIME]
    
        # if len(potential_groups[day]) == 0:
        #     del potential_groups[day]
    
        # potential_groups[day].sort(key=lambda group: len(group), reverse=True)
    
        # for i in range(len(potential_groups[day])):
        #     for j in range(i + 1, len(potential_groups[day])):
        #         potential_groups[day][i] = potential_groups[day][i].find_overlap(potential_groups[day][j])
        
        # potential_groups[day] = [group for group in potential_groups[day] if len(group) >= GROUP_TIME]
    
        # if len(potential_groups[day]) == 0:
        #     del potential_groups[day]
    
        # potential_groups[day].sort(key=lambda group: len(group), reverse=True)
    
        # for i in range(len(potential_groups[day])):
        #     for j in range(i + 1, len(potential_groups[day])):
        #         potential_groups[day][i] = potential_groups[day][i].find_overlap(potential_groups[day][j])