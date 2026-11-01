import json

d = json.load(open('master_site_blueprint.json'))
pages = d['pages']
slugs = [p['slug'] for p in pages]
print('VALID JSON -', len(pages), 'page blueprints')
print('Unique slugs:', len(set(slugs)), '(duplicates:', len(slugs) - len(set(slugs)), ')')

ids = {p['page_id'] for p in pages}
errors = []
for p in pages:
    for link in p.get('internal_links_to', []):
        if link not in ids:
            errors.append(p['page_id'] + ' -> ' + link + ' NOT FOUND')

if errors:
    print('LINK ERRORS:', errors)
else:
    print('All internal links valid')

ta = json.load(open('topical_authority.json'))
ta_ids = {p['page_id'] for p in ta['pages']}
missing = ta_ids - ids
print('Missing from blueprint:', missing if missing else 'None')
print('ALL CHECKS PASSED' if not errors and not missing else 'ISSUES FOUND')

