import random
import pandas as pd
from time import time

def roll():
    """Roll a single d20."""

    result = random.randint(1, 20)

    return result


def advantage():
    first = roll()
    second = roll()

    highest = max(first, second)

    return highest


def disadvantage():
    first = roll()
    second = roll()

    lowest = min(first, second)

    return lowest
    

def advantage_disadvantage():
    """Roll twice with disadvantage and keep the higher result."""

    first = disadvantage()
    second = disadvantage()

    highest = max(first, second)

    return highest


def disadvantage_advantage():
    """Roll twice with advantage and keep the lower result."""

    first = advantage()
    second = advantage()

    lowest = min(first, second)

    return lowest


def create_test_set(function_name, iterations):
    """Take a function name and number of iterations to run and use it to create a test set of results."""

    result_set = []

    for iteration in range(iterations):

        result_set.append(function_name())

    return result_set


def analyze_roll(roll_type, iterations=10000):
    """Return analysis of a test set of a given roll type."""

    test_set = create_test_set(roll_type, iterations)

    test_series = pd.Series(test_set)

    return test_series.describe()


def generate_percentage_success_series(roll_name, iterations=1000000):
    """Create a series of percentages of success to get higher than numbers from 1 to 20 for a roll type."""

    test_set = create_test_set(roll_name, iterations)
    
    test_series = pd.Series(test_set)

    values = test_series.value_counts(normalize=True)

    values_sorted = values.sort_index()

    values_cumulative = values_sorted.cumsum()

    values_reversed = values_cumulative.apply(lambda x: 1.0 - x)

    return values_reversed
        

rolls_to_test = {
    "Regular die": roll,
    "advantage": advantage,
    "disadvantage": disadvantage,    
    "Advantage of disadvantage": advantage_disadvantage,
    "Disadvantage of advantage": disadvantage_advantage
}

success_values = {}

for roll_name in rolls_to_test:
    success_values[roll_name] = generate_percentage_success_series(rolls_to_test[roll_name])

df = pd.DataFrame(success_values)

df = df.round(4)

# print(df.info())
    
for roll_name in rolls_to_test:
    print(roll_name)
    print()
    t1 = time()
    print(analyze_roll(rolls_to_test[roll_name], iterations=1000000))
    t2 = time()
    print('Analysis complete in', str(t2 - t1), 'seconds')
    print('\n')




