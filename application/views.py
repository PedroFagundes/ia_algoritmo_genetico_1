# -*- coding: utf-8 -*-
from random import randint

from django.shortcuts import render

from .forms import Formulario
 
def get_letras_unicas(palavras):
	letras_unicas = []
	for l in palavras:
		if l not in letras_unicas:
			letras_unicas.append(l) 
	return letras_unicas


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

def gera_fa(populacao, letras_unicas, palavras):
	fa_palavra = ''
	fa = ''
	vetor_individuo_fa = []
	vetor_fa = []
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
		vetor_fa.append(str(fa))
		individuo_gerado = {}
		individuo_gerado['individuo'] = individuo
		individuo_gerado['fa'] = fa
		populacao_com_fa.append(individuo_gerado)
	#import pdb; pdb.set_trace()
	return populacao_com_fa

def index(request):
	form = Formulario()

	if request.method == 'POST':
		form = Formulario(request.POST)
		if form.is_valid():

			# Gerando populacao
			palavras = [form.cleaned_data['palavra_1'], form.cleaned_data['palavra_2'], form.cleaned_data['palavra_3']]

			letras_unicas = get_letras_unicas(form.cleaned_data['palavra_1'] + form.cleaned_data['palavra_2'] + form.cleaned_data['palavra_3'])
			
			populacao = gera_populacao(int(form.cleaned_data['populacao']))

			populacao = gera_fa(populacao, letras_unicas, palavras)

			#import pdb; pdb.set_trace()

			context = {'populacao' : populacao}

			return render(request, 'application/resultado.html', context)

		else:
			return render(request, 'application/index.html', {'form': form})

	else:
		return render(request, 'application/index.html', {'form': form})
