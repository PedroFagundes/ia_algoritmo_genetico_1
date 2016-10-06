# -*- coding: utf-8 -*-
from random import randint

from django.shortcuts import render

from .forms import Formulario


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


def index(request):
	form = Formulario()

	if request.method == 'POST':
		form = Formulario(request.POST)
		if form.is_valid():

			# Gerando populacao
			populacao = gera_populacao(int(form.cleaned_data['populacao']))
			return render(request, 'application/resultado.html', {'populacao': populacao})

		else:
			return render(request, 'application/index.html', {'form': form})

	else:
		return render(request, 'application/index.html', {'form': form})
