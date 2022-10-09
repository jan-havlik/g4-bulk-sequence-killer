"""Module for calculating G4 score and mutating original sequences"""


class Sequence:
    """
    Class for operating with sequences
    """

    def __init__(self, seq: str, score_window: str = None, score_threshold: float = 1.1):
        self.sequence = seq.upper()
        # score since when the mutation begins
        self.score_threshold = score_threshold
        # sequence score
        self.score = 0.0
        # sequence containing extra base pairs on both ends for precise score calculation
        self.score_window = score_window
        """
        in the format
        position: x
        size: y
        """
        self.clusters = []

    def __repr__(self):  # type: ignore
        return f"{self.sequence} [{self.score}/{self.score_threshold}]"

    def calculate_score(self) -> None:
        """Original G4 score calc presented in https://academic.oup.com/nar/article/44/4/1746/1854457
        Subsequent G nucleotides yield bigger score (C nucleotide is the same, but negative)
        Final score is divided by the sequence length, that's why the maximum score is -4/4.

        Examples:
            CCC => -3-3-3 = -9 => -9 / 3 = -3
            GGGGGG => 4+4+4+4+4+4 = 24 => 24 / 6 = 4
            ATCCCAAGGGAA => 0+0-3-3-3+0+0+3+3+3+0+0 = 0 => 0 / 12 = 0
            ATGGATGGATGATGAT => 0+0+2+2+0+0+2+2+0+0+1+0+0+1+0+0 = 10 => 10 / 16 = 0.625
        """
        self.clusters = []
        prev = None

        for i, nuc in enumerate(self.score_window if self.score_window else self.sequence):
            if nuc == "G" or nuc == "C":
                if prev != nuc:
                    self.clusters.append({"pos": i, "size": 1, "nuc": nuc})
                else:
                    self.clusters[-1]["size"] += 1
            prev = nuc

        self.score = round(sum(
            [
                (cluster["size"] ** 2 if cluster["size"] < 4 else cluster["size"] * 4)
                * (-1 if cluster["nuc"] == "C" else 1)
                for cluster in self.clusters
            ]
        ) / len(self.score_window if self.score_window else self.sequence), 4)

    def over_threshold(self) -> bool:
        """Compares score with threshold

        Returns:
            bool: True if score is over threshold
        """
        self.calculate_score()
        # check whether the score is in given interval (too many G's > threshold, too many C's < threshold)
        return self.score > self.score_threshold or self.score < -abs(self.score_threshold)

    def mutate(self) -> None:
        """Mutating original sequence in order to descreasing final G4 score.
        Usually means that we break the clusters by replacing with the nuc_replacement (other nucleotide)
        or universal `W` (A or T) character.

        Args:
            nuc_replacement (str, optional): Replacing nucleotide. Defaults to 'W'.
        """
        complementary = True
        # locate the biggest possible cluster and reduce it until the score drops under threshold
        clusters = list(filter(
            lambda cluster: cluster["nuc"] == "G" if self.score > 0 else cluster["nuc"] == "C",
            sorted(
                self.clusters,
                key=lambda cluster: cluster["size"],
                reverse=True,
            ),
        ))

        try:
            start = clusters[0]["pos"]
            end = clusters[0]["size"]
            pos = start + end // 2
        except IndexError as exc:
            print("ERR: trying to mutate on complementary side")
            return

        self.sequence = "".join(
            (self.sequence[:pos], 'W' if self.score > 0 else 'D', self.sequence[pos + 1 :])
        )

