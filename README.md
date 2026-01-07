# Cartographic Generalizer

Plugin QGIS para generalização cartográfica de feições lineares baseado em mudança de escala.

## Descrição

Plugin que implementa generalização cartográfica automática considerando o Índice de Generalização (Ig) derivado da mudança de escala. Aplica operadores de simplificação (Douglas-Peucker) e suavização (Chaikin) em feições lineares como curvas de nível, rios e outras geometrias lineares.

Baseado nos conceitos de generalização cartográfica da tese de Dal Santo, M.A. (2007) sobre generalização cartográfica automatizada para banco de dados cadastral.

## Funcionalidades

- **Cálculo de Índice de Generalização (Ig)**: calcula automaticamente baseado em escala origem/destino
- **Simplificação**: remove vértices desnecessários usando Douglas-Peucker
- **Suavização**: reduz ângulos agudos usando algoritmo Chaikin
- **Interface simples**: todos parâmetros em uma única tela
- **Controle manual**: usuário define todos os parâmetros

## Instalação

### Método 1: Via Gerenciador de Plugins (quando publicado)

1. Abra QGIS
2. Menu `Plugins > Manage and Install Plugins`
3. Busque por "Cartographic Generalizer"
4. Clique em `Install Plugin`

### Método 2: Instalação Manual

1. Localize a pasta de plugins do QGIS:
   - **Windows**: `C:\Users\SEU_USUARIO\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins`
   - **Linux**: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins`
   - **Mac**: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins`

2. Copie a pasta `cartographic_generalizer` para o diretório de plugins

3. Reinicie QGIS

4. Ative o plugin em `Plugins > Manage and Install Plugins > Installed`

## Uso

1. Abra uma camada vetorial de linhas (curvas de nível, hidrografia, etc.)

2. Acesse o plugin:
   - Menu: `Vector > Cartographic Generalizer > Generalização Cartográfica`
   - Ou clique no ícone na barra de ferramentas

3. Configure os parâmetros:
   - **Camada de Entrada**: selecione a camada a generalizar
   - **Escala Origem**: escala original dos dados (ex: 5000 para 1:5.000)
   - **Escala Destino**: escala desejada (ex: 25000 para 1:25.000)
   - Clique em **Calcular Ig** para ver o índice e tolerância sugerida

4. Ajuste parâmetros de generalização:
   - **Simplificação**: 
     - Marque para ativar
     - Ajuste tolerância (m) - quanto maior, mais simplificação
   - **Suavização**:
     - Marque para ativar
     - Ajuste iterações (1-10) - quanto maior, mais suave
     - Ajuste offset (0.1-1.0) - controla intensidade

5. Defina nome da camada de saída

6. Clique em **Aplicar Generalização**

## Conceitos

### Índice de Generalização (Ig)

**Fórmula:** Ig = Do/Dg (conforme Dal Santo, 2007)

Onde:
- Do = denominador da escala de origem
- Dg = denominador da escala generalizada (destino)

Exemplo: 1:5.000 → 1:25.000 resulta em Ig = 5000/25000 = 0.2

**Interpretação:**
- Ig < 1 indica necessidade de generalização
- Quanto menor o Ig, maior a generalização necessária
- Ig = 0.2 significa que a escala é 5x menor (menos detalhada)

### Simplificação (Douglas-Peucker)

Remove vértices mantendo forma essencial. A tolerância define distância máxima permitida entre linha original e simplificada.

### Suavização (Chaikin)

Reduz ângulos agudos criando curvas mais suaves. Cada iteração suaviza mais a linha.

## Exemplos de Uso

### Curvas de Nível

- **Escala Origem**: 5000 (1:5.000)
- **Escala Destino**: 25000 (1:25.000)
- **Ig**: 0.2 (5000/25000)
- **Simplificação**: Ativada, tolerância ~2.5m (sugerida automaticamente)
- **Suavização**: Ativada, 3 iterações, offset 0.25

### Rios/Hidrografia

- **Escala Origem**: 10000 (1:10.000)
- **Escala Destino**: 50000 (1:50.000)
- **Ig**: 0.2 (10000/50000)
- **Simplificação**: Ativada, tolerância ~2.5m (sugerida automaticamente)
- **Suavização**: Ativada, 3 iterações, offset 0.25

**Nota**: Os valores de tolerância são calculados automaticamente usando a fórmula (1/Ig) × 0.5, resultando em valores apropriados para a mudança de escala. Ajuste conforme necessário para seus dados específicos.

## Requisitos

- QGIS 3.0 ou superior
- Python 3.6+
- PyQt5 (incluído no QGIS)

## Limitações

- Processa apenas geometrias de linha (LineString)
- Não considera hierarquia de redes (ordem de Strahler)
- Não preserva conectividade automática entre feições
- Processa uma camada por vez

## Desenvolvimento Futuro

Possíveis melhorias:

- Suporte a ordem de Strahler para hidrografia
- Preservação automática de conectividade
- Processamento em lote de múltiplas camadas
- Presets de parâmetros salvos
- Relatório de estatísticas (vértices removidos, etc.)

## Autor

Desenvolvido por Indiara Elis.

## Licença

GPL v3 ou superior

## Contribuições

Contribuições são bem-vindas! Abra issues ou pull requests no repositório.

## Referências

Baseado nos conceitos de generalização cartográfica:

- DAL SANTO, M. A. Generalização cartográfica automatizada para um banco de dados cadastral. 2007. Tese (Doutorado em Engenharia Civil) - Programa de Pós-Graduação em Engenharia Civil, Universidade Federal de Santa Catarina, Florianópolis, 2007. Disponível em: http://repositorio.ufsc.br/xmlui/handle/123456789/89592
- McMaster, R. B., & Shea, K. S. (1992). Generalization in Digital Cartography
- Keates, J. S. (1989). Cartographic Design and Production