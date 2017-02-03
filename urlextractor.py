import re
import tldextract
import esm



def extractUrl(text, match):
	pretld, posttld = None, None
	url = ""

	tld = match[1]
	startpt, endpt = match[0][0], match[0][1]

	# check the next character is valid
	if len(text) > endpt:
		nextcharacter = text[endpt]
		if re.match("[a-z0-9-.]", nextcharacter):
			return None

		posttld = re.match(':?[0-9]*[/[!#$&-;=?a-z]+]?', text[endpt:])
	pretld = re.search('[a-z0-9-.]+?$', text[:startpt])

	if pretld:
		url = pretld.group(0)
		startpt -= len(pretld.group(0))
	url += tld
	if posttld:
		url += posttld.group(0)		
		endpt += len(posttld.group(0))

	
	url = url.rstrip(",.") 

	return (startpt, endpt), url

def parseText(text):
	results = []
	tlds = (tldextract.TLDExtract()._get_tld_extractor().tlds)
	tldindex = esm.Index()
	for tld in tlds:
		tldindex.enter("." + tld.encode("idna"))
	tldindex.fix()
	tldsfound = tldindex.query(text)
	results = [extractUrl(text, tld) for tld in tldsfound]
	results = [x for x in results if x] # remove nulls
	return results


   

