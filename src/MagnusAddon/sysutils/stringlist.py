def remove_duplicates(text: list[str]) -> list[str]:
    unique_list = []
    for item in text:
        if item not in unique_list:
            unique_list.append(item)

    return unique_list