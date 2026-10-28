# Pilares da POO

- **Encapsulamento:** A interface permite consultar `atalho.destino` e usar `redirecionar()`. A implementação esconde o atributo `__destino` e suas validações.
- **Herança:** A interface do `Atalho` inclui recursos herdados de `Item`, como `nome`, `pai` e `caminho()`. A implementação reaproveita o código da classe pai.
- **Polimorfismo:** A interface permite chamar `tamanho()` em diferentes objetos. A implementação varia conforme a classe: `Atalho` retorna `1`, enquanto `Pasta` soma os tamanhos dos filhos.
