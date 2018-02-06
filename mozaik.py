
"""
Description: 	Simple script which takes the input image, and fills it 
				with images obtain from a user-provided keyword image search.
				The images downloaded are "Licenced for noncomercial use with 
				modification", the author cannot be held responsible for
				any misuse.

Example: 		python mozaik.py -i "Arnold.jpg" -g "pug" -s 32
"""

import argparse
import requests
import time
import sys
import glob
import json
import pickle
from io import BytesIO
import urllib.request
import numpy as np 
from PIL import Image, ImageFilter
from bs4 import BeautifulSoup


# Get args
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('-i',   '--image',      
                    dest='main_img', 
                    help="Path to desired input image.")
parser.add_argument('-g',   '--google',      
                    dest='google_img', 
                    help="Search term for Google image search.\n"
                    	 "Default extracts the keywords from the\n"
                    	 "input image name.")
parser.add_argument('-s',   '--fsize',      
                    dest='filler_size', 
                    help="Size of the filler images.",
                    default=64)
args = parser.parse_args()

# Load main image
try:
	filename = args.main_img
except Exception as e: 
	print(e)
	print("Using test file")
	filename = 'Arnold.jpg'

# Load google images
try:
	search_term = args.google_img
	search_term = '+'.join(search_term.split(' '))
except Exception as e: 
	print(e)
	print("Estimating search term from filename")
	search_term = filename.split('_')
	search_term[-1] = search_term[-1].split('.')[0]
	search_term = '+'.join(search_term)

IMG_SIZE = int(args.filler_size)
IMG_LIMIT = 50


def getFillers(search_term):
	""" 
	Load filler images from google image search 
	(Licence for noncomercial use with modification)
	"""
	imgs_urls = []
	for color in ['','red', 'orange', 'yellow', 'green', 'teal', 'blue', 'purple', 'pink', 'white', 'gray', 'black', 'brown']:
		if color=='':
			SEARCH_URL = 'https://www.google.com/search?q={}&tbs=sur:fm&source=lnms&tbm=isch'.format(search_term)
		else:
			SEARCH_URL = 'https://www.google.com/search?q={}&tbs=sur:fm,ic:specific,isc:{}&source=lnms&tbm=isch'.format(search_term, color)
		try:
			headers = {}
			headers[
			    'User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
			req = urllib.request.Request(SEARCH_URL, headers=headers)
			resp = urllib.request.urlopen(req)
			html = str(resp.read())
		except Exception as e:
			print(str(e))
		soup = BeautifulSoup(html, "html.parser")
		imgs_urls.append(soup.find_all("div", {'class':'rg_meta'}))
	# num_urls = sum([len(i) for i in imgs_urls])
	num_urls = IMG_LIMIT * len(imgs_urls)
	val_list, img_list = [], []
	print("\nGetting {} images... (This might take a couple of minutes)".format(search_term))
	sys.stdout.write("[%s]" % (" " * 50))
	sys.stdout.flush()
	sys.stdout.write("\b" * (51))
	c,p = 0,2
	for _urls in imgs_urls:
		for k in _urls[:IMG_LIMIT]:
			time.sleep(0.1)
			c+=1
			try:
				url_image = json.loads(k.text)["ou"]
				### load image from url in memory
				img_net = Image.open(requests.get(url_image, stream=True).raw)#.convert('HSV')
				# img_net = Image.open(urllib.request.urlopen(url_image)).convert('HSV')
				if len(np.asarray(img_net).shape)<3 or np.asarray(img_net).shape[2]<3:
					continue
			except Exception as e:
				# print(str(e))
				continue
			### resize and crop
			if img_net.size[1] > img_net.size[0]:
				np_net = np.asarray(img_net.resize((int(img_net.size[1]*IMG_SIZE/img_net.size[0]), IMG_SIZE), Image.ANTIALIAS))
				np_net = np_net[:, int(np_net.shape[1]/2-IMG_SIZE/2):int(np_net.shape[1]/2+IMG_SIZE/2), :]
			else:
				np_net = np.asarray(img_net.resize((IMG_SIZE, int(img_net.size[0]*IMG_SIZE/img_net.size[1])), Image.ANTIALIAS))	
				np_net = np_net[int(np_net.shape[0]/2-IMG_SIZE/2):int(np_net.shape[0]/2+IMG_SIZE/2), :, :]
			### just resize
			# np_net = np.asarray(img_net.resize((IMG_SIZE, IMG_SIZE), Image.ANTIALIAS))
			### edge case
			if np_net.shape[2]>3:
				np_net = np_net[:,:,:3]
			### get average RGB (or HSV or brightness)
			val_avg = np.mean(np_net, axis=(0,1))[::-1]
			### keep track of image pixel values
			img_list.append(np_net)
			val_list.append(val_avg)
			###  print progress
			progress = int(c / num_urls * 100)
			if progress>=p:	
				p += 2
				sys.stdout.write("-")
				sys.stdout.flush()
	sys.stdout.write("\n")
	print('Done. Loaded {} images out of {}.'.format(len(img_list), num_urls))
	return np.array(val_list), np.array(img_list)


def getSimilar(vals, val_list, img_list):
	""" 
	Find the most similar filler image for the appropriate pixel
	"""
	# DeltaE CIE76 (http://www.easyrgb.com/en/math.php)
	# 1) https://en.wikipedia.org/wiki/SRGB
	# 2) https://en.wikipedia.org/wiki/Lab_color_space
 	# 3) https://en.wikipedia.org/wiki/Color_difference#CIE76
	# match RGB equation
	match = np.sum(np.sqrt((val_list - np.tile(vals[::-1], (val_list.shape[0], 1)))**2 * np.array([3,4,2])), axis=1)
	#	
	return img_list[np.argmin(match)]


def populateMain(im, val_list, img_list, uniform=False):
	""" 
	Populate the main image with appropriate filler images
	"""
	# check orientation and keep aspect
	if max(im.size) < 4800:
		if im.size[1] > im.size[0]:	# portrait
			new_h = 4800
			new_w = int(im.size[0]/im.size[1]*new_h)
		else:						# landscape
			new_w = 4800
			new_h = int(im.size[1]/im.size[0]*new_w)
		im = im.resize((new_w, new_h), Image.ANTIALIAS)
	# make placeholders
	img_temp = im.resize((int(im.size[0]/IMG_SIZE), int(im.size[1]/IMG_SIZE)), Image.ANTIALIAS)
	np_temp = np.asarray(img_temp)
	# np_out = np.zeros(np.asarray(im).shape)
	np_out = np.zeros(np_temp.shape*np.array([IMG_SIZE, IMG_SIZE, 1]))
	# progress bar
	print('\nFilling image...')
	sys.stdout.write("[%s]" % (" " * 50))
	sys.stdout.flush()
	sys.stdout.write("\b" * (51))
	c,p = 0,2
	# replace pixels with filler images
	for i in range(int(np_temp.shape[0])):
		for j in range(int(np_temp.shape[1])):
			if not uniform:
				# select image to insert
				block = getSimilar(np_temp[i,j,:], val_list, img_list)
			else:
				# define color block to insert
				block = np.ones((IMG_SIZE, IMG_SIZE, 3))
				block[:,:,:] *= np_temp[i,j,:]
			### insert at location
			np_out[i*IMG_SIZE:i*IMG_SIZE+IMG_SIZE, j*IMG_SIZE:j*IMG_SIZE+IMG_SIZE, :] = block
			###  print progress
			c+=1
			progress = int(c/np.prod(np_temp.shape[:2])*100)
			if progress>=p:	
				# print('Progress: {}%'.format(progress))
				p += 2
				sys.stdout.write("-")
				sys.stdout.flush()
	sys.stdout.write("\n")
	print('Done.')
	img_out = Image.fromarray(np_out.astype('uint8'))
	img_out.show()
	return img_out


if __name__ == "__main__":

	# Load main image
	img_main = Image.open(filename)#.convert('HSV')

	# Load filler images
	if './saved_search/'+search_term+'_IMG{}.pkl'.format(IMG_SIZE) in glob.glob('./saved_search/*.pkl'):
		#load search
		with open('./saved_search/'+search_term+'_IMG{}.pkl'.format(IMG_SIZE), 'rb') as f: 
		    val_list, img_list = pickle.load(f)
	else:
		#save search
		val_list, img_list = getFillers(search_term)
		with open('./saved_search/'+search_term+'_IMG{}.pkl'.format(IMG_SIZE), 'wb') as f:
		    pickle.dump([val_list, img_list], f)

	# Populate the main image
	img_fin = populateMain(img_main, val_list, img_list)

	# Display/save final image
	img_fin.save(filename.split('.')[0]+'_mozaikd.jpg', 'JPEG')



