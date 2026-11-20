# -*- coding: utf-8 -*-
"""
	cocoesp - GranTorrent (castellano). Spec 006.
	Búsqueda y rutas basadas en el canal de Alfa (alfa-addon/addon, GPL-3.0).
	Los .torrent se sirven desde el subdominio files.<dominio>.
"""
from cocoesp.modules.spanish_sites import SpanishTorrentSite


class source(SpanishTorrentSite):
	site_name = 'grantorrent'
	url_setting = 'grantorrent.url'
	default_domain = 'https://grantorrent.zip'
	search_path = '/peliculas/?query=%s'
	movie_link_re = r'/peliculas/[^/?#]+'
