from xbmcgui import dialog
from .tools import save_check, save_move1

def main(NAME, NAME2, VERSION, URL, ICON, FANART, DESCRIPTION):
	
	yesInstall = dialog.yesno(NAME, 'Onze wizard is klaar om uw build te installeren.', nolabel='Annuleer', yeslabel='Ga door')
	if yesInstall:
	    save_check()
	    save_move1()
	    yesFresh = dialog.yesno('Frisse start', 'All data wordt nu eerst verwijderd', nolabel='Stop', yeslabel='Ga door')
	    if yesFresh:
	    	from .freshstart import freshStart
	    	freshStart()
	    from .buildinstall import buildInstall
	    buildInstall(NAME, NAME2, VERSION, URL)
	else:
		return