import yaml
import json 

DESC_WORDS = 30
DESC_SEP1 = '<div class="english-col" markdown="1">'
DESC_SEP2 = '</div>'

with open('_data/galleries/overview.yml', 'r') as yml:
	overview = yaml.safe_load(yml)
latest = overview[0]
params = dict()

params['title'] = latest['title']
params['date'] = latest['date']
params['page'] = latest['directory']
params['img'] = f'{latest["directory"]}/{latest["preview"]["thumbnail"]}'

with open(f'galleries/{params["page"]}.md') as f:
	text = f.read()

desc = text.split(DESC_SEP1)[1].split(DESC_SEP2)[0].replace('\n',' ').replace('\r','').strip().split(' ')[:DESC_WORDS]
desc = ' '.join(desc)
if desc.endswith(','):
	desc = desc[:-1]
desc = desc + '..' if desc.endswith('.') else desc + '...'
params['desc'] = desc

with open('assets/site/latest/params.json', 'w') as outfile:
	json.dump(params, outfile, indent=2)

print('Update complete.')