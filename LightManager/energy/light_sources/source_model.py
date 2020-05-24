

class LightSource():

    def __init__(self, *, name, type, efficacy, description):
        """
        Create a new light source

        :param  name: Source name
        :type   name: str()

        :param  type: Source type (unique type for internal use)
        :type   type: str()

        :param  efficacy: Light source efficacy, low efficacy cause a lot of energy lose
        :type   efficacy: int()

        :param  description: Source type description for user
        :type   description: str()
        """

        self.name = name
        self.type = type
        self.efficacy = efficacy
        self.description = description