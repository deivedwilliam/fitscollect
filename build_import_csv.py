from astropy.io import fits
from pathlib import Path
import csv
import os
import string


baseDirectories = ['/mnt/Jupiter/OPD/', '/mnt/Callisto/camargo/OPD/']

atribute = [
	'filename',
	'path',
	'object',
	'exposure',
	'date-obs',
	'ra',
	'dec',
	'telescop',
	'instrume',
	'observer',
	'filter',
	'file_size'
	]

keys = [
	'OBJECT',
	'EXPOSURE',
	'DATE-OBS',
	'RA',
	'DEC',
	'TELESCOP',
	'INSTRUME',
	'OBSERVER',
	'FILTER'
]


eso_wfiDict = {
	'RA':['RA'],
	'DEC':['DEC'],
	'EXPOSURE':['EXPTIME'],
	'DATE-OBS':['DATE-OBS'],
	'TELESCOP':['TELESCOP'],
	'INSTRUME':['INSTRUME'],
	'OBSERVER':['OBSERVER'],
	'FILTER':['FILT1NAM'],
	'OBJECT':['OBJECT']
}

ikonDict = {
	'RA':['RA'],
	'DEC':['DEC'],
	'EXPOSURE':['EXPOSURE', 'EXPTIME'],
	'DATE-OBS':['DATE-OBS', 'FRAME'],
	'TELESCOP':['TELESCOP'],
	'INSTRUME':['INSTRUME'],
	'OBSERVER':['OBSERVER'],
	'FILTER':['FILTER','FILTERS'],
	'OBJECT':['OBJECT']
}

ixonDict = {
	'RA':['RA'],
	'DEC':['DEC'],
	'EXPOSURE':['EXPOSURE', 'EXPTIME'],
	'DATE-OBS':['FRAME', 'DATE-OBS'],
	'TELESCOP':['TELESCOP'],
	'INSTRUME':['INSTRUME'],
	'OBSERVER':['OBSERVER'],
	'FILTER':['FILTER', 'FILTERS'],
	'OBJECT':['OBJECT']
}

goodmanDict = {
	'RA':['RA'],
	'DEC':['DEC'],
	'EXPOSURE':['EXPTIME'],
	'DATE-OBS':['DATE-OBS'],
	'TELESCOP':['TELESCOP'],
	'INSTRUME':['INSTRUME'],
	'OBSERVER':['OBSERVER'],
	'FILTER':['FILTER'],
	'OBJECT':['OBJECT']
}

raptorDict = {
	'RA':['RA'],
	'DEC':['DEC'],
	'EXPOSURE':['EXP_TIME'],
	'DATE-OBS':['TIMESTMP'],
	'TELESCOP':['TELESCOP'],
	'OBSERVER':['OBSV'],
	'FILTER':['FILTER'],
	'OBJECT':['TARGET']
}


dirlist = {
	'goodman':[],
	'raptor':[],
	'ixon':[],
	'ikon':[],
	'wfi':[]
}

dicts = {
    'goodman':goodmanDict,
    'raptor': raptorDict,
    'ixon': ixonDict,
    'ikon':ikonDict,
    'wfi': eso_wfiDict
}

def comp(inst, key, header):
	
	qkeys = len(dicts[inst][key])
	
	for k in range(0, qkeys):
		try:
			
			value = header[dicts[inst][key][k]]
			
			return value
		
		except KeyError:
			
			print('Key Error: ', key)
			
	return 'Unknown'

dir_file = open('paths.csv', 'r', newline='\n')
log = open('log_build_import.txt', 'w', newline='\n')
csvfile = open('table_import.csv', 'w', newline='\n')
csv_writer = csv.DictWriter(csvfile, fieldnames = atribute, delimiter = ';')
readC = csv.DictReader(dir_file, delimiter = ';')
csv_writer.writeheader()

for row in readC:
	
	srow = dict()
	
	hdul = fits.open(os.path.join(row['path'], row['filename']), ignore_missing_end=True , lazy_load_hdus=False)
	
	print(row['filename'])
	
	try:
		hdul.verify('silentfix+ignore')
	
	except AttributeError:
		log.write('AttributeErros '.format(os.path.join(row['path'], row['filename'])))
		break
	
	try:
		headerFits = hdul[1].header
	except IndexError:
		headerFits = hdul[0].header
		
	srow.update({
		'filename': row['filename'],
		'path': row['path'],
		'file_size': os.path.getsize(os.path.join(row['path'], row['filename']))
	})
	
	if row['path'].lower().count('ikon') > 0:

		for prop in keys:
			
			prop_name = prop.lower()
			value = comp('ikon', prop, headerFits)

			srow.update({
				prop_name: value
			})
		csv_writer.writerow(srow)


	elif row['path'].lower().count('ixon') > 0:
		for prop in keys:
			
			prop_name = prop.lower()
			value = comp('ixon', prop, headerFits)

			srow.update({
				prop_name: value
			})
		csv_writer.writerow(srow)
	
	elif row['path'].lower().count('goodman') > 0:
		for prop in keys:
			
			prop_name = prop.lower()
			value = comp('goodman', prop, headerFits)

			srow.update({
				prop_name: value
			})
		csv_writer.writerow(srow)

	elif row['path'].lower().count('raptor') > 0:
		for prop in keys:
			
			prop_name = prop.lower()
			value = comp('raptor', prop, headerFits)

			srow.update({
				prop_name: value
			})
		csv_writer.writerow(srow)

	elif row['path'].lower().count('wfi') > 0:
		for prop in keys:
			
			prop_name = prop.lower()
			value = comp('wfi', prop, headerFits)

			srow.update({
				prop_name: value
			})
		csv_writer.writerow(srow)

	del srow