"""Simple sorting algorithm visualizer helper."""


def bubble_sort(values: list[int]) -> list[list[int]]:
    steps: list[list[int]] = [values[:]]
    working = values[:]
    for i in range(len(working)):
        for j in range(0, len(working) - i - 1):
            if working[j] > working[j + 1]:
                working[j], working[j + 1] = working[j + 1], working[j]
                steps.append(working[:])
    return steps

