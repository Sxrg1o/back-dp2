"""
Mesa mapper for converting between models and schemas.
"""
from typing import List

from app.models.mesa import Mesa
from app.schemas.mesa import MesaResponse, MesaListResponse


class MesaMapper:
    """Mapper for Mesa model and schemas."""
    
    @staticmethod
    def to_response(mesa: Mesa) -> MesaResponse:
        """Convert Mesa model to MesaResponse schema."""
        return MesaResponse.from_orm(mesa)
    
    @staticmethod
    def to_list_response(mesa: Mesa) -> MesaListResponse:
        """Convert Mesa model to MesaListResponse schema."""
        return MesaListResponse.from_orm(mesa)
    
    @staticmethod
    def to_response_list(mesas: List[Mesa]) -> List[MesaResponse]:
        """Convert list of Mesa models to list of MesaResponse schemas."""
        return [MesaMapper.to_response(mesa) for mesa in mesas]
    
    @staticmethod
    def to_list_response_list(mesas: List[Mesa]) -> List[MesaListResponse]:
        """Convert list of Mesa models to list of MesaListResponse schemas."""
        return [MesaMapper.to_list_response(mesa) for mesa in mesas]


# Create mapper instance
mesa_mapper = MesaMapper()