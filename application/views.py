# -*- coding: utf-8 -*-
from random import randint, sample, shuffle

from operator import itemgetter

from django.shortcuts import render

from .forms import Formulario

#----------------- função para gerar o vetor de letras unicas --------------------
def get_letras_unicas(palavras):
	letras_unicas = []
	for l in palavras:
		if l not in letras_unicas:
			letras_unicas.append(l) 
	return letras_unicas

#----------------- função para gerar a população de individuos -------------------
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

#----------------- função que gera os fa's dos individuos -------------------------
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

#------------------ função que ordena os fa's --------------------------------------	
def ordena_fa(populacao_com_fa):
	dict_fa = {}
	individuo_fa_ordenado = []
	for individuo_com_fa in populacao_com_fa:
		dict_fa[int(individuo_com_fa['individuo'])] = individuo_com_fa['fa']
	individuo_fa_ordenado = sorted(dict_fa.items(), key=itemgetter(1))
	return individuo_fa_ordenado	

#-----|| Funções de seleção ||----------

#--------------------- Truncamento -------------------------
def truncamento(individuo_fa_ordenado):
	individuos_selecionados_truncamento = []
	for individuo_melhor_fa in individuo_fa_ordenado:
		if len(individuos_selecionados_truncamento) < 4:
			individuos_selecionados_truncamento.append(individuo_melhor_fa)
	return individuos_selecionados_truncamento

#--------------------- Torneio simples ----------------------
def torneio_simples(populacao_individuo_fa):
	vetor_aux_ts = []
	individuo_selecionado_ts = []
	shuffle(populacao_individuo_fa)
	for i in range(4):
		vetor_aux_ts = sample(populacao_individuo_fa, 3)
		vetor_aux_ts = sorted(vetor_aux_ts, key=itemgetter(1))
		individuo_selecionado_ts.append(vetor_aux_ts[0])
		vetor_aux_ts = []
	return individuo_selecionado_ts

#---------------------- Roleta -------------------------------
def roleta(populacao_individuo_fa):
	individuo_fa_roleta = []
	fa_roleta_acomulado = 0
	shuffle(populacao_individuo_fa)
	for individuo_fa in populacao_individuo_fa:
		if individuo_fa[1] == 0:
			fa_roleta = 100000
			fa_roleta_acomulado += fa_roleta
			tupla_aux = individuo_fa[0], individuo_fa[1], fa_roleta, fa_roleta_acomulado
			individuo_fa_roleta.append(tupla_aux)
		else:
			fa_roleta = str((1 / individuo_fa[1]) * 100000)
			fa = int(fa_roleta[fa_roleta.index('.') + 1])
			if fa >= 5:
				fa_roleta = float(fa_roleta)
				fa_roleta = int(fa_roleta) + 1
				fa_roleta_acomulado += fa_roleta
				tupla_aux = individuo_fa[0], individuo_fa[1], fa_roleta, fa_roleta_acomulado
				individuo_fa_roleta.append(tupla_aux)
			else:
				fa_roleta = float(fa_roleta)
				fa_roleta = int(fa_roleta)
				fa_roleta_acomulado += fa_roleta
				tupla_aux = individuo_fa[0], individuo_fa[1], fa_roleta, fa_roleta_acomulado
				individuo_fa_roleta.append(tupla_aux)
	return individuo_fa_roleta

#-------------------- Torneio estocástico ---------------------
def torneio_estocastico(individuo_fa_roleta):
	vetor_aux_es = []
	individuo_selecionado_te = []
	primeiro_fa_acomulado = individuo_fa_roleta[0]
	ultimo_fa_acomulado = individuo_fa_roleta[-1]
	for i in range(4):
		for j in range(3):
			num_casa_individuo = randint(primeiro_fa_acomulado[3], ultimo_fa_acomulado[3]) 
			for fa_roleta in individuo_fa_roleta:
				if num_casa_individuo <= fa_roleta[3]:
					vetor_aux_es.append(fa_roleta)
					break
				else:
					pass
		vetor_aux_es = sorted(vetor_aux_es, key=itemgetter(1))
		individuo_selecionado_te.append(vetor_aux_es[0])
		vetor_aux_es = []
	return individuo_selecionado_te

#----------------- || Fim funções de seleção || ------------------

def index(request):
	form = Formulario()

	if request.method == 'POST':
		form = Formulario(request.POST)
		if form.is_valid():

			# Gerando populacao
			palavras = [form.cleaned_data['palavra_1'], form.cleaned_data['palavra_2'], form.cleaned_data['palavra_3']]

			letras_unicas = get_letras_unicas(form.cleaned_data['palavra_1'] + form.cleaned_data['palavra_2'] + form.cleaned_data['palavra_3'])
			
			populacao = gera_populacao(int(form.cleaned_data['populacao']))

			populacao_com_fa = gera_fa(populacao, letras_unicas, palavras)

			individuo_fa_ordenado = ordena_fa(populacao_com_fa)

			individuos_truncamento = truncamento(individuo_fa_ordenado)

			individuos_ts = torneio_simples(individuo_fa_ordenado)

			roleta_fa = roleta(individuo_fa_ordenado)

			individuo_te = torneio_estocastico(roleta_fa)

			context = {'populacao_com_fa' : populacao_com_fa, 'individuo_fa_ordenado' : individuo_fa_ordenado}

			return render(request, 'application/resultado.html', context)

		else:
			return render(request, 'application/index.html', {'form': form})

	else:
		return render(request, 'application/index.html', {'form': form})
