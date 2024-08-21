import pandas as pd
import pickle


class Modelo:
    """
    Classe para carregar um modelo treinado e fazer previsões em novos dados.
    """

    def __init__(self, modelo, novos_dados):
        """
        Inicializa a classe Modelo.

        Args:
            modelo (str): Caminho para o arquivo do modelo treinado (formato pickle).
            novos_dados (list): Lista contendo os novos dados para previsão.
        """
        self._modelo = modelo
        self._novos_dados = novos_dados

    def funcao_modelo(self):
        """
        Carrega o modelo treinado, faz previsões nos novos dados e imprime os resultados.
        """

        # Carregar o modelo treinado a partir do arquivo pickle
        modelo_carregado = pickle.load(open(self._modelo, 'rb'))

        # Converter a lista de novos dados em um DataFrame do pandas
        novos_dados = pd.DataFrame([self._novos_dados], columns=['barra_1', 'barra_2', 'barra_3', 'barra_4',
                                                                 'barra_5', 'barra_6', 'barra_7', 'barra_8'])

        # Fazer as previsões usando o modelo carregado
        previsoes = modelo_carregado.predict(novos_dados)

        # Imprimir as previsões no console
        print(previsoes)

        # Retornar as previsões
        return previsoes
