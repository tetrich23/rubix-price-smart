from core.product import Product


class ProductFactory:

    def __init__(self):
        pass

    def create_products(self, dataframe, mapping):

        products = []

        for index, row in dataframe.iterrows():

            product = Product(row_number=index + 2)

            # ---------------------------------------

            if "Materiał" in dataframe.columns:
                product.material = str(row["Materiał"]).strip()

            # ---------------------------------------

            if mapping["description"]:
                product.description = str(
                    row[mapping["description"]]
                ).strip()

            # ---------------------------------------

            if mapping["manufacturer"]:
                product.manufacturer = str(
                    row[mapping["manufacturer"]]
                ).strip()

            # ---------------------------------------

            if mapping["part_number"]:
                product.manufacturer_part_number = str(
                    row[mapping["part_number"]]
                ).strip()

            # ---------------------------------------

            if mapping["quantity"]:

                try:
                    product.quantity = float(
                        str(row[mapping["quantity"]]).replace(",", ".")
                    )

                except:

                    product.quantity = 0

            # ---------------------------------------

            if mapping["price"]:

                try:
                    product.price = float(
                        str(row[mapping["price"]]).replace(",", ".")
                    )

                except:

                    product.price = 0

            products.append(product)

        return products
