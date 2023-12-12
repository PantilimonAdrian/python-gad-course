# Tasks 1 - Define class "Fractie" and implement the following
# methods init, str, add, sub and inverse

class Fractie:
    def __init__(self, numarator, numitor):
        if numitor == 0:
            raise ValueError("Numitorul unei fractii nu poate fi zero.")
        self.numarator = numarator
        self.numitor = numitor
        self.simplificare_fractie()

    def __str__(self):
        return f"{self.numarator}/{self.numitor}"

    def __add__(self, second_function):
        numarator_nou = self.numarator * second_function.numitor + second_function.numarator * self.numitor
        numitor_nou = self.numitor * second_function.numitor
        fractie_rezultat = Fractie(numarator_nou, numitor_nou)
        return fractie_rezultat

    def __sub__(self, second_function):
        numarator_nou = self.numarator * second_function.numitor - second_function.numarator * self.numitor
        numitor_nou = self.numitor * second_function.numitor
        fractie_rezultat = Fractie(numarator_nou, numitor_nou)
        return fractie_rezultat

    def inverse(self):
        if self.numarator != 0:
            return Fractie(self.numitor, self.numarator)
        else:
            raise ValueError("Fractia nu are inversa, deoarece numitorul nu poate fi 0!")

    def simplificare_fractie(self):

        cmmdc = self.gcd(self.numarator, self.numitor)
        self.numarator = self.numarator // cmmdc
        self.numitor = self.numitor // cmmdc


    def gcd(self, a, b):
        # Algoritmul lui euclid imparire
        while b:
            a, b = b, a % b
        return a


if __name__ == "__main__":
    fractie1 = Fractie(1, 2)
    fractie2 = Fractie(3, 4)

    suma_fractii = fractie1 + fractie2
    diferenta_fractii = fractie1 - fractie2
    inversa_fractie1 = fractie1.inverse()
    inversa_fractie2 = fractie2.inverse()

    print(f"Fractie1: {fractie1}")
    print(f"Fractie2: {fractie2}")
    print(f"Suma fractii: {suma_fractii}")
    print(f"Diferenta fractii: {diferenta_fractii}")
    print(f"Inversa fractie1: {fractie1.inverse()}")
    print(f"Inversa fractie2: {fractie2.inverse()}")

    # Simplificare fractie
    fractie3 = Fractie(6, 9)
    print(f"Fractie3 simplificata: {fractie3}")

    # Fractie cu numitor 0
    try:
        fractie4 = Fractie(6, 0)
    except Exception as e:
        print(f"Eroare: {e}")
    # print(f"Fractie4 cu numitor0: {fractie4}")

    # Inversare fractie cu numarator 0
    try:
        fractie5 = Fractie(0, 15)
        fractie5.inverse()
    except Exception as e:
        print(f"Eroare: {e}")