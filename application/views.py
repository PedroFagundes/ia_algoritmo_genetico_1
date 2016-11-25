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
	fa = ''
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


'''____________________________________________________
   ______________|| Funções de seleção ||______________'''

'''___________________________________________________
   ________________ Truncamento ______________________'''

def truncamento(individuo_fa_roleta, crossover):
	individuos_selecionados_truncamento = []
	vetor_aux_truncamento = []
	
	vetor_aux_truncamento = sorted(individuo_fa_roleta, key=itemgetter(1))

	if crossover < 2:
		crossover = 2
	
	elif crossover % 2 != 0:
		crossover += 1
	
	else:
		pass

	for individuo_melhor_fa in vetor_aux_truncamento:
		
		if len(individuos_selecionados_truncamento) < crossover:
			individuos_selecionados_truncamento.append(individuo_melhor_fa)
	
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
		
		if vetor_aux_ts[0] not in individuo_selecionado_ts:
			individuo_selecionado_ts.append(vetor_aux_ts[0])
			crossover -= 1
		
		else:
			pass
		
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
				
				if fa_roleta not in individuo_selec_roleta:
					individuo_selec_roleta.append(fa_roleta)
					crossover -= 1
		
				else:
					pass
				
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
		
		if vetor_aux_es[0] not in individuo_selecionado_te:
			individuo_selecionado_te.append(vetor_aux_es[0])
			crossover -= 1

		else:
			pass
		
		vetor_aux_es = []
	
	return individuo_selecionado_te


'''_________________ || Fim funções de seleção || ___________________

   _________________ || Metodos de Cruzamento || ____________________'''

def pmx(populacao_crossover):
	indice_populacao_0 = 0
	indice_populacao_1 = 1
	filhos = []

	
	for controle_repeticao_cruzamento in range(int(len(populacao_crossover) / 2)):
		
		controlador_individuo_1 = 0
		indice_filho_1_extremo_1 = 0
		indice_filho_1_extremo_2 = 0

		controlador_individuo_2 = 0
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

		while (controlador_individuo_1 < 6):
			
			if indice_filho_1_extremo_1 < 3:
				
				indice_numero_repete = filho_1.find(filho_1[indice_filho_1_extremo_1], 3)
			
				if indice_numero_repete >= 0:
					filho_1 = filho_1.replace(filho_1[indice_filho_1_extremo_1], filho_2[indice_numero_repete], 1)
			
				else:
					indice_filho_1_extremo_1 += 1
					controlador_individuo_1 += 1
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
					controlador_individuo_1 += 1

		''' // desinvertendo o filho 1 // '''	
		filho_1 = filho_1[::-1]
		filhos.append(filho_1)

		'''// Gerando o filho 1 e 2 novamente // '''	
		filho_1 = pai_1[:3] + pai_2[3:7] + pai_1[7:]
		filho_2 = pai_2[:3] + pai_1[3:7] + pai_2[7:]

		'''______________						 ___________
		   ______________|| Cruzamento Filho 2 ||___________''' 

		while (controlador_individuo_2 < 6):
			
			if indice_filho_2_extremo_1 < 3:
				
				indice_numero_repete = filho_2.find(filho_2[indice_filho_2_extremo_1], 3)
			
				if indice_numero_repete >= 0:
					filho_2 = filho_2.replace(filho_2[indice_filho_2_extremo_1], filho_1[indice_numero_repete], 1)
			
				else:
					indice_filho_2_extremo_1 += 1
					controlador_individuo_2 += 1
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
					controlador_individuo_2 += 1

		''' // desinvertendo o filho 2 // '''	
		filho_2 = filho_2[::-1]
		filhos.append(filho_2)
		
		''' // incrementando os indices que pegam o individuo da populaçao // '''
		indice_populacao_0 += 2
		indice_populacao_1 += 2

	return filhos



	
def index(request):
	form = Formulario()

	if request.method == 'POST':
		form = Formulario(request.POST)
		if form.is_valid():

			# Gerando populacao
			palavras = [form.cleaned_data['palavra_1'], form.cleaned_data['palavra_2'], form.cleaned_data['palavra_3']]

			tour = int(form.cleaned_data['tour'])

			percent_crossover = int(form.cleaned_data['crossover'])

			letras_unicas = get_letras_unicas(form.cleaned_data['palavra_1'] + form.cleaned_data['palavra_2'] + form.cleaned_data['palavra_3'])
			
			populacao = gera_populacao(int(form.cleaned_data['populacao']))

			qtd_crossover = crossover(percent_crossover, populacao)

			populacao_com_fa = gera_fa(populacao, letras_unicas, palavras)

			individuo_fa = gera_lista_tuplas(populacao_com_fa)

			individuo_fa_roleta = definindo_roleta(individuo_fa)

			individuos_truncamento = truncamento(individuo_fa_roleta, qtd_crossover)

			individuos_ts = torneio_simples(individuo_fa_roleta, qtd_crossover, tour)

			individuos_te = torneio_estocastico(individuo_fa_roleta, qtd_crossover, tour)

			individuo_selec_roleta = roleta(individuo_fa_roleta, qtd_crossover)

			metpmx = pmx(individuos_ts)

			context = {'populacao_com_fa' : populacao_com_fa, 'individuo_fa' : individuo_fa, 'individuos_te' : individuos_te}

			return render(request, 'application/resultado.html', context)

		else:
			return render(request, 'application/index.html', {'form': form})

	else:
		return render(request, 'application/index.html', {'form': form})
