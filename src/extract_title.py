def extract_title(markdown: str) -> str:
    """
    Return the first H1 header from the given markdown string.
    A valid H1 is a line that starts with a single '#' (allowing leading whitespace).
    Raises ValueError if no H1 is found or the H1 is empty after stripping.
    """
    for line in markdown.splitlines():
        stripped_left = line.lstrip()
        # must start with a single '#', not '##' or more
        if stripped_left.startswith("#") and not stripped_left.startswith("##"):
            title = stripped_left[1:].strip()
            if title:
                return title
            raise ValueError("Found H1 header but it is empty")
    raise ValueError("No H1 header found in markdown")