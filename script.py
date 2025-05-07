import csv
import chardet
import re

# Arquivos
arquivo_entrada = "Análise Real x Orçado (Analítico).csv"
arquivo_saida = "arquivo_corrigido.csv"

# Regex
tags_XML = r'<[^>]+>'
prefixos = r'^[^:]*:\s*'

# Remover tags XML
def remover_tags(texto):
   return re.sub(tags_XML, '', texto)

# Remover prefixos
def remover_prefixos(texto):
   return re.sub(prefixos, '', texto).strip()

# Detectar o encoding
with open(arquivo_entrada, 'rb') as f:
   enc = chardet.detect(f.read())['encoding']

# Ler o arquivo
with open(arquivo_entrada, 'r', encoding=enc, errors='ignore') as f:
   reader = csv.reader(f, delimiter=';')
   cabecalho = next(reader)
   colunas_corretas = 15

   linhas_corrigidas = []

# Lógica para corrigir os campos extrapolados
   for linha in reader:
      if len(linha) != colunas_corretas:
         if any(campo.strip() != '' for campo in linha[colunas_corretas:]):
            campos_com_valor = [campo for campo in linha[colunas_corretas:] if campo.strip() != '']
            origem_corrigida = linha[9] + ' ' + ' '.join([campo for campo in linha[10: 10 + len(campos_com_valor)]])
            linha_corrigida = linha[:9] + [origem_corrigida] + linha[10:len(cabecalho)]
            del linha_corrigida[10: 10 + len(campos_com_valor)]
            linha_sem_tags = [remover_tags(campo) for campo in linha_corrigida]
            linhas_corrigidas.append(linha_sem_tags)     
         else:
            linha_sem_tags = [remover_tags(campo) for campo in linha]
            linhas_corrigidas.append(linha_sem_tags) 
      else:
         linha_sem_tags = [remover_tags(campo) for campo in linha]
         linhas_corrigidas.append(linha_sem_tags)   

# Variáveis para a divisão da coluna de origem
novas_linhas = []
cabecalho_atualizado = cabecalho[:]
origem_subcolunas = ['Documento Ref', 'Fornecedor', 'Referencia', 'Doc.Compras', 'Material', 'Texto']
novo_cabecalho = cabecalho_atualizado[2:8] + origem_subcolunas + cabecalho_atualizado[10:12] + cabecalho_atualizado[13:15]
novo_cabecalho = [campo.strip() for campo in novo_cabecalho]

for linha in linhas_corrigidas:
   origem_split = linha[9].split('|')
   origem_split = [remover_prefixos(valor) for valor in origem_split]
   origem_split += [''] * (len(origem_subcolunas) - len(origem_split))
   nova_linha = linha[2:8] + origem_split[:len(origem_subcolunas)] + linha[10:12] + linha[13:15]
   novas_linhas.append(nova_linha)


# Salvar o arquivo corrigido
with open(arquivo_saida, 'w', encoding=enc, newline='') as f:
   writer = csv.writer(f, delimiter=';')
   writer.writerow(novo_cabecalho)
   writer.writerows(novas_linhas)

print(f"Arquivo corrigido salvo como {arquivo_saida}")