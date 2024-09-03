# Posible solucion inicial
import os

class DatabaseSearch:
    def __init__(self, file_path, page_size=1000):
        self.file_path = file_path
        self.page_size = page_size
        self.num_records = self._get_num_records()

    def _get_num_records(self):
        """Devuelve el número de registros en la tabla."""
        with open(self.file_path, 'r') as file:
            return sum(1 for _ in file)

    def _get_page(self, page_number):
        """Carga una página de registros en memoria."""
        with open(self.file_path, 'r') as file:
            start = page_number * self.page_size
            file.seek(start * 100)  # Asumiendo que cada registro tiene un tamaño fijo en bytes
            page = [file.readline().strip() for _ in range(self.page_size)]
        return page

    def _binary_search_in_page(self, page, target):
        """Realiza una búsqueda binaria dentro de una página de registros."""
        low, high = 0, len(page) - 1
        while low <= high:
            mid = (low + high) // 2
            record = page[mid].split(',')[0]  # Suponiendo que el índice está en la primera columna
            if record == target:
                return page[mid]
            elif record < target:
                low = mid + 1
            else:
                high = mid - 1
        return None

    def search(self, target):
        """Busca el registro objetivo utilizando búsqueda binaria con paginación."""
        low, high = 0, self.num_records // self.page_size

        while low <= high:
            mid = (low + high) // 2
            page = self._get_page(mid)

            if not page:
                return None

            if target < page[0].split(',')[0]:  # Comparando con el primer registro de la página
                high = mid - 1
            elif target > page[-1].split(',')[0]:  # Comparando con el último registro de la página
                low = mid + 1
            else:
                # Búsqueda dentro de la página si el target está en el rango de la página
                return self._binary_search_in_page(page, target)

        return None

