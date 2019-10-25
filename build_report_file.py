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

report = open('report.csv','w', newline='\n')
csvfile = open('table.csv', 'w', newline='\n')
log = open('log_table.txt', 'w', newline='\n')

reportWrite = csv.DictWriter(report, fieldnames = atribute, delimiter = ';')
csv_writer = csv.DictWriter(csvfile, fieldnames = atribute, delimiter = ';')

csv_writer.writeheader()
reportWrite.writeheader()


emptyFileCounter = 0
ocutFileCounter = 0
fitsFileCounter = 0
csvMappedFilesCounter = 0
filesKeyWordsMs = 0
emptyFile = True
for dirr in baseDirectories:
	for p, _, files in os.walk(os.path.abspath(dirr)):
		for file in files:
			if file.endswith('.fits') == True:
				try:

					hdul = fits.open(os.path.join(p, file),ignore_missing_end=True ,lazy_load_hdus=False)
					print(file)
					try:
						hdul.verify('silentfix+ignore')
					except AttributeError:
						log.write('AttributeErros '.format(os.path.join(p, file)))
						break

					try:
						headerFits = hdul[1].header
					except IndexError:
						headerFits = hdul[0].header

					fitsFileCounter += 1
					headerKeys = headerFits.keys()
					
					if 'KCT' in headerKeys:
						ocutFileCounter += 1
					else:	
						row = dict()
						reportRow = dict()

						row.update({
							'filename': file,
							'path': p
						})

						row.update({
							'file_size':os.path.getsize(os.path.join(p, file))
						})

						for prop in keys:
							try:
								
								prop_name = prop.lower()
								value = headerFits[prop]
								
								'''
								if prop == 'INSTRUME':
									value = translInstru[value]
								'''
								row.update({
									prop_name: value
								})

								reportRow.update({
									'filename': file,
									'path': p,
									prop_name: 'S'
								})

							except KeyError:

								reportRow.update({
									'filename': file,
									'path': p,
									prop_name: 'N'
								})

								emptyFile = False

						if not emptyFile:

							reportRow.update({
								'file_size':os.path.getsize(os.path.join(p, file))
							})

							reportWrite.writerow(reportRow)
							emptyFile = True
							filesKeyWordsMs += 1

						else:
							csv_writer.writerow(row)
							csvMappedFilesCounter += 1

						hdul.close()
						del row
						del reportRow
				except OSError:
					log.write('Não abriu {}\n'.format(os.path.join(p, file)))


log.write('Quantidade de arquivos FITS: {}\n'.format(fitsFileCounter))
log.write('Arquivos com todas as palavras chaves: {}\n'.format(csvMappedFilesCounter))
log.write('Arquivos com uma ou mais chaves faltando: {}'.format(filesKeyWordsMs))
log.write('Arquivos de ocutação: {}\n'.format(ocutFileCounter))