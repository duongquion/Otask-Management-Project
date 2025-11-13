def FormatProjectKey(name: str):
    initials = "".join(word[0].upper() for word in name.split())
    return initials