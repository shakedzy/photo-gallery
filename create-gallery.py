import os
import argparse
from PIL import Image

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-n', '--name', dest='gallery_name', required=True, help='Gallery directory name')
	parser.add_argument('-p', '--preview', dest='preview', required=True, help='Image number of preview photo')
	parser.add_argument('-t', '--title', dest='title', required=True, help='Gallery title')
	parser.add_argument('-d', '--date', dest='date', required=True, help='Gallery shooting date')
	parser.add_argument('-z', '--zeroes', dest='zeroes', default=4, help='Number of total figures in files names')
	parser.add_argument('-s', '--skip', dest='skip_all', default=False, action='store_true', help="Skip both overview and gallery")
	parser.add_argument('-ts', '--thumbnail-size', dest='thumbnail_size', default='600,400', help="Width and height of thumbnails")
	parser.add_argument('-nt', '--no-thumbs', dest='no_thumbnails', default=False, action='store_true', help="Don't create thumbnails (assume they already exist)")
	parser.add_argument('-so', '--skip-overview', dest='skip_overview', default=False, action='store_true', help="Don't add gallery to overview.yml")
	parser.add_argument('-sg', '--skip-gallery', dest='skip_gallery', default=False, action='store_true', help="Don't add gallery md file")
	args = parser.parse_args()

	SUFFIX = '.JPG'

	photos_path = os.getcwd() + "/assets/photography/" + args.gallery_name
	photos = [name for name in os.listdir(photos_path) if os.path.isfile(os.path.join(photos_path, name)) and name.endswith(SUFFIX) and 'thumbnail' not in name]
	num_of_photos = len(photos)
	prefix = photos[0].split('-', 1)[0]

	def get_image_name(n, original=False, thumbnail=False):
		s = f'{prefix}-{str(n).zfill(args.zeroes)}'
		if thumbnail: s += '-thumbnail' + SUFFIX
		elif original: s += SUFFIX
		return s

	if not args.no_thumbnails:
		width, height = [int(i) for i in args.thumbnail_size.split(',')]
		for photo in photos:
			thumbnail_size = (width, width) if width > height else (height, height)
			thumbnail_filename = f'{photo[:-len(SUFFIX)]}-thumbnail{SUFFIX}'
			im = Image.open(os.path.join(photos_path, photo))
			im.thumbnail(thumbnail_size, Image.ANTIALIAS)
			im.save(os.path.join(photos_path, thumbnail_filename))

	with open(os.getcwd() + f'/_data/galleries/{args.gallery_name}.yml', 'w+') as f:
		f.write(f'picture_path: {args.gallery_name} \n')
		f.write('pictures: \n')
		for i in range(1, num_of_photos+1):
			f.write(f'- filename: {get_image_name(i)} \n')
			f.write(f'  original: {get_image_name(i, original=True)} \n')
			f.write(f'  thumbnail: {get_image_name(i, thumbnail=True)} \n')

	if not (args.skip_all or args.skip_overview):
		with open(os.getcwd() + '/_data/galleries/overview.yml', 'r+') as f:
			content = f.read()
			f.seek(0, 0)
			f.write('- \n')
			f.write(f' title: {args.title or args.gallery_name} \n')
			f.write(f' directory: {args.gallery_name} \n')
			f.write(f' date: {args.date} \n')
			f.write(' preview: \n')
			f.write(f'  filename: {get_image_name(args.preview)} \n')
			f.write(f'  original: {get_image_name(args.preview, original=True)} \n')
			f.write(f'  thumbnail: {get_image_name(args.preview, thumbnail=True)} \n')
			f.write(content)

	if not (args.skip_all or args.skip_gallery):
		with open(os.getcwd() + f'/galleries/{args.gallery_name}.md', 'w+') as f:
			f.write('--- \n')
			f.write('layout: gallery \n')
			f.write(f'title: {args.title} \n')
			f.write(f'date: {args.date} \n')
			f.write('no_menu_item: true \n') 
			f.write('support: [jquery, gallery] \n')
			f.write('--- \n\n\n')
			f.write('{% include gallery-layout.html gallery=site.data.galleries.' + args.gallery_name + ' %} \n')
