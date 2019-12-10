from minion import Minion


class Minions:
    @staticmethod
    def new(name):
        if name == 'Righteous Protector':
            instance = Minion(name, 1, 1, 1, taunt=True, bubble=True)
        elif name == 'Voidwalker':
            instance = Minion(name, 1, 3, 1, type='Demon', taunt=True)

        elif name == 'Annoy-o-Tron':
            instance = Minion(name, 1, 2, 2, type='Mech', taunt=True, bubble=True)
        elif name == 'Nightmare Amalgam':
            instance = Minion(name, 3, 4, 2, type='All')
        elif name == 'Shielded Minibot':
            instance = Minion(name, 2, 2, 2, type='Mech', bubble=True)

        elif name == 'Psych-o-Tron':
            instance = Minion(name, 3, 4, 3, type='Mech', taunt=True, bubble=True)
        
        return instance