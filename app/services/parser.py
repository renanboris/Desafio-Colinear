import csv
import re
from services.text_cleaning_tool import clean_text

def process_accounting_file(file_path):
    """
    Leitura do CSV, detecta cabeçalhos e extrai lançamentos.
    """
    extracted_data = []
    
    account_code_current = None
    account_desc_current = None  
    
    # Índices das colunas
    i_data = 0
    i_hist = 5
    i_deb = 17
    i_cred = 19
    header_found = False

    print(f"Lendo: {file_path}...")

    try:
        with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f:
            reader = csv.reader(f)
            
            for row in reader:
                if not row: continue

                if not header_found and "Data" in row and "Débito" in row:
                    try:
                        i_data = row.index("Data")
                        for i, col in enumerate(row):
                            if "Hist" in col:
                                i_hist = i
                                break
                        i_deb = row.index("Débito")
                        i_cred = row.index("Crédito")
                        header_found = True
                    except ValueError:
                        print("Aviso: Cabeçalho incompleto, usando índices padrão.")
                    continue

                #Conta
                if row[0].startswith("Conta:"):
                    cleaned_row = [x for x in row if x.strip()]
                    
                    if len(cleaned_row) >= 3:
                        account_code_current = cleaned_row[1]
                        raw_account_name = cleaned_row[-1]
                        account_desc_current = clean_text(raw_account_name)
                    continue

                #Lançamentos
                if header_found and len(row) > i_data and re.match(r'\d{2}/\d{2}/\d{4}', row[i_data]):
                    if not account_code_current: continue

                    raw_history = row[i_hist]
                    v_debit = row[i_deb].strip()
                    v_credit = row[i_cred].strip()

                    valor_final = "0.00"
                    tipo = "D"

                    if v_debit and v_debit != "0,00":
                        valor_final = v_debit
                        tipo = "d"
                    elif v_credit and v_credit != "0,00":
                        valor_final = v_credit
                        tipo = "c"
                    else:
                        continue 

                    # Limpeza e Formatação da Descrição
                    clean_history = clean_text(raw_history)
                    clean_value = valor_final.replace('"', '').replace(',', '')
                    
                    final_description = f"{clean_history} valor {clean_value} {tipo}"

                    extracted_data.append({
                        'descricao': final_description,
                        'contacontabil': account_code_current,
                        'desc_contacontabil': account_desc_current 
                    })

    except Exception as e:
        print(f"Erro ao processar arquivo: {e}")

    return extracted_data