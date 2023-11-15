import fitdecode
from datetime import datetime

UNIX_TIME_OFFSET = 631065600
SPEED_SCALE_FACTOR = 1/1000
DISTANCE_SCALE_FACTOR = 1/100


class SwimFitReader():
    def __init__(self, filename) -> None:
        self.filename = filename

        self.laps = {}
        self.laps['index'] = []
        self.laps['start_time'] = []
        self.laps['stroke'] = []
        self.laps['total_strokes'] = []
        self.laps['total_distance'] = []
        self.laps['number_of_lanes'] = []
        self.laps['avg_velocity_in_m_per_s'] = []
        self.laps['avg_pace_in_min_per_100m'] = []
        self.laps['avg_pace_in_min_per_100m_string'] = []
        self.laps['max_velocity_in_m_per_s'] = []
        self.laps['max_pace_in_min_per_100m'] = []
        self.laps['max_pace_in_min_per_100m_string'] = []
        self.laps['total_elapsed_time_in_min'] = []
        self.laps['total_elapsed_time_in_min_string'] = []
        self.laps['lanes'] = []

        self.lanes = {}
        self.lanes['index'] = []
        self.lanes['stroke'] = []
        self.lanes['total_strokes'] = []
        self.lanes['velocity_in_m_per_s'] = []
        self.lanes['avg_pace_in_min_per_100m'] = []
        self.lanes['avg_pace_in_min_per_100m_string'] = []
        self.lanes['total_elapsed_time_in_min'] = []
        self.lanes['total_elapsed_time_in_min_string'] = []
        self.session = {}
        self.metadata = {}

        self._extract_data()

    def get_lane(self, lane_index):
        lane = {}
        for key in self.lanes:
            lane[key] = self.lanes[key][lane_index]

        return lane

    def get_lap(self, lap_index):
        lap = {}
        for key in self.laps:
            lap[key] = self.laps[key][lap_index]

        return lap

    def get_max_number_of_lanes(self):
        return self.lanes["index"][-1]+1

    def get_max_number_of_laps(self):
        return self.laps["index"][-1]+1

    def _extract_data(self):
        self._extract_all_lanes()
        self._extract_all_laps()
        self._integrate_lanes_to_laps()

    def _integrate_lanes_to_laps(self):
        for index_laps in self.laps["index"]:
            self.laps['lanes'].append([])
            for index_lanes in range(0, self.laps["number_of_lanes"][index_laps]):
                self.laps['lanes'][index_laps].append(
                    self.get_lane(index_lanes))

    def _extract_all_lanes(self):
        self.fit_file = fitdecode.FitReader(self.filename)
        for frame in self.fit_file:
            if isinstance(frame, fitdecode.records.FitDataMessage):
                if frame.name == "length":
                    for field in frame.fields:
                        if field.name == "message_index":
                            self.lanes['index'].append(field.raw_value)
                        if field.name == "swim_stroke":
                            if field.raw_value == 0:
                                self.lanes['stroke'].append("Freestyle")
                            elif field.raw_value == 2:
                                self.lanes['stroke'].append("Breaststroke")
                            elif field.raw_value == 5:
                                self.lanes['stroke'].append("Miscellaneous")
                            else:
                                self.lanes['stroke'].append("Backstroke")
                        if field.name == "total_strokes":
                            self.lanes['total_strokes'].append(field.raw_value)
                        if field.name == "avg_speed":
                            self.lanes['velocity_in_m_per_s'].append(field.raw_value *
                                                                     SPEED_SCALE_FACTOR)
                            self.lanes['avg_pace_in_min_per_100m'].append(1 /
                                                                          self.lanes['velocity_in_m_per_s'][-1] /
                                                                          DISTANCE_SCALE_FACTOR/60)
                            self.lanes['avg_pace_in_min_per_100m_string'].append(
                                self._minutes2string(self.lanes['avg_pace_in_min_per_100m'][-1]))
                        if field.name == "total_elapsed_time":
                            self.lanes['total_elapsed_time_in_min'].append(self._milliseconds2min(
                                field.raw_value))
                            self.lanes['total_elapsed_time_in_min_string'].append(
                                self._minutes2string(self.lanes['total_elapsed_time_in_min'][-1]))

    def _extract_all_laps(self):
        self.fit_file = fitdecode.FitReader(self.filename)
        for frame in self.fit_file:
            if isinstance(frame, fitdecode.records.FitDataMessage):
                if frame.name == "lap":
                    for field in frame.fields:
                        # print(field.name + " = " + str(field.raw_value))
                        if field.name == "message_index":
                            self.laps['index'].append(field.raw_value)
                        if field.name == "start_time":
                            self.laps['start_time'].append(datetime.fromtimestamp(
                                field.raw_value+UNIX_TIME_OFFSET))
                        if field.name == "swim_stroke":
                            if field.raw_value == 0:
                                self.laps['stroke'].append("Freestyle")
                            elif field.raw_value == 2:
                                self.laps['stroke'].append("Breaststroke")
                            elif field.raw_value == 5:
                                self.laps['stroke'].append("Miscellaneous")
                            else:
                                self.laps['stroke'].append("Backstroke")
                        if field.name == "total_strokes":
                            self.laps['total_strokes'].append(field.raw_value)
                        if field.name == "total_distance":
                            self.laps['total_distance'].append(
                                field.raw_value*DISTANCE_SCALE_FACTOR)
                        if field.name == "num_lengths":
                            self.laps['number_of_lanes'].append(
                                field.raw_value)
                        if field.name == "min_temperature":
                            self.laps['water_temperature'].append(
                                field.raw_value)
                        if field.name == "enhanced_avg_speed" and field.raw_value is not None:
                            self.laps['avg_velocity_in_m_per_s'].append(field.raw_value *
                                                                        SPEED_SCALE_FACTOR)
                            self.laps['avg_pace_in_min_per_100m'].append(1 /
                                                                         self.laps['avg_velocity_in_m_per_s'][-1] /
                                                                         DISTANCE_SCALE_FACTOR/60)
                            self.laps['avg_pace_in_min_per_100m_string'].append(
                                self._minutes2string(self.laps['avg_pace_in_min_per_100m'][-1]))
                        if field.name == "enhanced_max_speed" and field.raw_value is not None:
                            self.laps['max_velocity_in_m_per_s'].append(field.raw_value *
                                                                        SPEED_SCALE_FACTOR)
                            self.laps['max_pace_in_min_per_100m'].append(1 /
                                                                         self.laps['max_velocity_in_m_per_s'][-1] /
                                                                         DISTANCE_SCALE_FACTOR/60)
                            self.laps['max_pace_in_min_per_100m_string'].append(
                                self._minutes2string(self.laps['max_pace_in_min_per_100m'][-1]))
                        if field.name == "total_elapsed_time":
                            self.laps['total_elapsed_time_in_min'].append(self._milliseconds2min(
                                field.raw_value))
                            self.laps['total_elapsed_time_in_min_string'].append(
                                self._minutes2string(self.laps['total_elapsed_time_in_min'][-1]))

    def _milliseconds2min(self, miliseconds):
        minutes = miliseconds/(1000*60)

        return minutes

    def _minutes2string(self, minutes):
        [minutes, rest] = str(minutes).split('.')
        seconds = round(float('0.' + rest)*60, 1)

        return str(minutes) + ":" + str(seconds).zfill(4)
