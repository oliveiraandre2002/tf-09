
# Os pilares na árvore de arquivos:
# herança, polimorfismo, abstração e interface.

from abc import ABC, abstractmethod


# INTERFACE: contrato para objetos que sabem informar seu tamanho.
class Medivel(ABC):
    __slots__ = ()

    @abstractmethod
    def tamanho(self):
        pass


# ABSTRAÇÃO: características comuns de arquivos e pastas.
class Item(Medivel):
    __slots__ = ("__nome", "__pai")

    def __init__(self, nome, pai=None):
        self.__validar_nome(nome)
        self.__nome = nome
        self.__pai = None

        if pai is not None:
            self.mover_para(pai)

    def __validar_nome(self, nome):
        if nome == "" or "/" in nome:
            raise ValueError("nome inválido: " + repr(nome))

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, novo_nome):
        self.__validar_nome(novo_nome)
        self.__nome = novo_nome

    @property
    def pai(self):
        return self.__pai

    def mover_para(self, destino):
        if destino is self.__pai:
            return

        destino._receber(self)

        if self.__pai is not None:
            self.__pai._soltar(self)

        self.__pai = destino

    # Por padrão, um item não aceita outros itens dentro dele.
    def _receber(self, item):
        raise ValueError(
            self.__nome + " é um arquivo, não pode conter itens"
        )

    def caminho(self):
        if self.__pai is None:
            return self.__nome

        return self.__pai.caminho() + "/" + self.__nome

    def profundidade(self):
        if self.__pai is None:
            return 0

        return self.__pai.profundidade() + 1

    @abstractmethod
    def mostrar(self):
        pass


# ARQUIVO: possui um tamanho próprio em bytes.
class Arquivo(Item):
    __slots__ = ("__bytes",)

    def __init__(self, nome, tamanho_bytes, pai=None):
        if tamanho_bytes < 0:
            raise ValueError("tamanho não pode ser negativo")

        self.__bytes = tamanho_bytes
        super().__init__(nome, pai)

    def tamanho(self):
        return self.__bytes

    def mostrar(self):
        recuo = "    " * self.profundidade()
        print(
            recuo + self.nome + " (" + str(self.tamanho()) + " B)"
        )


# PASTA: pode conter arquivos e outras pastas.
class Pasta(Item):
    __slots__ = ("__filhos",)

    def __init__(self, nome, pai=None):
        self.__filhos = []
        super().__init__(nome, pai)

    @property
    def filhos(self):
        return tuple(self.__filhos)

    # A pasta aceita itens, mas impede ciclos na árvore.
    def _receber(self, item):
        ancestral = self

        while ancestral is not None:
            if ancestral is item:
                raise ValueError(
                    "não dá para mover "
                    + item.nome
                    + " para dentro dela mesma"
                )

            ancestral = ancestral.pai

        self.__filhos.append(item)

    def _soltar(self, item):
        self.__filhos.remove(item)

    # Polimorfismo: soma o tamanho de todos os itens da pasta.
    def tamanho(self):
        total = 0

        for filho in self.__filhos:
            total = total + filho.tamanho()

        return total

    def mostrar(self):
        recuo = "    " * self.profundidade()

        print(
            recuo + self.nome + "/ ("
            + str(self.tamanho()) + " B)"
        )

        for filho in self.__filhos:
            filho.mostrar()


# LIXEIRA: mede os arquivos descartados sem pertencer à árvore.
class Lixeira(Medivel):
    __slots__ = ("__descartados",)

    def __init__(self):
        self.__descartados = []

    def descartar(self, arquivo):
        self.__descartados.append(arquivo)

    def tamanho(self):
        total = 0

        for arquivo in self.__descartados:
            total = total + arquivo.tamanho()

        return total


# Soma o tamanho de qualquer conjunto de objetos mensuráveis.
def espaco_total(coisas):
    total = 0

    for coisa in coisas:
        total = total + coisa.tamanho()

    return total


# Executa uma ação e informa se ela passou ou gerou um erro.
def tentar(rotulo, acao):
    try:
        acao()
        print(rotulo, "-> passou (!)")
    except Exception as erro:
        print(
            rotulo,
            "->",
            type(erro).__name__ + ":",
            erro
        )
