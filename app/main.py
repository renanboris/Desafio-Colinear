import os
import pandas as pd
from services.parser import process_accounting_file

def main():
    print("*** Processamento de Dados Contábeis ***")
    
    files = [
        'lancamentos_11.csv'
    #    'lancamentos_106.csv',
    #    'lancamentos_109.csv'
    ]
    
    #Cabeçalho padrão
    columns = ['descricao', 'contacontabil', 'desc_contacontabil']

    #Acumula arquivos processados
    all_data = []

    for file in files:
        if os.path.exists("input"):
            file_path = os.path.join("input", file)
        else:
            file_path = file

        if os.path.exists(file_path):
            
            data = process_accounting_file(file_path)
            
            if data:
                all_data.extend(data)
                print(f"Arquivo lido com sucesso: {file} ({len(data)} registros adicionados)")
            else:
                print(f"Arquivo processado sem dados válidos: {file}")
                
        else:
            print(f"Arquivo não encontrado: {file_path}")

    #Geração Arquivo CSV - Output
    print("*" * 40)
    
    if all_data:
        df = pd.DataFrame(all_data)
        
        if set(columns).issubset(df.columns):
            df = df[columns]
        
        #Remove duplicatas
        df.drop_duplicates(inplace=True)
       
        output_name = "dataset_final.csv"
        
        #Gerar CSV
        df.to_csv(output_name, index=False, encoding='utf-8')
        
        print(f"ARQUIVO FINAL GERADO: {output_name}")
        print(f"Total acumulado de linhas: {len(df)}")
    else:
        print("Nenhum dado foi gerado no total.")

    print("\nProcessamento finalizado.")

if __name__ == "__main__":
    main()