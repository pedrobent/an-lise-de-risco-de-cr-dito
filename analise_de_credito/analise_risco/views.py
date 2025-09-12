from django.shortcuts import render
import pandas as pd
import joblib

def home(request):
    context = {}
    
    if request.method == 'POST':
        modelo = joblib.load('modelo_risco_credito.joblib')

        # --- Coletar todos os dados do formulário ---
        # (Convertendo para o tipo numérico quando necessário)
        form_data = {
            'status_conta_corrente': request.POST.get('status_conta_corrente'),
            'duracao_mes': int(request.POST.get('duracao_mes')),
            'historico_credito': request.POST.get('historico_credito'),
            'proposito': request.POST.get('proposito'),
            'valor_credito': int(request.POST.get('valor_credito')),
            'poupanca': request.POST.get('poupanca'),
            'emprego_atual': request.POST.get('emprego_atual'),
            'taxa_instalment': int(request.POST.get('taxa_instalment')),
            'estado_civil_sexo': request.POST.get('estado_civil_sexo'),
            'outros_devedores': request.POST.get('outros_devedores'),
            'residencia_atual_desde': int(request.POST.get('residencia_atual_desde')),
            'propriedade': request.POST.get('propriedade'),
            'idade': int(request.POST.get('idade')),
            'outros_planos_pagamento': request.POST.get('outros_planos_pagamento'),
            'moradia': request.POST.get('moradia'),
            'n_creditos_existentes': int(request.POST.get('n_creditos_existentes')),
            'emprego': request.POST.get('emprego'),
            'n_dependentes': int(request.POST.get('n_dependentes')),
            'telefone': request.POST.get('telefone'),
            'trabalhador_estrangeiro': request.POST.get('trabalhador_estrangeiro'),
        }

        # --- Preparar os dados para o modelo ---
        colunas_modelo = [
            'duracao_mes', 'valor_credito', 'taxa_instalment', 'residencia_atual_desde', 'idade',
            'n_creditos_existentes', 'n_dependentes', 'status_conta_corrente_A11', 'status_conta_corrente_A12',
            'status_conta_corrente_A13', 'status_conta_corrente_A14', 'historico_credito_A30', 'historico_credito_A31',
            'historico_credito_A32', 'historico_credito_A33', 'historico_credito_A34', 'proposito_A40',
            'proposito_A41', 'proposito_A410', 'proposito_A42', 'proposito_A43', 'proposito_A44',
            'proposito_A45', 'proposito_A46', 'proposito_A48', 'proposito_A49', 'poupanca_A61', 'poupanca_A62',
            'poupanca_A63', 'poupanca_A64', 'poupanca_A65', 'emprego_atual_A71', 'emprego_atual_A72',
            'emprego_atual_A73', 'emprego_atual_A74', 'emprego_atual_A75', 'estado_civil_sexo_A91',
            'estado_civil_sexo_A92', 'estado_civil_sexo_A93', 'estado_civil_sexo_A94', 'outros_devedores_A101',
            'outros_devedores_A102', 'outros_devedores_A103', 'propriedade_A121', 'propriedade_A122',
            'propriedade_A123', 'propriedade_A124', 'outros_planos_pagamento_A141', 'outros_planos_pagamento_A142',
            'outros_planos_pagamento_A143', 'moradia_A151', 'moradia_A152', 'moradia_A153', 'emprego_A171',
            'emprego_A172', 'emprego_A173', 'emprego_A174', 'telefone_A191', 'telefone_A192',
            'trabalhador_estrangeiro_A201', 'trabalhador_estrangeiro_A202'
        ]

        # Cria DataFrame com zeros
        dados_cliente = pd.DataFrame(0, index=[0], columns=colunas_modelo)

        # Preenche as colunas numéricas
        for col in ['duracao_mes',
                    'valor_credito',
                    'taxa_instalment',
                    'residencia_atual_desde',
                    'idade', 'n_creditos_existentes',
                    'n_dependentes']:
            
            if col in form_data:
                dados_cliente[col] = form_data[col]
        
        # Preenche as colunas categóricas (one-hot encoding)
        for col_name, value in form_data.items():
            if isinstance(value, str): # Apenas para os campos de texto/select
                coluna_encoded = f'{col_name}_{value}'
                if coluna_encoded in dados_cliente.columns:
                    dados_cliente[coluna_encoded] = 1

        # --- Fazer a previsão ---
        previsao = modelo.predict(dados_cliente)
        
        # --- Interpretar e enviar resultado ---
        if previsao[0] == 0:
            resultado = "Crédito Aprovado! (Baixo Risco)"
        else:
            resultado = "Crédito Negado! (Alto Risco)"
        
        context['resultado'] = resultado
        # Reenviar os dados do formulário para o template (opcional, mas bom para manter os campos preenchidos)
        context['form_data'] = form_data

    return render(request, 'home.html', context)