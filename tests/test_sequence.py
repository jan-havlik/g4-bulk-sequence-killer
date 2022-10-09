import pytest

from src.sequence import Sequence
from src.helpers.complement import get_complementary_sequence


@pytest.mark.parametrize("sequence,score",
    [
        ("CCC", -3),
        ("GGGGGG", 4),
        ("ATCCCAAGGGAA", 0),
        ("ATGGATGGATGATGAT", 0.625),
        ("GATCCACTTGGCTACATCCGCCCCC", -1),
        ("ATCCACTTGGCTACATCCGCCCCCT", -1.04),
        ("TCCACTTGGCTACATCCGCCCCCTT", -1.04),
        ("CCACTTGGCTACATCCGCCCCCTTA", -1.04)
    ]
)
def test_score(sequence, score):
    seq = Sequence(sequence)
    seq.calculate_score()
    assert seq.score == score

@pytest.mark.parametrize("sequence, mutated, score",
    [
        ("CCC", "CCC", -3),
        ("GGGGGG", "GWGWGW", 0.5),
        ("ATCCCAAGGGAA", "ATCCCAAGGGAA", 0),
        ("ATGGATGGATGATGAT", "ATGWATGGATGATGAT", 0.4375),
        ("GATCCACTTGGCTACATCCGCCCCC", "GATCCACTTGGCTACATCCGCCCCC", -1),
        ("ATCCACTTGGCTACATCCGCCCCCT", "ATCCACTTGGCTACATCCGCCCCCT", -1.04),
        ("TCCACTTGGCTACATCCGCCCCCTT", "TCCACTTGGCTACATCCGCCCCCTT", -1.04),
        ("CCACTTGGCTACATCCGCCCCCTTA", "CCACTTGGCTACATCCGCCCCCTTA", -1.04)
    ]
)
def test_mutation(sequence, mutated, score):
    seq = Sequence(sequence, score_threshold=0.5)  # ensure mutation is done

    while seq.over_threshold():
        seq.mutate()
    
    assert seq.sequence == mutated
    assert seq.score == score


@pytest.mark.parametrize("sequence, mutated, score",
    [
        ("CCC", "WWG", 0.3333),
        ("GGGGGG", "CCCCCC", -4.0),
        ("ATCCCAAGGGAA", "TAGGGTTCCCTT", 0),
        ("ATGGATGGATGATGAT", "TACCTACCTACTACTA", -0.625),
        ("GATCCACTTGGCTACATCCGCCCCC", "CTAGWTGAACCGATGTAGGCGGWGG", 0.4),
        ("ATCCACTTGGCTACATCCGCCCCCT", "TAGWTGAACCGATGTAGGCGGWGGA", 0.44),
        ("TCCACTTGGCTACATCCGCCCCCTT", "AGWTGAACCGATGTAGGCGGWGGAA", 0.44),
        ("CCACTTGGCTACATCCGCCCCCTTA", "GWTGAACCGATGTAGGCGGWGGAAT", 0.44)
    ]
)
def test_mutation_complementary(sequence, mutated, score):
    seq = Sequence(get_complementary_sequence(sequence), score_threshold=0.5)  # ensure mutation is done

    while seq.over_threshold():
        seq.mutate()
    
    assert seq.sequence == mutated
    assert seq.score == score