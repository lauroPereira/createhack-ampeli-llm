from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from .enums import Gender, MaritalStatus, FaithStage, EventPreference

class Member(BaseModel):
    user_id: Optional[int] = None
    nome_completo: str
    data_nascimento: date
    genero: Gender
    estado_civil: MaritalStatus
    email: str
    telefone: str
    tempo_igreja: str
    outras_igrejas: Optional[str] = None
    como_conheceu: str
    participacao_anterior: Optional[str] = None
    areas_interesse: List[str]
    habilidades_dons: Optional[str] = None
    voluntariar_area: Optional[str] = None
    dias_horarios_disponiveis: str
    preferencia_eventos: EventPreference
    interesse_em: List[str]  # discipulado, comunidade, cursos, evangelismo
    busca_na_igreja: str
    disposto_novos_grupos: bool
    preferencia_grupos: Optional[str] = None
    estagio_fe: FaithStage
    acompanhamento_pastoral: bool
    dificuldades_fe: Optional[str] = None
