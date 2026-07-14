import re
from rapidfuzz import fuzz

from core.product import Product
from utils.text_cleaner import TextCleaner


class ProductParser:

    def __init__(self):

        self.cleaner = TextCleaner()

        self.manufacturers = {

            "SKF",
            "INA",
            "FAG",
            "NSK",
            "NTN",
            "TIMKEN",
            "FESTO",
            "SMC",
            "PARKER",
            "BOSCH",
            "BOSCH REXROTH",
            "SIEMENS",
            "ABB",
            "3M",
            "LOCTITE",
            "WURTH",
            "LINCOLN ELECTRIC",
            "ESAB",
            "KARCHER",
            "SEW",
            "NORGREN",
            "SICK",
            "IFM",
            "BALLUFF"

        }

    # -------------------------------------------------------

    def detect_manufacturer(self, text):

        best = ""
        score = 0

        upper = text.upper()

        for manufacturer in self.manufacturers:

            if manufacturer in upper:
                return manufacturer

            value = fuzz.partial_ratio(
                manufacturer,
                upper
            )

            if value > score:
                score = value
                best = manufacturer

        if score >= 90:
            return best

        return ""

    # -------------------------------------------------------

    def detect_part_number(self, text):

        patterns = [

            r"[A-Z]{1,5}-?\d{2,}[A-Z0-9/-]*",

            r"\d{3,}[A-Z/-]*",

            r"[A-Z0-9]+/[A-Z0-9]+",

            r"\d{4,}-?[A-Z0-9]+"

        ]

        for pattern in patterns:

            result = re.findall(pattern, text)

            if result:

                longest = max(result, key=len)

                return longest

        return ""

    # -------------------------------------------------------

    def detect_type(self, text):

        text = text.upper()

        keywords = {

            "ŁOŻYSKO": [
                "ŁOŻYSKO",
                "LOZYSKO"
            ],

            "USZCZELNIACZ": [
                "USZCZELNIACZ"
            ],

            "SIŁOWNIK": [
                "SIŁOWNIK",
                "SILOWNIK"
            ],

            "DRUT": [
                "DRUT"
            ],

            "ELEKTRODA": [
                "ELEKTRODA"
            ],

            "SMAR": [
                "SMAR"
            ],

            "TAŚMA": [
                "TAŚMA",
                "TASMA"
            ]

        }

        for item, words in keywords.items():

            for word in words:

                if word in text:

                    return item

        return ""

    # -------------------------------------------------------

    def build_search_query(self, product):

        query = []

        if product.detected_manufacturer:

            query.append(product.detected_manufacturer)

        if product.detected_part_number:

            query.append(product.detected_part_number)

        if len(query) == 0:

            query.append(product.cleaned_description)

        return " ".join(query)

    # -------------------------------------------------------

    def parse(self, product: Product):

        product.cleaned_description = self.cleaner.clean(
            product.description
        )

        product.detected_manufacturer = self.detect_manufacturer(
            product.cleaned_description
        )

        product.detected_part_number = self.detect_part_number(
            product.cleaned_description
        )

        product.product_type = self.detect_type(
            product.cleaned_description
        )

        product.search_query = self.build_search_query(
            product
        )

        confidence = 0

        if product.detected_manufacturer:
            confidence += 40

        if product.detected_part_number:
            confidence += 50

        if product.product_type:
            confidence += 10

        product.confidence = confidence

        return product
