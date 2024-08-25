RANKS = ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Jade", "Master", "Grandmaster", "Nova", "Astra", "Celestial"]
SUBRANKS = ["I", "II", "C"]

class Scenario:

    def __init__(self, name, thresholds) -> None:
        self.name = name
        self.thresholds = thresholds

    def get_rank(self, score):
        progress = score/self.thresholds[-1]
        rank = RANKS[0]
        for i, threshold in enumerate(self.thresholds):
            if score >= threshold:
                rank = RANKS[i+1]
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
        best = "Bronze"
        for rank in RANKS:
            if rank in ranks:
                best = rank
        repeats = len([r for r in ranks if r == best])
        subrank = SUBRANKS[repeats-1]
        return best, subrank

    def static_rank(self, scores) -> tuple[str, str]:
        ranks = [scen.get_rank(score)[1] for scen, score in zip(self.static_scenarios, scores)]
        best = "Bronze"
        for rank in RANKS:
            if rank in ranks:
                best = rank
        repeats = len([r for r in ranks if r == best])
        subrank = SUBRANKS[repeats-1]
        return best, subrank

    def get_ranks(self, scores) -> list:
        scenarios = self.dynamic_scenarios + self.static_scenarios
        return [scenario.get_rank(score) for scenario, score in zip(scenarios, scores)]
