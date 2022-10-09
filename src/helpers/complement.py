

def get_complementary_sequence(seq: str) -> str:
    complement = ""
    for c in seq:
        if c == 'G':
            complement += 'C'
        elif c == 'C':
            complement += 'G'
        elif c == 'A':
            complement += 'T'
        elif c == 'T':
            complement += 'A'
        else:
            complement += c
    return complement