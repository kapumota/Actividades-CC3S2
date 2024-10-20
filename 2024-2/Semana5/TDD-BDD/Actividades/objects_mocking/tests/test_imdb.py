"""
Casos de prueba para Mocking Lab
"""
import json
import pytest
from unittest.mock import patch, Mock
from requests import Response
from models import IMDb

# Fixture para cargar los datos de IMDb desde un archivo JSON
@pytest.fixture(scope="session")
def imdb_data():
    """Carga las respuestas de IMDb necesarias para las pruebas"""
    with open('tests/fixtures/imdb_responses.json') as json_data:
        return json.load(json_data)

class TestIMDbDatabase:
    """Casos de prueba para la base de datos de IMDb"""

    @pytest.fixture(autouse=True)
    def setup_class(self, imdb_data):
        """Configuración inicial para cargar los datos de IMDb"""
        self.imdb_data = imdb_data

    ######################################################################
    #  CASOS DE PRUEBA
    ######################################################################

    @patch('models.requests.get')
    def test_search_titles_success(self, mock_get, imdb_data):
        """Prueba que la búsqueda de títulos retorna datos correctamente"""
        # Configurar el mock para devolver una respuesta exitosa
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = imdb_data['search_title']
        mock_get.return_value = mock_response

        imdb = IMDb(apikey="fake_api_key")
        resultado = imdb.search_titles("Inception")

        assert resultado == imdb_data['search_title']
        mock_get.assert_called_once_with("https://imdb-api.com/API/SearchTitle/fake_api_key/Inception")

    @patch('models.requests.get')
    def test_search_titles_failure(self, mock_get):
        """Prueba que la búsqueda de títulos maneja errores correctamente"""
        # Configurar el mock para devolver una respuesta fallida
        mock_response = Mock(spec=Response)
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        imdb = IMDb(apikey="fake_api_key")
        resultado = imdb.search_titles("TituloInexistente")

        assert resultado == {}
        mock_get.assert_called_once_with("https://imdb-api.com/API/SearchTitle/fake_api_key/TituloInexistente")

    @patch('models.requests.get')
    def test_movie_reviews_success(self, mock_get, imdb_data):
        """Prueba que la obtención de reseñas retorna datos correctamente"""
        # Configurar el mock para devolver una respuesta exitosa
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = imdb_data['movie_reviews']
        mock_get.return_value = mock_response

        imdb = IMDb(apikey="fake_api_key")
        resultado = imdb.movie_reviews("tt1375666")

        assert resultado == imdb_data['movie_reviews']
        mock_get.assert_called_once_with("https://imdb-api.com/API/Reviews/fake_api_key/tt1375666")

    @patch('models.requests.get')
    def test_movie_ratings_success(self, mock_get, imdb_data):
        """Prueba que la obtención de calificaciones retorna datos correctamente"""
        # Configurar el mock para devolver una respuesta exitosa
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = imdb_data['movie_ratings']
        mock_get.return_value = mock_response

        imdb = IMDb(apikey="fake_api_key")
        resultado = imdb.movie_ratings("tt1375666")

        assert resultado == imdb_data['movie_ratings']
        mock_get.assert_called_once_with("https://imdb-api.com/API/Ratings/fake_api_key/tt1375666")
