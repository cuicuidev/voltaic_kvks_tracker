import numpy as np
from scipy.interpolate import interp1d

RANKS = ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Jade", "Master", "Grandmaster", "Nova", "Astra", "Celestial"]
SUBRANKS = ["I", "II", "C"]

def equal_spacing_transform(value, thresholds):
    thresholds = np.array(thresholds)

    min_val = thresholds.min()
    max_val = thresholds.max()
    normalized_thresholds = (thresholds - min_val) / (max_val - min_val)

    n = len(thresholds)
    equal_spacing = np.linspace(0, 1, n)

    interpolation_function = interp1d(normalized_thresholds, equal_spacing, kind='linear', fill_value="extrapolate")
    
    normalized_value = (value - min_val) / (max_val - min_val)
    transformed_value = interpolation_function(normalized_value)

    return transformed_value

class Scenario:

    def __init__(self, name, thresholds) -> None:
        self.name = name
        self.thresholds = thresholds

    def get_rank(self, score):
        progress = equal_spacing_transform(score, [0]+self.thresholds)
        rank = "Unranked"
        goal = equal_spacing_transform(self.thresholds[0], [0]+self.thresholds)
        for i, threshold in enumerate(self.thresholds):
            if score >= threshold:
                rank = RANKS[i]
                if i < len(RANKS) - 1:
                    goal = equal_spacing_transform(self.thresholds[i+1], [0]+self.thresholds)
                else:
                    goal = 1
        return score, rank, progress, goal
 
class Clicking:

    def __init__(self) -> None:
        self.dynamic_scenarios = [
            Scenario("pasu_easy", [40,50,56,66,75]),
            Scenario("b180_easy", [52,61,70,77,86]),
            Scenario("popcorn_easy", [100,150,200,250,310])
        ]

        self.static_scenarios = [
            Scenario("ww3t", [83,93,103,113,123]),
            Scenario("1w4ts", [70, 82, 91, 100, 110]),
            Scenario("6_sphere_hipfire", [95, 108, 120, 132, 142])
        ]

    def dynamic_rank(self, scores) -> tuple[str, str]:
        ranks = [scen.get_rank(score)[1] for scen, score in zip(self.dynamic_scenarios, scores)]
        best = "Unrated"
        for rank in RANKS:
            if rank in ranks:
                best = rank
        repeats = len([r for r in ranks if r == best])
        subrank = SUBRANKS[repeats-1]
        if best == "Unrated":
            subrank = ""
        return best, subrank

    def static_rank(self, scores) -> tuple[str, str]:
        ranks = [scen.get_rank(score)[1] for scen, score in zip(self.static_scenarios, scores)]
        best = "Unrated"
        for rank in RANKS:
            if rank in ranks:
                best = rank
        repeats = len([r for r in ranks if r == best])
        subrank = SUBRANKS[repeats-1]
        if best == "Unrated":
            subrank = ""
        return best, subrank

    def get_ranks(self, scores) -> list:
        scenarios = self.dynamic_scenarios + self.static_scenarios
        return [scenario.get_rank(score) for scenario, score in zip(scenarios, scores)]

class Tracking:

    def __init__(self, log=False) -> None:
        self.precise_scenarios = [
            Scenario("smoothbot_easy", [1700,2100,2400,2800,3100]),
            Scenario("air_angelic_4_easy", [1800,2200,2600,3000,3300]),
            Scenario("pgti_easy", [700,1000,1300,1600,1900])
        ]
        self.reactive_scenarios = [
            Scenario("fuglaaxyz_easy", [7500,8500,10000,12000,14000]),
            Scenario("ground_plaza_easy", [835, 845, 855, 870, 880]),
            Scenario("air_easy", [775, 800, 825, 852, 865])
        ]
        self.log = log
        if log:
            for scen in self.precise_scenarios:
                scen.thresholds = [np.log(x) for x in scen.thresholds]
            for scen in self.reactive_scenarios:
                scen.thresholds = [np.log(x) for x in scen.thresholds]

    def precise_rank(self, scores):
        if self.log:
            scores = [np.log(score) for score in scores]
        ranks = [scen.get_rank(score)[1] for scen, score in zip(self.precise_scenarios, scores)]
        best = "Unrated"
        for rank in RANKS:
            if rank in ranks:
                best = rank
        repeats = len([r for r in ranks if r == best])
        subrank = SUBRANKS[repeats-1]
        if best == "Unrated":
            subrank = ""
        return best, subrank


    def reactive_rank(self, scores):
        if self.log:
            scores = [np.log(score) for score in scores]
        ranks = [scen.get_rank(score)[1] for scen, score in zip(self.reactive_scenarios, scores)]
        best = "Unrated"
        for rank in RANKS:
            if rank in ranks:
                best = rank
        repeats = len([r for r in ranks if r == best])
        subrank = SUBRANKS[repeats-1]
        if best == "Unrated":
            subrank = ""
        return best, subrank

    def get_ranks(self, scores) -> list:
        if self.log:
            scores = [np.log(score) for score in scores]
        scenarios = self.precise_scenarios + self.reactive_scenarios
        return [scenario.get_rank(score) for scenario, score in zip(scenarios, scores)]

class Switching:

    def __init__(self, log=False) -> None:
        self.speed_scenarios = [
            Scenario("patts_easy", [65,80,85,91,98]),
            Scenario("psalmts_easy", [50,58,67,76,85]),
            Scenario("voxts_easy", [74,82,90,100,109])
        ]
        self.evasive_scenarios = [
            Scenario("kints_easy", [45,54,60,66,72]),
            Scenario("b180t_easy", [40, 51, 60, 69, 77]),
            Scenario("smoothbot_ts_easy", [35, 42, 46, 50, 54])
        ]
        self.log = log
        if log:
            for scen in self.speed_scenarios:
                scen.thresholds = [np.log(x) for x in scen.thresholds]
            for scen in self.evasive_scenarios:
                scen.thresholds = [np.log(x) for x in scen.thresholds]

    def speed_rank(self, scores):
        if self.log:
            scores = [np.log(score) for score in scores]
        ranks = [scen.get_rank(score)[1] for scen, score in zip(self.speed_scenarios, scores)]
        best = "Unrated"
        for rank in RANKS:
            if rank in ranks:
                best = rank
        repeats = len([r for r in ranks if r == best])
        subrank = SUBRANKS[repeats-1]
        if best == "Unrated":
            subrank = ""
        return best, subrank


    def evasive_rank(self, scores):
        if self.log:
            scores = [np.log(score) for score in scores]
        ranks = [scen.get_rank(score)[1] for scen, score in zip(self.evasive_scenarios, scores)]
        best = "Unrated"
        for rank in RANKS:
            if rank in ranks:
                best = rank
        repeats = len([r for r in ranks if r == best])
        subrank = SUBRANKS[repeats-1]
        if best == "Unrated":
            subrank = ""
        return best, subrank

    def get_ranks(self, scores) -> list:
        if self.log:
            scores = [np.log(score) for score in scores]
        scenarios = self.speed_scenarios + self.evasive_scenarios
        return [scenario.get_rank(score) for scenario, score in zip(scenarios, scores)]
