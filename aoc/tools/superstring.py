class SuperString(str):
    """Additional functions for strings that are adapted to AoC"""

    def split(self, characters:str|list[str]=None)->list[str]:
        """Can now split with several characters! No need for Regex"""
        if characters is None or isinstance(characters, str):
            return super().split(characters)
        elif isinstance(characters, list):
            if any([not isinstance(e, str) for e in characters]):
                raise TypeError(
                    f'In {self.__class__.__name__}.split, check arguments:\n'\
                    f'characters = {characters}'
                )
            else:
                result = [str(self)]
                for c in characters:
                    result = [
                        subsubself 
                        for subself in result
                        for subsubself in subself.split(c) 
                        if subsubself != ''
                    ]
                return result
        else:
            raise TypeError(
                f'In {self.__class__.__name__}.split, check arguments:\n'\
                f'characters = {characters}'
            )
