from enum import Enum

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

class Scenarios(Enum):
    PASU_EASY = Scenario("pasu_easy", [40,50,56,66,75])
    B180_EASY = Scenario("b180_easy", [52,61,70,77,86])
    POPCORN_EASY = Scenario("popcorn_easy", [100,150,200,250,310])
    WW3T = Scenario("ww3t", [83,93,103,113,123]),
    _1W4TS = Scenario("1w4ts", [70, 82, 91, 100, 110]),
    _6SH = Scenario("6_sphere_hipfire", [95, 108, 120, 132, 142])
    
    SMOOTHBOT_EASY = Scenario("smoothbot_easy", [1700,2100,2400,2800,3100]),
    AIR_ANGELIC_4_EASY = Scenario("air_angelic_4_easy", [1800,2200,2600,3000,3300]),
    PGTI_EASY = Scenario("pgti_easy", [700,1000,1300,1600,1900])
    FUGLAAXYZ_EASY = Scenario("fuglaaxyz_easy", [7500,8500,10000,12000,14000]),
    GP_EASY = Scenario("ground_plaza_easy", [835, 845, 855, 870, 880]),
    AIR_EASY = Scenario("air_easy", [775, 800, 825, 852, 865])
    
    PATTS_EASY = Scenario("patts_easy", [65,80,85,91,98]),
    PSALMTS_EASY = Scenario("psalmts_easy", [50,58,67,76,85]),
    VOXTS_EASY = Scenario("voxts_easy", [74,82,90,100,109])
    KINTS_EASY = Scenario("kints_easy", [45,54,60,66,72]),
    B180T_EASY = Scenario("b180t_easy", [40, 51, 60, 69, 77]),
    SMOOTHBOT_TS_EASY = Scenario("smoothbot_ts_easy", [35, 42, 46, 50, 54])

class ScenarioCluster:

    def __init__(self, name, scenarios):
        self.name = name
        self.scenarios = scenarios

    def evaluate(self, scores):
        assert len(scores) == len(self.scenarios)
        return [scenario.get_rank(score) for scenario, score in zip(self.scenarios, scores)]


class Benchmark:

    def __init__(self, name: str, clusters: list[ScenarioCluster]) -> None:
        self.name = name
        self.clusters = clusters

    def get_rank(self, scores, cluster_name) -> tuple[str, str]:
        matching_clusters = [cluster for cluster in self.clusters if cluster.name == cluster_name]
        assert len(matching_clusters) == 1
        scenarios = matching_clusters[0].scenarios

        ranks = [scen.get_rank(score)[1] for scen, score in zip(scenarios, scores)]
        best = "Iron"
        for rank in RANKS:
            if rank in ranks:
                best = rank
        repeats = len([r for r in ranks if r == best])
        subrank = SUBRANKS[repeats-1]
        if best == "Iron":
            subrank = ""
        return best, subrank

    def get_ranks(self, scores, cluster_name) -> list:
        return [scenario.get_rank(score) for scenario, score in zip(self.scenarios, scores)]
