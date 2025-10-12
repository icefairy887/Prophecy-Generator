import random

def default_tokenize(text: str):
    return text.split()

class MarkovModel:
    def __init__(self, n=2):
        self.n = n
        self.trans_counts = {}

    def fit(self, corpora, tokenize=default_tokenize):
        for text in corpora:
            tokens = tokenize(text)
            for i in range(len(tokens) - self.n):
                state = tuple(tokens[i:i+self.n])
                nxt = tokens[i+self.n]
                self.trans_counts.setdefault(state, {}).setdefault(nxt, 0)
                self.trans_counts[state][nxt] += 1

    def dump(self):
        return {"n": self.n, "trans_counts": self.trans_counts}

    @classmethod
    def load(cls, data):
        m = cls(n=data["n"])
        m.trans_counts = data["trans_counts"]
        return m


class LuminaGenerator:
    def __init__(self, model, equation, temperature=1.0, rng=None):
        self.model = model
        self.eq = equation
        self.temperature = temperature
        self.rng = rng or random.Random()

    def generate(self, seed, max_tokens=80, stop=None):
        history = list(seed)
        state = tuple(seed[-self.model.n:])
        out = []

        for t in range(max_tokens):
            candidates = self.model.trans_counts.get(state, {})
            if not candidates:
                break

            weighted = []
            for cand, count in candidates.items():
                w = count * self.eq.weight(history, state, cand, t)
                if w > 0:
                    weighted.append((cand, w))

            if not weighted:
                break

            total = sum(w for _, w in weighted)
            r = self.rng.uniform(0, total)
            upto = 0
            for cand, w in weighted:
                upto += w
                if upto >= r:
                    out.append(cand)
                    history.append(cand)
                    state = tuple((list(state) + [cand])[-self.model.n:])
                    break

            if stop and out[-1] in stop:
                break

        return out
