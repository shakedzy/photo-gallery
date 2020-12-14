import os
import argparse
from PIL import Image, ExifTags
from datetime import datetime

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-n', '--name', dest='gallery_name', required=True, help='Gallery directory name')
	parser.add_argument('-p', '--preview', dest='preview', default=1, help='Image number of preview photo')
	parser.add_argument('-t', '--title', dest='title', help='Gallery title')
	parser.add_argument('-d', '--date', dest='date', help='Gallery shooting date')
	parser.add_argument('-z', '--zfill', dest='zfill', default=4, help='Number of total figures in files names')
	parser.add_argument('-x', '--suffix', dest='suffix', default="JPG", help="Files suffix")
	parser.add_argument('-ts', '--thumbnail-size', dest='thumbnail_size', default='600,400', help="Width and height of thumbnails")
	parser.add_argument('-st', '--skip-thumbs', dest='skip_thumbnails', default=False, action='store_true', help="Don't create thumbnails (assume they already exist)")
	parser.add_argument('-so', '--skip-overview', dest='skip_overview', default=False, action='store_true', help="Don't add gallery to overview.yml")
	parser.add_argument('-sg', '--skip-gallery', dest='skip_gallery', default=False, action='store_true', help="Don't add gallery md file")
	parser.add_argument('-he', '--hide-exif', dest='hide_exif', default=False, action='store_true', help="Do not show EXIF metadata")
	args = parser.parse_args()

	photos_path = os.getcwd() + "/assets/photography/" + args.gallery_name
	photos = [name for name in os.listdir(photos_path) if os.path.isfile(os.path.join(photos_path, name)) and name.endswith(args.suffix) and 'thumbnail' not in name]
	num_of_photos = len(photos)
	prefix = photos[0].split('-', 1)[0]

	def get_image_name_from_id(n):
		return f'{prefix}-{str(n).zfill(args.zfill)}'

	def get_image_thumbnail_name(name):
		return f'{name}-thumbnail.{args.suffix}'

	if not args.skip_thumbnails:
		th_width, th_height = [int(i) for i in args.thumbnail_size.split(',')]
		for photo in photos:
			thumbnail_size = (th_width, th_width) if th_width > th_height else (th_height, th_height)
			thumbnail_filename = get_image_thumbnail_name(photo)
			im = Image.open(os.path.join(photos_path, photo))
			im.thumbnail(thumbnail_size, Image.ANTIALIAS)
			im.save(os.path.join(photos_path, thumbnail_filename))

	min_date = None
	max_date = None
	with open(os.getcwd() + f'/_data/galleries/{args.gallery_name}.yml', 'w+') as f:
		f.write(f'picture_path: {args.gallery_name} \n')
		f.write('pictures: \n')
		for i in range(1, num_of_photos+1):
			photo = get_image_name_from_id(i)
			f.write(f'- filename: {photo} \n')
			f.write(f'  original: {photo}.{args.suffix} \n')
			f.write(f'  thumbnail: {get_image_thumbnail_name(photo)} \n')
			f.write('  exif: \n')
			im = Image.open(os.path.join(photos_path, f'{photo}.{args.suffix}'))
			exif = dict()
			exif_info = {ExifTags.TAGS[k]: v for k, v in im._getexif().items() if k in ExifTags.TAGS}
			exif['model'] = exif_info.get('Model', '?')
			exif['lens'] = exif_info.get('LensModel', None)
			exif['aperture'] = str(exif_info['FNumber'][0] / exif_info['FNumber'][1]) if 'FNumber' in exif_info else '?'
			exif['shutter'] = f"{exif_info['ExposureTime'][0]}/{exif_info['ExposureTime'][1]}" if 'ExposureTime' in exif_info else '?'
			exif['focal'] = int(exif_info['FocalLength'][0] / exif_info['FocalLength'][1]) if 'FocalLength' in exif_info else '?'
			exif['iso'] = exif_info.get('ISOSpeedRatings', '?')
			exif['datetime'] = exif_info.get('DateTime', '?')
			for k,v in exif.items():
				if v is not None:
					f.write(f'    {k}: {v} \n')
			if args.hide_exif:
				f.write(f'    hide_exif: true \n')
			if exif['datetime']:
				dt = datetime.strptime(exif['datetime'], '%Y:%m:%d %H:%M:%S').date()
				if min_date is None: min_date = dt
				elif min_date > dt: min_date = dt
				if max_date is None: max_date = dt
				elif max_date < dt: max_date = dt

	date = ''
	if args.date:
		date = args.date
	else:
		if min_date is None or max_date is None:
			pass
		elif min_date == max_date:
			date = max_date.strftime("%d/%m/%Y")
		elif min_date.month == max_date.month and min_date.year == max_date.year:
			date = f"{min_date.strftime('%d')}-{max_date.strftime('%d/%m/%Y')}"
		else:
			date = f"{min_date.strftime('%d/%m/%Y')} - {max_date.strftime('%d/%m/%Y')}"
	date = date or 'Who knows when...'

	if not args.skip_overview:
		with open(os.getcwd() + '/_data/galleries/overview.yml', 'r+') as f:
			photo = get_image_name_from_id(args.preview)
			content = f.read()
			f.seek(0, 0)
			f.write('- \n')
			f.write(f' title: {args.title or args.gallery_name} \n')
			f.write(f' directory: {args.gallery_name} \n')
			f.write(f' date: {date} \n')
			f.write(' preview: \n')
			f.write(f'  filename: {photo} \n')
			f.write(f'  original: {photo}.{args.suffix} \n')
			f.write(f'  thumbnail: {get_image_thumbnail_name(photo)} \n')
			f.write(content)

	if not args.skip_gallery:
		with open(os.getcwd() + f'/galleries/{args.gallery_name}.md', 'w+') as f:
			f.write('--- \n')
			f.write('layout: gallery \n')
			f.write(f'title: {args.title or args.gallery_name} \n')
			f.write(f'date: {date} \n')
			f.write('no_menu_item: true \n') 
			f.write('support: [jquery, gallery] \n')
			f.write('--- \n\n\n')
			f.write('{% include gallery-layout.html gallery=site.data.galleries.' + args.gallery_name + ' %} \n')
