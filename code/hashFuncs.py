import io



class hashFunc:
    """
    This is a simple base class that will define the bare minimal functionality,
    basically a guideline of calls that will be used in the general code

    :Suffix => HASH
    """

    def __init__(self, module, **kwargs):
        self.module = module
    #placeholder
    def encode(self, key: str) -> int:
        position = ""
        for c in key:
            # ord seems to be ify with UTF, but it works and this is a placeholder function
            position = position + str(ord(c))
        position = int(position)
        return position % self.module


