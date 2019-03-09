

class Analyzer:

    def out(self, message):
        if isinstance(message, list):
            for s in message:
                self.out(s)
        else:
            print(message)
