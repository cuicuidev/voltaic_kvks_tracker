RANKS = ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Jade", "Master", "Grandmaster", "Nova", "Astra", "Celestial"]
SUBRANKS = ["I", "II", "C"]

class Scenario:

    def __init__(self, name, thresholds) -> None:
        self.name = name
        self.thresholds = thresholds

    def get_rank(self, score):
        progress = score/self.thresholds[-1]
        rank = "Unranked"
        for i, threshold in enumerate(self.thresholds):
            if score >= threshold:
                rank = RANKS[i]
        return score, rank, progress
 
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

    def __init__(self) -> None:
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

    def precise_rank(self, scores):
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
        scenarios = self.precise_scenarios + self.reactive_scenarios
        return [scenario.get_rank(score) for scenario, score in zip(scenarios, scores)]

class Switching:

    def __init__(self) -> None:
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

    def speed_rank(self, scores):
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
        scenarios = self.speed_scenarios + self.evasive_scenarios
        return [scenario.get_rank(score) for scenario, score in zip(scenarios, scores)]
