from enum import Enum

class Gender(str, Enum):
    MASCULINO = "masculino"
    FEMININO = "feminino"
    OUTRO = "outro"

class MaritalStatus(str, Enum):
    SOLTEIRO = "solteiro"
    CASADO = "casado"
    DIVORCIADO = "divorciado"
    VIUVO = "viuvo"

class FaithStage(str, Enum):
    INICIANTE = "iniciante"
    CAMINHANDO = "caminhando"
    ATUANTE = "atuante"

class EventPreference(str, Enum):
    PRESENCIAL = "presencial"
    DIGITAL = "digital"
    AMBOS = "ambos"
