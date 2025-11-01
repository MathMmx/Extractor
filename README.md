# Data Extractor


Este projeto é um exemplo de sistema de extração e análise de dados a partir de uma API mock. O foco principal é demonstrar o processamento, validação e análise de dados, não a API em si.

⚠️ Observação: O mock_api.py serve apenas como um exemplo de API para teste. O objetivo real é a extração e tratamento dos dados no extractor.py.

Estrutura do Projeto
repo_portfolio/
│
├─ extractor.py           # Script principal de extração e análise
├─ mock_api.py            # API de teste com dados aleatórios
├─ utils.py               # Funções utilitárias de limpeza e validação
├─ config.json            # Configurações de colunas, tipos e saídas
├─ output/                # Diretório onde arquivos CSV, Excel e HTML são gerados

Funcionalidades

Extração de Dados

Conecta a uma API definida em config.json.

Suporta headers personalizados.

Limpeza e Validação

CPF (clean_cpf, is_valid_cpf)

Telefone (clean_phone, is_valid_phone)

Moeda (clean_currency)

Datas (parse_datetime) com múltiplos formatos

Emails (validação simples pelo caractere @)

Conversão de strings numéricas para inteiros (string_to_int)

Cálculos e Estatísticas

Total de registros

CPFs válidos

Emails válidos

Telefones válidos

Soma de valores monetários

Dias de atraso (days_overdue):

Positivo → atraso

Negativo → cliente em dia

Relatórios

CSV (output/remessa_tratada.csv)

Excel (output/remessa_tratada.xlsx)

HTML (output/relatorio.html) com destaque para:

CPFs inválidos

Atrasos (dias positivos e negativos)
