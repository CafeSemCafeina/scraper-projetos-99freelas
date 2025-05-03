# Scraper de Projetos 99Freelas

Este script Python realiza web scraping no site 99Freelas para extrair informações sobre os projetos mais recentes na categoria "Web, Mobile & Software" publicados nos últimos 3 dias.

## Funcionamento Principal

O script funciona da seguinte maneira:

1.  Define a URL base e os parâmetros de busca (categoria, ordenação, data de publicação).
2.  Itera pelas páginas de resultados do 99Freelas.
3.  Para cada página, envia uma requisição HTTP GET, simulando um navegador com um `User-Agent`.
4.  Utiliza a biblioteca `BeautifulSoup` para parsear o conteúdo HTML da página.
5.  Extrai os detalhes de cada projeto listado na página, incluindo:
    *   Título do projeto
    *   Link para o projeto
    *   Informações adicionais (tipo, nível, propostas, etc.)
    *   Descrição do projeto
6.  Organiza os dados extraídos.
7.  Verifica a pasta `varreduras` para encontrar o próximo número sequencial para o arquivo de saída.
8.  Salva os dados coletados em um arquivo Markdown (`.md`) dentro da pasta `varreduras`, formatando cada projeto de forma legível. O nome do arquivo segue o padrão `projetos-X.md`, onde `X` é o número da execução.

## Tecnologias Utilizadas

*   **Python 3:** Linguagem de programação principal.
*   **Requests:** Biblioteca para realizar requisições HTTP.
*   **BeautifulSoup4:** Biblioteca para fazer parsing de HTML e XML.

## Instalação

Para rodar este script em outra máquina, siga os passos abaixo:

1.  **Instale Python 3:** Certifique-se de que o Python 3 está instalado. Você pode baixá-lo em [python.org](https://www.python.org/).
2.  **Clone o repositório (ou copie os arquivos):**
    ```bash
    git clone <url_do_repositorio>
    cd scraper-projetos-99freelas
    ```
    Ou simplesmente copie o arquivo `scraper.py` para um diretório em sua máquina.
3.  **Instale as dependências:** Navegue até o diretório onde o script está localizado e instale as bibliotecas necessárias usando pip:
    ```bash
    pip install -r requirements.txt
    ```
    *Recomendação:* É uma boa prática criar um ambiente virtual para isolar as dependências do projeto:
    ```bash
    python -m venv venv
    # No Windows
    .\venv\Scripts\activate
    # No Linux/macOS
    # source venv/bin/activate
    pip install -r requirements.txt
    ```

## Uso Básico

1.  Abra um terminal ou prompt de comando.
2.  Navegue até o diretório onde o script `scraper.py` está localizado.
3.  (Opcional) Ative o ambiente virtual, se você criou um:
    ```bash
    .\venv\Scripts\activate
    ```
4.  Execute o script:
    ```bash
    python scraper.py
    ```
5.  O script começará a buscar os projetos e exibirá mensagens de progresso no console.
6.  Ao finalizar, os dados dos projetos encontrados serão salvos em um novo arquivo `.md` dentro da pasta `varreduras` (que será criada automaticamente se não existir).