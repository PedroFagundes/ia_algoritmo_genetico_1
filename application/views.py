# -*- coding: utf-8 -*-
from random import randint, sample, shuffle

from operator import itemgetter

from django.shortcuts import render

from .forms import Formulario

'''_____________________________________________________________________
   _____________função para gerar o vetor de letras unicas______________'''

def get_letras_unicas(palavras):
	letras_unicas = []
	
	for l in palavras:
	
		if l not in letras_unicas:
			letras_unicas.append(l) 
	
	return letras_unicas


'''______________________________________________________________________
   _____________função para gerar a população de individuos______________'''

def gera_populacao(qtd):
	populacao = []
	individuo = ''
	
	for i in range(qtd):
	
		while len(individuo) < 10:
	
			for j in range(10):
				numero_gerado = randint(0,9)
	
				if str(numero_gerado) not in individuo:
					individuo += str(numero_gerado)
		
		populacao.append(individuo)
		individuo = ''
	
	return populacao


'''_________________________________________________________________
   _____________função que gera os fa's dos individuos______________'''

def gera_fa(populacao, letras_unicas, palavras):
	fa_palavra = ''
	vetor_individuo_fa = []
	populacao_com_fa = []
	
	for individuo in populacao:
	
		for palavra in palavras:
	
			for p in palavra:
				index_letra = letras_unicas.index(p)
				fa_palavra += individuo[index_letra]
	
			vetor_individuo_fa.append(fa_palavra)
			fa_palavra = ''
	
		fa = abs(int(vetor_individuo_fa[0]) + int(vetor_individuo_fa[1]) - int(vetor_individuo_fa[2]))
		vetor_individuo_fa = []
		individuo_gerado = {}
		individuo_gerado['individuo'] = individuo
		individuo_gerado['fa'] = fa
		populacao_com_fa.append(individuo_gerado)
	
	return populacao_com_fa



'''_______________________________________________________
   _____________ Gerando LIsta de Tuplas _________________'''

def gera_lista_tuplas(populacao_com_fa):
	dict_fa = {}
	individuo_fa = []
	
	for individuo_com_fa in populacao_com_fa:
		dict_fa[individuo_com_fa['individuo']] = individuo_com_fa['fa']
	
	individuo_fa = dict_fa.items()
	
	return individuo_fa	


'''_______________________________________________________
   __________________Definindo Roleta ____________________'''

def definindo_roleta(populacao_individuo_fa):
	individuo_fa_roleta = []
	fa_roleta_acomulado = 0
	
	for individuo_fa in populacao_individuo_fa:
		
		if individuo_fa[1] == 0:
			fa_roleta = 100000
			fa_roleta_acomulado += fa_roleta
			tupla_aux = individuo_fa[0], individuo_fa[1], fa_roleta, fa_roleta_acomulado
			individuo_fa_roleta.append(tupla_aux)
		
		else:
			fa_roleta = (1 / individuo_fa[1]) * 100000
			fa_roleta = int(round(fa_roleta))
			fa_roleta_acomulado += fa_roleta
			tupla_aux = individuo_fa[0], individuo_fa[1], fa_roleta, fa_roleta_acomulado
			individuo_fa_roleta.append(tupla_aux)
	
	return individuo_fa_roleta


'''_______________________________________________________
   _____________Definindo tamanho Crossover ______________'''

def crossover(percent_crossover, populacao):
	
	return int((percent_crossover/100) * len(populacao))
'''_______________________________________________________
   _____________Definindo tamanho mutacao ______________'''

def taxa_mutacao(percent_mutacao, populacao):

	return int((percent_mutacao/100) * len(populacao))

'''____________________________________________________
   ______________|| Funções de seleção ||______________'''

'''___________________________________________________
   ________________ Truncamento ______________________'''

def truncamento(individuo_fa_roleta, crossover):
	individuos_selecionados_truncamento = []
	
	vetor_aux_truncamento = sorted(individuo_fa_roleta, key=itemgetter(1))

	if crossover < 2:
		crossover = 2
	
	elif crossover % 2 != 0:
		crossover += 1
	
	else:
		pass

	for individuo in vetor_aux_truncamento:
		
		if crossover > len(individuos_selecionados_truncamento):
			individuos_selecionados_truncamento.append(individuo)
		
		else:
			break
		
	return individuos_selecionados_truncamento



'''_______________________________________________________
   ________________ Torneio simples ______________________'''

def torneio_simples(individuo_fa_roleta, crossover, tour):
	vetor_aux_ts = []
	individuo_selecionado_ts = []
	
	if crossover < 2:
		crossover = 2
	
	elif crossover % 2 != 0:
		crossover += 1
	
	else:
		pass
		
	while (crossover > 0):
		vetor_aux_ts = sample(individuo_fa_roleta, tour)
		vetor_aux_ts = sorted(vetor_aux_ts, key=itemgetter(1))
		
		#if vetor_aux_ts[0] not in individuo_selecionado_ts:
		individuo_selecionado_ts.append(vetor_aux_ts[0])
		crossover -= 1
		
		#else:
			#pass
		
		vetor_aux_ts = []
	
	return individuo_selecionado_ts



'''_____________________________________________________
   _______________________ Roleta ______________________'''


def roleta(individuo_fa_roleta, crossover):
	individuo_selec_roleta = []
	
	primeiro_fa_acomulado = individuo_fa_roleta[0]
	ultimo_fa_acomulado = individuo_fa_roleta[-1]
	
	if crossover < 2:
		crossover = 2
	
	elif crossover % 2 != 0:
		crossover += 1
	
	else:
		pass

	while (crossover > 0):
		num_casa_individuo = randint(primeiro_fa_acomulado[3], ultimo_fa_acomulado[3]) 
		
		for fa_roleta in individuo_fa_roleta:
		
			if num_casa_individuo <= fa_roleta[3]:
				
				#if fa_roleta not in individuo_selec_roleta:
				individuo_selec_roleta.append(fa_roleta)
				crossover -= 1
		
				#else:
					#pass
				
				break
			else:
				pass
	
	return individuo_selec_roleta
	


'''_______________________________________________________
   ________________ Torneio Estocastico __________________'''


def torneio_estocastico(individuo_fa_roleta, crossover, tour):
	vetor_aux_es = []
	individuo_selecionado_te = []
	
	primeiro_fa_acomulado = individuo_fa_roleta[0]
	ultimo_fa_acomulado = individuo_fa_roleta[-1]
	
	if crossover < 2:
		crossover = 2
	
	elif crossover % 2 != 0:
		crossover += 1
	
	else:
		pass

	while(crossover > 0):

		for j in range(tour):
			num_casa_individuo = randint(primeiro_fa_acomulado[3], ultimo_fa_acomulado[3]) 

			for fa_roleta in individuo_fa_roleta:

				if num_casa_individuo <= fa_roleta[3]:
					vetor_aux_es.append(fa_roleta)
					break

				else:
					pass
		
		vetor_aux_es = sorted(vetor_aux_es, key=itemgetter(1))
		
		#if vetor_aux_es[0] not in individuo_selecionado_te:
		individuo_selecionado_te.append(vetor_aux_es[0])
		crossover -= 1

		#else:
		#	pass
		
		vetor_aux_es = []
	
	return individuo_selecionado_te


'''_________________ || Fim funções de seleção || ___________________'''

'''___________________________________________________________________
   ________________ Pegando Somente Individuos _______________________'''

def pega_individuo(individuo_fa_roleta):
	somente_individuos = []

	for individuo in individuo_fa_roleta:
		somente_individuos.append(individuo[0])

	return somente_individuos

'''  _________________ || Metodos de Cruzamento || ____________________'''

'''_______________________________________________________
   ________________ Cruzamento Pmx _______________________'''

def pmx(populacao_crossover):
	indice_populacao_0 = 0
	indice_populacao_1 = 1
	filhos_pmx = []

	
	for controle_repeticao_cruzamento_pmx in range(int(len(populacao_crossover) / 2)):
		
		controlador_cruzamento_pmx_filho_1 = 0
		indice_filho_1_extremo_1 = 0
		indice_filho_1_extremo_2 = 0

		controlador_cruzamento_pmx_filho_2 = 0
		indice_filho_2_extremo_1 = 0
		indice_filho_2_extremo_2 = 0
		
		individuo_1 = populacao_crossover[indice_populacao_0]
		individuo_2 = populacao_crossover[indice_populacao_1]
		
		pai_1 = individuo_1[0]
		pai_2 = individuo_2[0]
		
		filho_1 = pai_1[:3] + pai_2[3:7] + pai_1[7:]
		filho_2 = pai_2[:3] + pai_1[3:7] + pai_2[7:]

		
		'''______________						 ___________
		   ______________|| Cruzamento Filho 1 ||___________'''

		while (controlador_cruzamento_pmx_filho_1 < 6):
			
			if indice_filho_1_extremo_1 < 3:
				
				indice_numero_repete = filho_1.find(filho_1[indice_filho_1_extremo_1], 3)
			
				if indice_numero_repete >= 0:
					filho_1 = filho_1.replace(filho_1[indice_filho_1_extremo_1], filho_2[indice_numero_repete], 1)
			
				else:
					indice_filho_1_extremo_1 += 1
					controlador_cruzamento_pmx_filho_1 += 1
			else:
				
				if indice_filho_1_extremo_1 == 3:
					filho_1 = filho_1[::-1]
					filho_2 = filho_2[::-1]
					indice_filho_1_extremo_1 += 1

				indice_numero_repete = filho_1.find(filho_1[indice_filho_1_extremo_2], 3)
			
				if indice_numero_repete >= 0:
					filho_1 = filho_1.replace(filho_1[indice_filho_1_extremo_2], filho_2[indice_numero_repete], 1)

				else:
					indice_filho_1_extremo_2 += 1
					controlador_cruzamento_pmx_filho_1 += 1

		''' // desinvertendo o filho 1 // '''	
		filho_1 = filho_1[::-1]
		filhos_pmx.append(filho_1)

		'''// Gerando o filho 1 e 2 novamente // '''	
		filho_1 = pai_1[:3] + pai_2[3:7] + pai_1[7:]
		filho_2 = pai_2[:3] + pai_1[3:7] + pai_2[7:]

		'''______________						 ___________
		   ______________|| Cruzamento Filho 2 ||___________''' 

		while (controlador_cruzamento_pmx_filho_2 < 6):
			
			if indice_filho_2_extremo_1 < 3:
				
				indice_numero_repete = filho_2.find(filho_2[indice_filho_2_extremo_1], 3)
			
				if indice_numero_repete >= 0:
					filho_2 = filho_2.replace(filho_2[indice_filho_2_extremo_1], filho_1[indice_numero_repete], 1)
			
				else:
					indice_filho_2_extremo_1 += 1
					controlador_cruzamento_pmx_filho_2 += 1
			else:
				
				if indice_filho_2_extremo_1 == 3:
					filho_2 = filho_2[::-1]
					filho_1 = filho_1[::-1]
					indice_filho_2_extremo_1 += 1

				indice_numero_repete = filho_2.find(filho_2[indice_filho_2_extremo_2], 3)
			
				if indice_numero_repete >= 0:
					filho_2 = filho_2.replace(filho_2[indice_filho_2_extremo_2], filho_1[indice_numero_repete], 1)

				else:
					indice_filho_2_extremo_2 += 1
					controlador_cruzamento_pmx_filho_2 += 1

		''' // desinvertendo o filho 2 // '''	
		filho_2 = filho_2[::-1]
		filhos_pmx.append(filho_2)
		
		''' // incrementando os indices que pegam o individuo da populaçao // '''
		indice_populacao_0 += 2
		indice_populacao_1 += 2

	return filhos_pmx


'''_______________________________________________________
   ________________ Cruzamento Ciclico ___________________'''

def ciclico(populacao_crossover):
	indice_populacao_0 = 0
	indice_populacao_1 = 1
	filhos_ciclico = []

	for controle_repeticao_cruzamento_ciclico in range(int(len(populacao_crossover) / 2)):

		individuo_1 = populacao_crossover[indice_populacao_0]
		individuo_2 = populacao_crossover[indice_populacao_1]
		
		pai_1 = individuo_1[0]
		pai_2 = individuo_2[0]
		
		ponto_inicial_troca = randint(0, 9)

		controle_cruzamento_ciclico_filhos = pai_1[ponto_inicial_troca]

		filho_1 = pai_1.replace(pai_1[ponto_inicial_troca], pai_2[ponto_inicial_troca])
		filho_2 = pai_2.replace(pai_2[ponto_inicial_troca], pai_1[ponto_inicial_troca])
		
		while (controle_cruzamento_ciclico_filhos != filho_1[ponto_inicial_troca]):
			
			pai_1 = filho_1
			pai_2 = filho_2

			indice_numero_repete = filho_1.find(filho_1[ponto_inicial_troca], ponto_inicial_troca + 1)

			if indice_numero_repete > 0:
				
				filho_1_aux = filho_1[::-1]
				filho_2_aux = filho_2[::-1]
				
				filho_1 = filho_1_aux.replace(pai_1[indice_numero_repete], pai_2[indice_numero_repete], 1)
				filho_2 = filho_2_aux.replace(pai_2[indice_numero_repete], pai_1[indice_numero_repete], 1)
				
				filho_1 = filho_1[::-1]
				filho_2 = filho_2[::-1]
				
				ponto_inicial_troca = indice_numero_repete
			
			else:
				
				indice_numero_repete = filho_1.find(filho_1[ponto_inicial_troca])
				
				filho_1 = filho_1.replace(pai_1[indice_numero_repete], pai_2[indice_numero_repete], 1)
				filho_2 = filho_2.replace(pai_2[indice_numero_repete], pai_1[indice_numero_repete], 1)

				ponto_inicial_troca = indice_numero_repete

		filhos_ciclico.append(filho_1)
		filhos_ciclico.append(filho_2)

		''' // incrementando os indices que pegam o individuo da populaçao // '''
		indice_populacao_0 += 2
		indice_populacao_1 += 2


	return filhos_ciclico


'''_______________________________________________________
   ________________ Cruzamento Ciclico ___________________'''

def mutacao(qtd_mutacao, somente_individuos):

	for taxa_mutacao in range(qtd_mutacao):
		
		individuo = randint(0, (len(somente_individuos)-1))
		individuo_auxiliar = somente_individuos[individuo]
		
		ponto_1 = randint(0, 9)
		ponto_2 = randint(0, 9)

		individuo_aleatorio = individuo_auxiliar.replace(individuo_auxiliar[ponto_1], individuo_auxiliar[ponto_2])
		
		individuo_repete = individuo_aleatorio.find(individuo_aleatorio[ponto_1], ponto_1 + 1)

		if individuo_repete > 0:
			individuo_aleatorio = individuo_aleatorio[::-1]
			individuo_aleatorio = individuo_aleatorio.replace(individuo_auxiliar[ponto_2], individuo_auxiliar[ponto_1], 1)
			individuo_aleatorio = individuo_aleatorio[::-1]
		else:
			individuo_aleatorio = individuo_aleatorio.replace(individuo_auxiliar[ponto_2], individuo_auxiliar[ponto_1], 1)

		somente_individuos.remove(individuo_auxiliar)
		somente_individuos.append(individuo_aleatorio)

	return somente_individuos 

'''___________________________________________________________________
   ________________ Metodo Reinserçao Roleta_elite ___________________'''

def roleta_elite(individuo_fa_roleta, tamanho_populacao):
	individuo_selec_roleta = []
	
	primeiro_fa_acomulado = individuo_fa_roleta[0]
	ultimo_fa_acomulado = individuo_fa_roleta[-1]
	
	if tamanho_populacao < 2:
		tamanho_populacao = 2
	
	elif tamanho_populacao % 2 != 0:
		tamanho_populacao += 1
	
	else:
		pass

	vetor_aux_truncamento = sorted(individuo_fa_roleta, key=itemgetter(1))
	individuo_selec_roleta.append(vetor_aux_truncamento[0])

	while (tamanho_populacao > 1):
		num_casa_individuo = randint(primeiro_fa_acomulado[3], ultimo_fa_acomulado[3]) 
		
		for fa_roleta in individuo_fa_roleta:
		
			if num_casa_individuo <= fa_roleta[3]:
				
				#if fa_roleta not in individuo_selec_roleta:
				individuo_selec_roleta.append(fa_roleta)
				tamanho_populacao -= 1
		
				#else:
				#	pass
				
				break
			else:
				pass
	
	return individuo_selec_roleta

'''___________________________________________________________________
   ________________ Pegar o Melhor da Geraçao ___________________'''

def melhor_da_geracao(individuo_fa_roleta, geracao):
	
	vetor_aux_truncamento = sorted(individuo_fa_roleta, key=itemgetter(1))
	
	melhor_geracao = vetor_aux_truncamento[0]
	melhor_geracao = (geracao + 1), melhor_geracao[0], melhor_geracao[1], melhor_geracao[2], melhor_geracao[3]

	return melhor_geracao

	

def index(request):
	form = Formulario()
	
	geracao_filhos = []

	if request.method == 'POST':
		form = Formulario(request.POST)
		
		if form.is_valid():
			
			palavras = [form.cleaned_data['palavra_1'], form.cleaned_data['palavra_2'], form.cleaned_data['palavra_3']]

			letras_unicas = get_letras_unicas(form.cleaned_data['palavra_1'] + form.cleaned_data['palavra_2'] + form.cleaned_data['palavra_3'])

			tamanho_populacao = int(form.cleaned_data['populacao'])

			geracao = int(form.cleaned_data['geracao'])

			metodo_selecao = form.cleaned_data['metodo_selecao']

			tour = int(form.cleaned_data['tour'])

			percent_crossover = int(form.cleaned_data['crossover'])

			met_cross = form.cleaned_data['met_cross']

			percent_mutacao = int(form.cleaned_data['tx_mutacao'])

			met_reinsercao = form.cleaned_data['met_reinsercao']

			

			populacao = gera_populacao(tamanho_populacao)

			qtd_crossover = crossover(percent_crossover, populacao)

			qtd_mutacao = taxa_mutacao(percent_mutacao, populacao)

			populacao_com_fa = gera_fa(populacao, letras_unicas, palavras)

			individuo_fa = gera_lista_tuplas(populacao_com_fa)

			individuo_fa_roleta = definindo_roleta(individuo_fa)


			'''_____________________________________________________________________
			   ___________________ Verificando o Metodo de Seleçao _________________'''


			if metodo_selecao == 'truncamento':

				for geracao in range(geracao):
					individuos_truncamento = truncamento(individuo_fa_roleta, qtd_crossover)
					somente_individuos = pega_individuo(individuo_fa_roleta)

					'''___________Verificando Metodo de Cruzamento_________'''
					if met_cross == 'pmx':
						metodo_pmx = pmx(individuos_truncamento)
						
						for filho_pmx in metodo_pmx:
							somente_individuos.append(filho_pmx)
					else:
						metodo_ciclico = ciclico(individuos_truncamento)
						
						for filho_ciclico in metodo_ciclico:
							somente_individuos.append(filho_ciclico)
					'''_____________________________________________________'''
							
					somente_individuos_com_filhos_mutados = mutacao(qtd_mutacao, somente_individuos)

					populacao_com_fa = gera_fa(somente_individuos_com_filhos_mutados, letras_unicas, palavras)
					individuo_fa = gera_lista_tuplas(populacao_com_fa)
					individuo_fa_roleta = definindo_roleta(individuo_fa)

					melhor_individuo_geracao = melhor_da_geracao(individuo_fa_roleta, geracao)
					geracao_filhos.append(melhor_individuo_geracao)

					if melhor_individuo_geracao[2] == 0:
						
						break
						'''___________________ Verifica o metodo de reinserçao _________________'''
					else:
						if met_reinsercao == 'uniforme':
							individuo_fa_roleta = truncamento(individuo_fa_roleta, tamanho_populacao)

						elif met_reinsercao == 'roleta':
							individuo_fa_roleta = roleta(individuo_fa_roleta, tamanho_populacao)

						else:
							individuo_fa_roleta = roleta_elite(individuo_fa_roleta, tamanho_populacao)

				
			elif metodo_selecao == 'torneio_simples':

				for geracao in range(geracao):
					individuos_torneio_simples = torneio_simples(individuo_fa_roleta, qtd_crossover, tour)
					somente_individuos = pega_individuo(individuo_fa_roleta)

					



					'''___________Verificando Metodo de Cruzamento_________'''
					if met_cross == 'pmx':
						metodo_pmx = pmx(individuos_torneio_simples)
						
						for filho_pmx in metodo_pmx:
							somente_individuos.append(filho_pmx)
					else:
						metodo_ciclico = ciclico(individuos_torneio_simples)
						
						for filho_ciclico in metodo_ciclico:
							somente_individuos.append(filho_ciclico)
					'''_____________________________________________________'''

					somente_individuos_com_filhos_mutados = mutacao(qtd_mutacao, somente_individuos)

					populacao_com_fa = gera_fa(somente_individuos_com_filhos_mutados, letras_unicas, palavras)
					individuo_fa = gera_lista_tuplas(populacao_com_fa)
					individuo_fa_roleta = definindo_roleta(individuo_fa)

					melhor_individuo_geracao = melhor_da_geracao(individuo_fa_roleta, geracao)
					geracao_filhos.append(melhor_individuo_geracao)

					if melhor_individuo_geracao[2] == 0:
						
						break
						'''___________________ Verifica o metodo de reinserçao _________________'''
					else:

						if met_reinsercao == 'uniforme':
							individuo_fa_roleta = truncamento(individuo_fa_roleta, tamanho_populacao)

						elif met_reinsercao == 'roleta':
							individuo_fa_roleta = roleta(individuo_fa_roleta, tamanho_populacao)

						else:
							individuo_fa_roleta = roleta_elite(individuo_fa_roleta, tamanho_populacao)
			

			





			elif metodo_selecao == 'torneio_estocastico':

				for geracao in range(geracao):
					individuos_torneio_estocastico = torneio_estocastico(individuo_fa_roleta, qtd_crossover, tour)
					somente_individuos = pega_individuo(individuo_fa_roleta)

					'''___________Verificando Metodo de Cruzamento_________'''
					if met_cross == 'pmx':
						metodo_pmx = pmx(individuos_torneio_estocastico)
						
						for filho_pmx in metodo_pmx:
							somente_individuos.append(filho_pmx)
					else:
						metodo_ciclico = ciclico(individuos_torneio_estocastico)
						
						for filho_ciclico in metodo_ciclico:
							somente_individuos.append(filho_ciclico)
					'''_____________________________________________________'''

					somente_individuos_com_filhos_mutados = mutacao(qtd_mutacao, somente_individuos)

					populacao_com_fa = gera_fa(somente_individuos_com_filhos_mutados, letras_unicas, palavras)
					individuo_fa = gera_lista_tuplas(populacao_com_fa)
					individuo_fa_roleta = definindo_roleta(individuo_fa)

					melhor_individuo_geracao = melhor_da_geracao(individuo_fa_roleta, geracao)
					geracao_filhos.append(melhor_individuo_geracao)

					if melhor_individuo_geracao[2] == 0:
						
						break
						
						'''___________________ Verifica o metodo de reinserçao _________________'''
					else:

						if met_reinsercao == 'uniforme':
							individuo_fa_roleta = truncamento(individuo_fa_roleta, tamanho_populacao)

						elif met_reinsercao == 'roleta':
							individuo_fa_roleta = roleta(individuo_fa_roleta, tamanho_populacao)

						else:
							individuo_fa_roleta = roleta_elite(individuo_fa_roleta, tamanho_populacao)

					somente_individuos = pega_individuo(individuo_fa_roleta)
					populacao_com_fa = gera_fa(somente_individuos, letras_unicas, palavras)
					individuo_fa = gera_lista_tuplas(populacao_com_fa)
					individuo_fa_roleta = definindo_roleta(individuo_fa)

			





			else:
	
				for geracao in range(geracao):
					individuos_roleta = roleta(individuo_fa_roleta, qtd_crossover)
					somente_individuos = pega_individuo(individuo_fa_roleta)

					'''___________Verificando Metodo de Cruzamento_________'''
					if met_cross == 'pmx':
						metodo_pmx = pmx(individuos_roleta)
						
						for filho_pmx in metodo_pmx:
							somente_individuos.append(filho_pmx)
					else:
						metodo_ciclico = ciclico(individuos_roleta)
						
						for filho_ciclico in metodo_ciclico:
							somente_individuos.append(filho_ciclico)
					'''_____________________________________________________'''

					somente_individuos_com_filhos_mutados = mutacao(qtd_mutacao, somente_individuos)

					populacao_com_fa = gera_fa(somente_individuos_com_filhos_mutados, letras_unicas, palavras)
					individuo_fa = gera_lista_tuplas(populacao_com_fa)
					individuo_fa_roleta = definindo_roleta(individuo_fa)

					melhor_individuo_geracao = melhor_da_geracao(individuo_fa_roleta, geracao)
					geracao_filhos.append(melhor_individuo_geracao)

					if melhor_individuo_geracao[2] == 0:
						
						break
						'''___________________ Verifica o metodo de reinserçao _________________'''
					else:

						if met_reinsercao == 'uniforme':
							individuo_fa_roleta = truncamento(individuo_fa_roleta, tamanho_populacao)

						elif met_reinsercao == 'roleta':
							individuo_fa_roleta = roleta(individuo_fa_roleta, tamanho_populacao)

						else:
							individuo_fa_roleta = roleta_elite(individuo_fa_roleta, tamanho_populacao)

					somente_individuos = pega_individuo(individuo_fa_roleta)
					populacao_com_fa = gera_fa(somente_individuos, letras_unicas, palavras)
					individuo_fa = gera_lista_tuplas(populacao_com_fa)
					individuo_fa_roleta = definindo_roleta(individuo_fa)


				


			context = {'populacao_com_fa' : populacao_com_fa, 'geracao_filhos' : geracao_filhos}

			return render(request, 'application/resultado.html', context)

		else:
			return render(request, 'application/index.html', {'form': form})

	else:
		return render(request, 'application/index.html', {'form': form})
