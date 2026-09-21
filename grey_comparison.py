class GreyNumber:
    def __init__(self, low, up):
        self.low = low
        self.up = up

def probability_greater(a: GreyNumber, b: GreyNumber) -> float:
    low_a, up_a = a.low, a.up
    low_b, up_b = b.low, b.up

    if low_a > up_b:
        return 1
    elif low_b > up_a:
        return 0
    elif low_a == low_b or up_a == up_b:
        raise ValueError("Lower or upper bounds of compared grey numbers are equal; this case is not supported for comparison.")
    elif low_a < low_b < up_a < up_b:
        return (up_a - low_b) ** 2 / (2 * (up_a - low_a) * (up_b - low_b))
    elif low_b < low_a < up_b < up_a:
        return 1 - (up_b - low_a) ** 2 / (2 * (up_a - low_a) * (up_b - low_b))
    elif low_b < low_a < up_a < up_b:
        return (low_a + up_a - 2 * low_b) / (2 * (up_b - low_b))
    elif low_a < low_b < up_b < up_a:
        return (2 * up_a - up_b - low_b) / (2 * (up_a - low_a))
    else:
        raise ValueError("Sorry, this case is not supported")

class GreyNumberBatchComparator:
    def __init__(self, grey_numbers):
        self.numbers = [GreyNumber(low, up) for low, up in self.adjust_equal_bounds(grey_numbers)]

    def adjust_equal_bounds(self, grey_numbers):
        epsilon = 1e-7
        n = len(grey_numbers)
        lows = [low for low, up in grey_numbers]
        ups = [up for low, up in grey_numbers]

        combined = []
        for i in range(n):
            combined.append((lows[i], i, 'low'))
            combined.append((ups[i], i, 'up'))

        combined.sort(key=lambda x: x[0])

        for i in range(1, len(combined)):
            prev_val, prev_idx, prev_type = combined[i-1]
            cur_val, cur_idx, cur_type = combined[i]
            if cur_val <= prev_val + 1e-12:
                combined[i] = (prev_val + epsilon, cur_idx, cur_type)

        for val, idx, t in combined:
            if t == 'low':
                lows[idx] = val
            else:
                ups[idx] = val

        return list(zip(lows, ups))

    def probability_greater(self, a, b):
        return probability_greater(a, b)

    def compare_all_pairs(self):
        results = []
        n = len(self.numbers)
        for i in range(n):
            for j in range(i + 1, n):
                try:
                    prob = self.probability_greater(self.numbers[i], self.numbers[j])
                    results.append(f"Possibility (X{i+1} > X{j+1}) = {prob:.7f}")
                except ValueError as e:
                    results.append(f"Error comparing X{i+1} and X{j+1}: {str(e)}")
        return "\n".join(results)


class MinimaxRegretApproach:
    def __init__(self, grey_numbers):
        self.numbers = [{"low": low, "up": up} for low, up in grey_numbers]
        self.n = len(self.numbers)
        self.ranks = [0] * self.n

    def compute_max_regret(self, current_indices):
        max_regrets = []
        for i in current_indices:
            low_i = self.numbers[i]["low"]
            up_i = self.numbers[i]["up"]
            regrets = []
            for j in current_indices:
                if i == j:
                    continue
                low_j = self.numbers[j]["low"]
                up_j = self.numbers[j]["up"]
                regret = max(0, up_j - low_i)
                regrets.append(regret)
            max_regrets.append((i, max(regrets) if regrets else 0))
        return max_regrets

    def rank_numbers(self):
        remaining = list(range(self.n))
        current_rank = self.n

        while remaining:
            max_regrets = self.compute_max_regret(remaining)
            min_regret_value = min(x[1] for x in max_regrets)
            candidates = [x[0] for x in max_regrets if x[1] == min_regret_value]
            chosen = candidates[0]

            self.ranks[chosen] = current_rank
            current_rank -= 1
            remaining.remove(chosen)

        sorted_indices = sorted(range(self.n), key=lambda i: self.ranks[i], reverse=True)
        return sorted_indices, self.ranks
