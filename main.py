from excel.reader import ExcelReader
from excel.analyzer import ExcelAnalyzer

from core.factory import ProductFactory
from core.parser import ProductParser

from utils.text_cleaner import TextCleaner


def main():

    print("=" * 80)
    print("WYCENIACZ RUBIX")
    print("=" * 80)

    # ----------------------------------------------------
    # ŚCIEŻKA DO PLIKU
    # ----------------------------------------------------

    file = "Kopia pliku RUBIX FILE 2025-2026.xlsx"

    # ----------------------------------------------------
    # WCZYTYWANIE EXCELA
    # ----------------------------------------------------

    reader = ExcelReader(file)

    info = reader.file_info()

    print("\nPlik:", info["name"])
    print("Arkusze:", info["sheets"])

    # ----------------------------------------------------
    # Wczytanie arkusza
    # ----------------------------------------------------

    df = reader.load_sheet("Data")

    # ----------------------------------------------------
    # Analiza
    # ----------------------------------------------------

    analyzer = ExcelAnalyzer(df)

    report = analyzer.summary()

    print("\n")
    print("=" * 80)
    print("RAPORT")
    print("=" * 80)

    print(f"Liczba wierszy               : {report['rows']}")
    print(f"Liczba kolumn               : {report['columns']}")
    print(f"Duplikaty                   : {report['duplicates']}")
    print(f"Puste wiersze               : {report['empty_rows']}")
    print(f"Puste komórki               : {report['empty_cells']}")
    print(f"Producentów                 : {report['manufacturers']}")
    print(f"Numery katalogowe           : {report['part_numbers']}")
    print(f"Bez numeru katalogowego     : {report['without_part_numbers']}")

    print("\n")

    print("=" * 80)
    print("WYKRYTE KOLUMNY")
    print("=" * 80)

    for key, value in report["mapping"].items():
        print(f"{key:20} -> {value}")

    # ----------------------------------------------------
    # Tworzenie obiektów Product
    # ----------------------------------------------------

    factory = ProductFactory()

    products = factory.create_products(
        df,
        report["mapping"]
    )

    print("\n")
    print("=" * 80)
    print("UTWORZONO PRODUKTY")
    print("=" * 80)

    print(f"Liczba produktów: {len(products)}")

    # ----------------------------------------------------
    # Parser
    # ----------------------------------------------------

    parser = ProductParser()

    print("\n")
    print("=" * 80)
    print("TEST PARSERA")
    print("=" * 80)

    for product in products[:20]:

        parser.parse(product)

        print("\n")
        print("-" * 80)

        print(f"Wiersz Excela        : {product.row_number}")

        print(f"Materiał             : {product.material}")

        print(f"Opis                 : {product.description}")

        print(f"Producent ERP        : {product.manufacturer}")

        print(f"Nr producenta ERP    : {product.manufacturer_part_number}")

        print()

        print(f"Opis po czyszczeniu  : {product.cleaned_description}")

        print(f"Wykryty producent    : {product.detected_manufacturer}")

        print(f"Wykryty numer        : {product.detected_part_number}")

        print(f"Typ produktu         : {product.product_type}")

        print(f"Zapytanie do RUBIX   : {product.search_query}")

        print(f"Pewność              : {product.confidence}%")

    print("\n")
    print("=" * 80)
    print("KONIEC TESTU")
    print("=" * 80)


if __name__ == "__main__":
    main()
