from math import hypot
from collections import OrderedDict
import copy

## CLASSES

class Activity:
    is_selected = False

    def __init__(self, name):
        self.name = name

    def toggle_selected(self):
        if self.is_selected == True:
            self.is_selected = False
        else:
            self.is_selected = True

class MovingActivity(Activity):

    def set_distance(self, distance):
        self.distance = distance

    def to_string(self):
        return "%s (%dm)" % (self.name, self.distance)

class OnSpotActivity(Activity):
    reps = 0
    sets = 0
    rest = 0

    def set_reps(self, reps):
        self.reps = reps

    def set_sets(self, sets):
        self.sets = sets

    def set_rest(self, rest):
        self.rest = rest

    def to_string(self):
        return "%s (%d reps %d sets, %d secs rest)" % (self.name, self.reps, self.sets, self.rest)

class WorkoutLocation:

    station = 1

    def __init__(self, x, y, on_spot_activities=[], moving_activity=None):
        self.x = x
        self.y = y
        self.on_spot_activities = on_spot_activities
        self.moving_activity = moving_activity

    def set_on_spot_activities(self, on_spot_activities):
        self.on_spot_activities = on_spot_activities

    def set_moving_activity(self, moving_activity):
        self.moving_activity = moving_activity

    def calculate_distance(self, previous_location):
        return hypot(previous_location.x - self.x, previous_location.y - self.y)

    def clone(self):
        return copy.deepcopy(self)

    def on_spot_activities_to_string(self):
        string = ""
        for activity in self.on_spot_activities:
            string = "%s %s\n" % (string, activity.to_string())
        return string

    def to_string(self):
        return "%d %d %s %s" % (self.x, self.y, self.on_spot_activities_to_string(), self.moving_activity.to_string())

## FUNCTIONS

def display_activities_for_input(activities):
    for index in xrange(len(activities)):
        if activities[index].is_selected:
            print '%d %s == selected ==' % (index, activities[index].name)
        else:
            print '%d %s' % (index, activities[index].name)
    return raw_input("Select the number of the activity, D for done:")

def move_selected_activities(activities):
    selected_activities = []
    for activity in activities:
        if activity.is_selected:
            selected_activities.append(activity)
            activity.toggle_selected()

    return selected_activities

def print_activity_list(activities):
    index = 0
    for activity in activities:
        print "%d %s" % (index, activity.name)
        index = index + 1

def select_moving_activity(activities):
    while True:
        print_activity_list(activities)

        result = raw_input("Select the number of the activity:")

        if result >= 0 or result < len(activities):
            index = int(result)
            return activities[index]
        else:
            print "Wrong selection! Try again"

def select_spot_activities(activities):
    result = None

    while True:
        result = display_activities_for_input(activities).lower()
        if result == "d":
            break
        elif result >= 0 or result < len(activities):
            index = int(result)
            activity = activities[index]
            if not activity.is_selected:
                activity.set_reps(raw_input("Enter the number of reps: "))
                activity.set_sets(raw_input("Enter the number of sets: "))
            activity.toggle_selected()
        else:
            print "Please enter d or the number of the activity! Try again"

    # now move all the selected ones into the selected activities
    selected_activities = move_selected_activities(activities)
    return selected_activities

def get_next_location():
    x, y = raw_input("Enter location coordinates in the following format 'x y':").split()
    return WorkoutLocation(int(x), int(y))

def print_overview(stations):
    ordered_stations_dict = OrderedDict(sorted(stations.items(), key=lambda t: t[0]))

    print "\n=== Exercise Overview ==="
    for i, (key, value) in enumerate(ordered_stations_dict.iteritems()):
        print 'Station %d (%d, %d):' % (key, value.x, value.y)

        for activity in value.on_spot_activities:
                print '%s %10s (reps) %5s (sets)' % (activity.name, str(activity.reps), str(activity.sets))

        if value.moving_activity != None:
            print '%s %10s (meters)' % (value.moving_activity.name, str(value.moving_activity.distance))

# Use a default message if nothing is passed in.
def print_selection_error(msg="That was an invalid selection. Please try again."):
    print msg

def print_workout_locations(locations):
    print "\nList of locations:"
    for key in locations:
        print "%d : %s" % (key, locations[key].to_string())

def delete_station(locations):
    # print all the locations
    print_workout_locations(locations)

    while True:
        result = raw_input("Select the number of the location to be deleted, (B) to go back:").lower()

        if result == "b":
            return locations
        elif int(result) in locations:  #if the result is not in here
            new_locations_dict = copy.deepcopy(locations)
            del new_locations_dict[int(result)]
            #need to reorder the keys here now
            print "deleted the location, returning new one now"
            return new_locations_dict
        else:
            print_selection_error("failed on delete station")


def display_stations(stations):
    print_overview(stations)

    while True:
        result = raw_input("Do you wish to (E)dit or (D)elete a station? (C) to cancel:").lower()
        if result == "e":
            # do editing
            print "Not implemented yet..."
            return stations
        elif result == "d":
            # delete the station
            stations = delete_station(stations)
            return stations
        elif result == "c":
            return stations
        else:
            print_selection_error("failed on display stations")

def main():
    moving_activities = [MovingActivity("running"), MovingActivity("skipping"), MovingActivity("jumping")]
    on_the_spot_activities = [OnSpotActivity("press ups"), OnSpotActivity("sit ups"), OnSpotActivity("crunches")]

    # maintain a map of each workout location
    current_index = 1  #remember which station it is
    last_index = 1 #remember where to insert the next station

    stations = {} #operate with a standard dictionary, sort it later
    done = False

    location = get_next_location()
    previous_location = location  #reset the previous location
    last_action = None

    while not done:
        print "You are at station %d" % (current_index)
        action = raw_input("Select (M)ove, on the (S)pot, (E)dit or (F)inished:").lower()

        if action == 'm':
            next_location = get_next_location()

            activity = select_moving_activity(moving_activities)
            distance = next_location.calculate_distance(location)
            activity.set_distance(distance)

            location.set_moving_activity(activity)

            # clone a reference and insert it in the map, update
            stations[last_index] = location.clone()
            last_index = last_index + 1

            previous_location = location  #update the target location
            location = next_location

        elif action == 's' and last_action != 's':
            activities = select_spot_activities(on_the_spot_activities)
            location.set_on_spot_activities(activities)

        elif action == 'f':
            stations[last_index] = location.clone() #clone the last station
            done = True

        elif action == 'e':
            stations = display_stations(stations)

        else:
            #action is to remove the station
            print "%s wasn\'t a correct choice, please try again" % (action)

        last_action = action

    print_overview(stations)

main()

#done
