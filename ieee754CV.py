from cmath import log
from re import I


class IEEE754():

    PRECISION = {  # Basi supportate (FLOAT, DOUBLE e DOUBLE128)
        "FLOAT32" : 
        {
            "esp" : 8,
            "baise" : 127,
            "m_bits" : 23
        },

        "DOUBLE64" :
        {
            "esp" : 11,
            "baise" : 1023,
            "m_bits" : 52
        },

        "PRECISION_SUPPORTED" : {"FLOAT32", "DOUBLE64"}
    }

    __CURRENT_PR = ""  # Precisione usata per calcolare il numero
    __SHIFT = 0 # Esponente calcolato nel metodo E(n)
    __MANTISSA = []
    __SIGN = 0 # Segno del numero converito
    __NUM = 0 # Numero da convertire


    def __init__(self, precision = "FLOAT32"):
        if precision in IEEE754.PRECISION["PRECISION_SUPPORTED"]:
            IEEE754.__CURRENT_PR= precision
        else:
            IEEE754.__CURRENT_PR = "FLOAT32"

    def __dec_to_bin(self, n):
        result = []
        i = 0
        while(n > 0):
            i+=1
            if (n%2==0):
                result.append(0)
            else:
                result.append(1)
            n //= 2
        
        return ''.join(map(str, result[::-1]))
    
    def S(self, n):
        if n > 0 :
            return 0;
        IEEE754.__SIGN = 1
        return 1;

    def E(self, n):
        IEEE754.__SHIFT = int(abs((log(abs(n), 2) / log(2, 2))))
        esp = IEEE754.PRECISION[IEEE754.__CURRENT_PR]["baise"] + IEEE754.__SHIFT
        return IEEE754.__dec_to_bin(self, esp)

    def M(self, n):
        result = []
        i = 0
        op= 0
        start = abs(n) / pow(2, IEEE754.__SHIFT)
        if start > 1 and start < 2:
            start -=1
        op = start * 2;
        result.append(int(op))

        while(i < IEEE754.PRECISION[IEEE754.__CURRENT_PR]["m_bits"] - 1) :
            if op > 1 and op < 2:
                op -= 1
            if op == 2 or op > 2 or op == 1.0:
                op = 0
            else:
                op = op * 2;
            i+=1
            result.append(int(op))
        IEEE754.__MANTISSA = result
        return result

    def convert(self, num : float) -> str:
        IEEE754.__NUM = num
        s = self.S(num)
        e = self.E(num)
        m = self.M(num)
        return str(s) + " " + e + " " + ''.join(map(str, m))

    def checksum(self) -> float:
        i = 0
        sum = 1
        while i < IEEE754.PRECISION[IEEE754.__CURRENT_PR]["m_bits"] :
            i+=1
            sum += IEEE754.__MANTISSA[i - 1] * pow(2, (i - (i*2)))
        ner = (sum) * pow(-1, IEEE754.__SIGN)
        return ner * pow(2, IEEE754.__SHIFT)   
    
    def get_precision(self) -> str:
        return IEEE754.__CURRENT_PR