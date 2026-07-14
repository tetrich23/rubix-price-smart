from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Product:

    row_number: int

    material: str = ""

    description: str = ""

    manufacturer: str = ""

    manufacturer_part_number: str = ""

    quantity: float = 0

    unit: str = ""

    price: float = 0

    currency: str = ""

    #####################################################

    detected_manufacturer: str = ""

    detected_part_number: str = ""

    cleaned_description: str = ""

    search_query: str = ""

    confidence: int = 0

    #####################################################

    rubix_found: bool = False

    rubix_price: Optional[float] = None

    rubix_url: str = ""

    rubix_name: str = ""

    #####################################################

    internet_found: bool = False

    internet_price: Optional[float] = None

    internet_url: str = ""

    internet_source: str = ""

    #####################################################

    status: str = "NEW"

    notes: list = field(default_factory=list)
