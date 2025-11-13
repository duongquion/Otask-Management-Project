"""
Provides shared utility functions used across the project.
"""

def FormatProjectKey(name: str):
    """
    Generate a project key from a project name by taking the first
    letter of each word and converting them to uppercase.

    Example:
        "Otask Project" -> "OP"
    """
    initials = "".join(word[0].upper() for word in name.split())
    return initials
