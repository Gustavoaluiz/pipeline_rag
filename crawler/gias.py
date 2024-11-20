import os
import re
import sys
from typing import List
import pandas as pd
import pdfplumber

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.abspath(os.path.join(current_dir, '..',))
sys.path.append(project_dir)

from regulacao_domain.registro_hierarquico import RegistroHierarquico
from regulacao_domain.categoria_regulacao import CategoriaRegulacao


class GisCrawler:
    def __init__(
            self,
            path: str, 
            name: str, 
            font_title: str = None, 
            ignore_pages: List[int] = []
    ):
        self.path = path
        self.name = name
        self.ignore_pages = ignore_pages
        self.section_idx = 0
        self.count = 0
        self.results = []

        self.categoria = CategoriaRegulacao.NORMAS_GLOBAIS_AUDITORIA_INTERNA
        self.nivel_1 = ''
        self.nivel_2 = ''
        self.nivel_3 = ''
        self.nivel_4 = ''
        self.nivel_5 = ''
        self.text = ''
        self.pages_text = ''

        # [nivel_3, nivel_4, nivel_5]
        self.nivel_count = [0, 0, 0]

        self.font_title = font_title

    def _save_to_csv(self, df):
        csv_path = os.path.join(
            current_dir, 
            'output', 
        )
        os.makedirs(csv_path, exist_ok=True)
        csv_path = os.path.join(csv_path, f'{self.name}.csv')
        
        if not os.path.exists(csv_path):
            df.to_csv(csv_path, index=False)
        else:
            df.to_csv(csv_path, mode='a', header=False, index=False)

    def _create_register(self):
        # Para cada linha, cria um dicionário com as informações extraidas

        return RegistroHierarquico(
            categoria=self.categoria.name,
            descricao_categoria=self.categoria.description,
            conteudo=self.text,
            nivel_1=self.nivel_1,
            nivel_2=self.nivel_2,
            nivel_3=self.nivel_3,
            nivel_4=self.nivel_4,
            nivel_5=self.nivel_5,
        )
    
    def _find_line_type(self, line):
        text = line['text']
        font = line['chars'][0]['fontname']
        size = int(line['chars'][0]['size'])
        last_entry = self.results[-1] if len(self.results) > 0 else None
        # Se achar "bold" na fonte, provavelmente é um titulo
        if re.match(r'RPPRGU\+BasicSans-Light', font) and size == 27:
            if last_entry is not None and self.count == self.nivel_count[0] + 1:
                self.nivel_1 = last_entry.nivel_1 + ' ' + text
            else:
                self.nivel_1 = text
                self.nivel_2 = ''
                self.nivel_3 = ''

            self.nivel_count[0] = self.count
        
        elif re.match(r'ORLZQA\+BasicSans-Regular', font) and size == 19:
            if self.count == self.nivel_count[1] + 1:
                self.nivel_2 = last_entry.nivel_2 + ' ' + text
            else:
                self.nivel_2 = text
                self.nivel_3 = ''

            self.nivel_count[1] = self.count

        elif re.match(r'ORLZQA\+BasicSans-SemiBold', font) and size == 17:
            if self.count == self.nivel_count[2] + 1:
                self.nivel_3 = last_entry.nivel_3 + ' ' + text
            else:
                self.nivel_3 = text

            self.nivel_count[2] = self.count
        
        elif re.match(r'ORLZQA\+BasicSans-Bold', font) and size == 8:
            self.text = ''
        elif re.match(r'RPPRGU\+BasicSans-Light', font) and size == 6:
            self.text = ''

        else:
            self.text = text + ' '

    def _extract_with_paragraph(self, page_text):    
        # Retirar as quebras de linhas dos meios dos parágrafos
        page_text = re.split(r'\.\n\s*(?=[A-Z])', page_text)
        # print(page_text)
        result =  ''
        for t in page_text:
            result += t + '.' + '\n\n'

        # CONSERTAR HIFENS
        result = re.sub(r'-\n\s*', '', result)
        # RETIRAR \N, mantendo somente os paragrafos
        result = re.sub(r'(?<!\n)\n(?!\n)', ' ', result)
        result =  re.sub(r'\d*\s*©\d{4}, The Institute of Internal Auditors\. All Rights Reserved\.', '', result)
        result =  re.sub(r' \n\nFor individual personal use only\.', '', result)

        return result

    def _extract_pdf(self, pdf):
        for page in pdf.pages:
            # Ignora páginas anotadas para serem ignoradas
            if page.page_number in self.ignore_pages:
                continue
            
            page_lines = page.extract_text_lines(strip=True, return_chars=True)
            page_text = page.extract_text()
            self.pages_text += self._extract_with_paragraph(page_text)

            # Itera o pdf linha por linha
            for line in page_lines:
                # print([line['chars'][0]['fontname'] + '\t' + str(int(line['chars'][0]['size'])) + '\t' + line['text']])

                self.count += 1
                self.text = ''

                self._find_line_type(line)

                if len(self.results) > 0:
                    last_entry = self.results[-1]
                    # se nada mudou na estrutura hierarquica, então continue adicionando no registro anterior
                    if  self.nivel_5 in last_entry.nivel_5 and \
                        self.nivel_4 in last_entry.nivel_4 and \
                        self.nivel_3 in last_entry.nivel_3 and \
                        self.nivel_2 in last_entry.nivel_2 and \
                        self.nivel_1 in last_entry.nivel_1:
                        last_entry.conteudo += self.text
                    
                    # senão, crie um novo registro
                    else:
                        register = self._create_register()
                        self.results.append(register)

                # Se registros estiver vazio, 
                # então adiciona a primeira linha da primeira seção
                else:
                    register = self._create_register()
                    self.results.append(register)

    def _add_paragraphs(self, row):
        # Conserta as separações por hífens nas quebras de linhas do pdf
        row['conteudo'] = re.sub(r'-\s*', '', row['conteudo'])

        # Dividindo o texto com parágrafos, utilizando as quebras duplas como delimitador
        paragraphs = self.pages_text.split('.\n\n')

        # Removendo espaços desnecessários dos parágrafos divididos
        paragraphs = [par.strip() for par in paragraphs if par.strip()]

        # Iterando sobre cada parágrafo encontrado
        for par in paragraphs:
            # Procurando onde a parte final parágrafo ocorre no texto
            index = row['conteudo'].find(par)
            
            if index != -1:
                # Calculando a posição de inserção da quebra dupla (logo após o parágrafo)
                insert_position = index + len(par) + 1
                # Inserindo a quebra dupla na posição correta
                row['conteudo'] = (
                    row['conteudo'][:insert_position] + "\n\n" + row['conteudo'][insert_position:]
                )

        return row

    def _clean_df(self, df):
        # Dropa linhas sem texto
        df.drop(df[df['conteudo'] == ''].index, inplace=True)
        df.drop(df[df['nivel_1'] == ''].index, inplace=True)
        df.apply(self._add_paragraphs, axis=1)  
        # df.drop(df[df['nivel_2'] == ''].index, inplace=True)
        

    def read_pdf(self):
        with pdfplumber.open(self.path) as pdf:
            self._extract_pdf(pdf)
            df = pd.DataFrame(self.results)
            self._clean_df(df)

        return self._save_to_csv(df)

def data_concat(name):
    df = pd.DataFrame()
    for data in os.listdir(os.path.join(current_dir, 'output')):
        df_temp = pd.read_csv(os.path.join(current_dir, 'output', data))
        df = pd.concat([df, df_temp])

    df.to_csv(os.path.join(current_dir, 'output', f'{name}.csv'), index=False)
        

if __name__ == '__main__':

    names = os.listdir(os.path.join(current_dir, 'data'))
    names = [name.replace('.pdf', '') for name in names]

    for name in names:
        print("Extraindo dados do arquivo: ", name)
        path = os.path.join(current_dir, 'data', f'{name}.pdf')

        ren = GisCrawler(
            path=path, 
            name=name, 
            ignore_pages=[1,2,3,4, 122]
        )
        ren.read_pdf()
        # print(ren.pages_text)

    # data_concat('proced_regula_tarifaria')
        