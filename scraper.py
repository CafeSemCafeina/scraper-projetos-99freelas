import requests
from bs4 import BeautifulSoup
import os
from pathlib import Path
import re

# --- Configurações ---
BASE_URL = "https://www.99freelas.com.br/projects"
PARAMS = {
    "order": "mais-recentes",
    "categoria": "web-mobile-e-software",
    "data-da-publicacao": "menos-de-3-dias-atras"
}
NUM_PAGINAS_PARA_VARREDURA = 3
PASTA_VARREDURAS = Path("varreduras")

# --- Funções ---

def buscar_html_pagina(page_num):
    """
    Busca o conteúdo HTML de uma página específica de resultados.

    Args:
        page_num (int): O número da página a ser buscada.

    Returns:
        BeautifulSoup object or None: O objeto BeautifulSoup com o HTML parseado
                                      ou None se ocorrer um erro na requisição.
    """
    url_paginada = f"{BASE_URL}?page={page_num}"
    print(f"Buscando dados da página: {url_paginada}")
    try:
        # Adiciona um cabeçalho User-Agent para simular um navegador
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # Adiciona os parâmetros fixos e o cabeçalho à URL da página específica
        response = requests.get(url_paginada, params=PARAMS, headers=headers, timeout=10) # Adicionado headers=headers
        response.raise_for_status() # Lança exceção para status HTTP ruins (4xx ou 5xx)
        # Usar 'html.parser' como parser padrão
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar a página {page_num}: {e}")
        return None

def extrair_dados_projetos(soup):
    """
    Extrai os detalhes dos projetos a partir de um objeto BeautifulSoup.

    Args:
        soup (BeautifulSoup object): O objeto BeautifulSoup com o HTML da página.

    Returns:
        list: Uma lista de dicionários, onde cada dicionário contém
              os detalhes de um projeto ('titulo', 'link', 'info', 'descricao').
    """
    projetos_encontrados = []
    # Encontra a lista principal que contém os projetos
    lista_resultados = soup.find('ul', class_='result-list')

    if not lista_resultados:
        print("A lista de resultados (<ul class='result-list'>) não foi encontrada.")
        return projetos_encontrados

    # Encontra todos os itens <li> dentro da lista
    itens_projeto = lista_resultados.find_all('li', id=lambda x: x and x.startswith('project-'))

    if not itens_projeto:
        print("Nenhum item de projeto (<li>) foi encontrado na lista.")
        return projetos_encontrados

    print(f"Encontrados {len(itens_projeto)} itens de projeto na página.")

    for item in itens_projeto:
        titulo = "Não encontrado"
        link = "Não encontrado"
        info = "Não encontrada"
        descricao = "Não encontrada"

        # Extrai o título e o link
        h1_title = item.find('h1', class_='title')
        if h1_title:
            link_tag = h1_title.find('a', href=True)
            if link_tag:
                titulo = link_tag.get_text(strip=True)
                # Garante que o link seja absoluto
                link_parcial = link_tag['href']
                if link_parcial.startswith('/'):
                    link = f"https://www.99freelas.com.br{link_parcial}"
                else:
                    link = link_parcial # Assume que já é absoluto se não começar com /

        # Extrai as informações (ajustando seletores conforme necessidade)
        # Tentativa 1: Classe exata fornecida pelo usuário (pode precisar de ajuste)
        info_tag = item.find('p', class_='item-text information') # Ajustado de 'item-texta'
        if info_tag:
            info = info_tag.get_text(separator=' | ', strip=True)
        else:
            # Tentativa 2: Buscar uma tag <p> com a classe 'information' (mais genérico)
            info_tag_alt = item.find('p', class_='information')
            if info_tag_alt:
                 info = info_tag_alt.get_text(separator=' | ', strip=True)
            else:
                # Se ainda não encontrar, pode ser necessário inspecionar o HTML real
                # para achar o seletor correto para as informações.
                pass # Mantém "Não encontrada"

        # Extrai a descrição
        desc_tag = item.find('div', class_='description') # Simplificado, a classe 'formatted-text' pode estar dentro
        if desc_tag:
            # Pega todo o texto dentro da div, incluindo tags aninhadas, e limpa espaços
            descricao = desc_tag.get_text(strip=True)
            # Alternativa: Se precisar do HTML interno: descricao = str(desc_tag)

        projetos_encontrados.append({
            'titulo': titulo,
            'link': link,
            'info': info,
            'descricao': descricao
        })

    return projetos_encontrados

def encontrar_proximo_numero_arquivo():
    """
    Verifica a pasta 'varreduras' e determina o próximo número
    para o nome do arquivo 'projetos-X.md'.

    Returns:
        int: O próximo número sequencial para o arquivo.
    """
    PASTA_VARREDURAS.mkdir(parents=True, exist_ok=True) # Cria a pasta se não existir
    maior_numero = 0
    # Regex para encontrar arquivos no formato projetos-NUMERO.md
    regex = re.compile(r"projetos-(\d+)\.md")
    try:
        for nome_arquivo in os.listdir(PASTA_VARREDURAS):
            match = regex.match(nome_arquivo)
            if match:
                numero = int(match.group(1))
                if numero > maior_numero:
                    maior_numero = numero
    except FileNotFoundError:
        # Pasta acabou de ser criada ou está vazia
        pass
    return maior_numero + 1

def salvar_projetos_em_markdown(projetos, numero_arquivo):
    """
    Salva a lista de projetos em um arquivo Markdown formatado.

    Args:
        projetos (list): A lista de dicionários de projetos.
        numero_arquivo (int): O número sequencial para o nome do arquivo.
    """
    nome_arquivo = PASTA_VARREDURAS / f"projetos-{numero_arquivo}.md"
    print(f"Salvando dados em: {nome_arquivo}")
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            f.write(f"# Varredura de Projetos 99Freelas - Execução {numero_arquivo}\n\n")
            if not projetos:
                f.write("Nenhum projeto encontrado nesta varredura.\n")
                return

            for i, projeto in enumerate(projetos, 1):
                f.write(f"## Projeto {i}: {projeto['titulo']}\n\n")
                f.write(f"**Link:** [{projeto['titulo']}]({projeto['link']})\n\n")
                f.write(f"**Informações:**\n{projeto['info']}\n\n")
                f.write(f"**Descrição:**\n```\n{projeto['descricao']}\n```\n")
                f.write("---\n\n")
        print(f"Dados salvos com sucesso em {nome_arquivo}")
    except IOError as e:
        print(f"Erro ao salvar o arquivo {nome_arquivo}: {e}")

# --- Execução Principal ---
if __name__ == "__main__":
    todos_os_projetos = []
    print("Iniciando varredura de projetos no 99Freelas...")

    # Itera pelas páginas definidas
    for i in range(1, NUM_PAGINAS_PARA_VARREDURA + 1):
        soup_pagina = buscar_html_pagina(i)
        if soup_pagina:
            print(f"Analisando dados da página {i}...")
            projetos_da_pagina = extrair_dados_projetos(soup_pagina)
            if projetos_da_pagina:
                todos_os_projetos.extend(projetos_da_pagina)
            else:
                print(f"Nenhum projeto extraído da página {i}.")
        else:
            print(f"Não foi possível buscar ou analisar a página {i}. Continuando...")

    print(f"\nVarredura concluída. Total de projetos encontrados: {len(todos_os_projetos)}")

    # Determina o nome do próximo arquivo e salva os dados
    if todos_os_projetos:
        proximo_num = encontrar_proximo_numero_arquivo()
        salvar_projetos_em_markdown(todos_os_projetos, proximo_num)
    else:
        print("Nenhum projeto foi encontrado para salvar.")

    print("Script finalizado.")