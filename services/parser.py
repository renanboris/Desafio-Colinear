import csv
import re
from services.text_cleaning_tool import clean_text

def process_accounting_file(file_path):
    """
    Leitura do CSV, detecta cabeçalhos e extrai lançamentos.
    """
    MIN_ELEMENTS_ACCOUNT_LINE = 3
    
    extracted_data = []
    
    account_code_current = None
    account_desc_current = None  
    
    # Índices para colunas dinâmicas
    i_data = None
    i_hist = None
    i_deb = None
    i_cred = None

    header_found = False

    print(f"Leitura: {file_path}...")

    try:
        with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f:
            reader = csv.reader(f)
            
            for row in reader:
                if not row: 
                    continue

                # --- 1. DETECÇÃO DE CABEÇALHO ---
                if not header_found and "Data" in row and "Débito" in row:
                    try:
                        i_data = row.index("Data")
                        
                        # Procurar coluna Histórico
                        for i, col in enumerate(row):
                            if "Hist" in col:
                                i_hist = i 
                                break
                        
                        i_deb = row.index("Débito")
                        i_cred = row.index("Crédito")
                        
                        if None not in (i_data, i_hist, i_deb, i_cred):
                            header_found = True
                        else:
                            print(f"Cabeçalho incompleto em {file_path}. Arquivo ignorado...")                            
                    except ValueError:
                        pass 
                    continue

                #Conta
                if row[0].startswith("Conta:"):
                    cleaned_row = [x for x in row if x.strip()]

                    if len(cleaned_row) >= MIN_ELEMENTS_ACCOUNT_LINE:
                        account_code_current = cleaned_row[1]
                        raw_account_name = cleaned_row[-1]
                        account_desc_current = clean_text(raw_account_name)
                    continue

                #Lançamentos
                if header_found and i_data is not None and len(row) > i_data and re.match(r'\d{2}/\d{2}/\d{4}', row[i_data]):
                    
                    if not account_code_current: 
                        print(f"Aviso: Linha de dados ignorada (sem conta pai definida): {row}")
                        continue
    
                    raw_history = row[i_hist]
                    v_debit = row[i_deb].strip()
                    v_credit = row[i_cred].strip()

                    final_value = "0.00"
                    category = "X" # <- Apenas para inicializar e evitar erro

                    if v_debit and v_debit != "0,00":
                        final_value = v_debit
                        category = "d"
                    elif v_credit and v_credit != "0,00":
                        final_value = v_credit
                        category = "c"
                    else:
                        continue 

                    # Limpeza e Formatação
                    clean_history = clean_text(raw_history)
                    clean_value = final_value.replace('"', '').replace(',', '')
                    
                    final_description = f"{clean_history} valor {clean_value} {category}"

                    extracted_data.append({
                        'descricao': final_description,
                        'contacontabil': account_code_current,
                        'desc_contacontabil': account_desc_current 
                    })

    except Exception as e:
        print(f"Erro ao processar arquivo: {e}")

    return extracted_data