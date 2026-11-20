# -*- coding: utf-8 -*-
"""
	cocoesp - DivxTotal (castellano). Spec 006.
	Búsqueda y rutas basadas en el canal de Alfa (alfa-addon/addon, GPL-3.0).
"""
from cocoesp.modules.spanish_sites import SpanishTorrentSite


class source(SpanishTorrentSite):
	site_name = 'divxtotal'
	url_setting = 'divxtotal.url'
	default_domain = 'https://divxtotal.foo'
	search_path = '/?s=%s'
	movie_link_re = r'/peliculas[^/]*/[^/?#]+'
