# Regex

## Formato do arquivo

Este arquivo segue o seguinte padrão:
```
    definição: expressão-regular
```

As definições se tornarão os tipos do token reconhecido pela expressão regular à direita.

Caso você precise de variáveis auxiliares, pode utilizar uma definição dentro de uma expressão regular subsequente, como no exemplo:

```
digit: [0-9]
letter: [a-zA-Z]
id: letter(letter|digit)*
```

Toda expressão que for utilizada dentro de outra será considerada auxiliar e, portanto, não será um tipo de token reconhecível. Neste caso, digit e letter não serão tipos reconhecíveis, mas id será.

Apenas as definições chamadas `ìd` serão utilizadas no analizador sintático como identificadores de variáveis.


## Expressões válidas

O formato de regex reconhecido pelo parsero é um pouco diferente do convencional.

São expressões válidas:

```
[a-z]                   | - Letras minúsculas
[A-Z]                   | - Letras maiúsculas
[a-Z] ou [a-zA-Z] ou \w | - Letras maiúsculas ou minúsculas
[0-9] ou \d             | - Dígitos de 0 a 9
\s                      | - Espaços vazios ou newlines
.                       | - Quaisquer símbolos suportados
&                       | - Palavra vazia
```

Os seguintes operadores são válidos para espressões S e T:
```
S*      | Fecho
S+      | Fecho positivo
ST      | concatenação
S|T     | ou
S?      | equivalente a (S | &)
```

## Limitações

Infelizmente os operadores `[]` e `{}` ainda não funcionam.

Intervalos genéricos como `[2-7]` ou `[x-z]` também não.

## Exemplos 

Existem alguns exemplos de definições regulares em "examples/regex". O mais completo deve ser o python.regex, com ele é possível avaliar corretamente boa parte dos arquivos do próprio repositório. Os erros que costumam aparecem são devido a caracteres não reconhecidos dentro de uma string ou comentário. 