import random


def roll_d(size):
    return random.randint(1, size)


def roll_nd(quantity, size):
    return [roll_d(size) for _ in range(quantity)]


def summarize(dice, mod: str) -> str:
    i_mod = 0
    if mod is not None:
        i_mod = int(mod)

    results = []
    for d in dice:
        siz = int(d[0])
        qtd = int(d[1])
        results.extend([roll_d(qtd) for _ in range(siz)])
    return f"{results} {str(mod or '')}: {sum(results)+i_mod}"
