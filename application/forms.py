# -*- coding: utf-8 -*-
from django import forms


class Formulario(forms.Form):
	palavra_1 = forms.CharField()
	palavra_2 = forms.CharField()
	palavra_3 = forms.CharField()
	populacao = forms.CharField()
	crossover = forms.CharField()
	tx_mutacao = forms.CharField()
	tour = forms.CharField() 
	metodo_selecao = forms.CharField()
	geracao = forms.CharField()
	met_cross = forms.CharField()
	met_reinsercao = forms.CharField()