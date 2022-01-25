import pandas as pd
from xml.sax.saxutils import escape
from os.path import exists
import sys
import re

print("""
       _                      _             _ _ 
  ___ (_)___  __  ___ __ ___ | |  _ __ ___ | | |
 / _ \| / __| \ \/ / '_ ` _ \| | | '__/ _ \| | |
| (_) | \__ \  >  <| | | | | | | | | | (_) | | |
 \___// |___/ /_/\_\_| |_| |_|_| |_|  \___/|_|_|
    |__/                                        

      """)

# get imput file
try:
    input_file = sys.argv[1]
except IndexError:
    input_file = input("Please type input filename with full path and press enter: ")

# get file dir
galley_dir = input("Please type full file path for galleys and press enter: ")


# get output filename
out_file = input('Please type output file name: ')

# set input file
df = pd.read_csv(input_file, sep=',')

# set Record_ID field as int type
df['Record_ID'] = df['Record_ID'].fillna(0).astype('int')

# set initial int for incrementing local ids
article_count = 99999999

def article_counter():
    global article_count
    article_count += 5
    return article_count

def convert_row(row):
    article_counter() #increment count for internal id
    return f"""<article xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" date_submitted="2021-03-30" status="3" submission_progress="0" current_publication_id="{row.Record_ID}" stage="production">
	<id type="internal" advice="ignore">{row.Record_ID}</id>
    {submission_file(row)}
    {publication(row)}
</article>
"""

def authors(row):
    def xml(givenname, familyname):
       return f"""<author primary_contact="true" include_in_browse="true" user_group_ref="Author" seq="3" id="1">
			<givenname>{givenname}</givenname>
			<familyname>{familyname}</familyname>
			<email>visible.language.editor@gmail.com</email>
		</author>"""

    pattern = re.compile('[\w-]+\,\s[\w-]+;?\s?[\w-]*')
    if pd.isnull(row.authors):
        print(f'Authors missing for row: {row}')
        sys.exit()
    elif not pattern.match(row.authors):
        print(f'Check author formatting in {row}')
        sys.exit()
    else: 
        # get row contents and parse into author xml entry
        a = [i.split(',') for i in row.authors.split(';')]
        # iterate over list and create return object with corresponding authors
        authors = ''
        for i in a:
            authors+=xml(i[1], i[0])
        return f"""<authors xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
		            xsi:schemaLocation="http://pkp.sfu.ca native.xsd">
                   {authors}
                   </authors>"""

def submission_file(row):
    if pd.isnull(row.galley):
        return ''
    else:
        return f"""<submission_file xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" stage="proof" id="{article_count}" xsi:schemaLocation="http://pkp.sfu.ca native.xsd">
        <revision number="1" genre="Article Text" filename="{row.galley}" viewable="false" date_uploaded="2021-03-30" date_modified="2021-03-30" filesize="170067" filetype="application/pdf" uploader="ojsadmin">
          <name locale="en_US">ojsadmin,{row.galley}</name>
          <embed encoding="base64">{file(row, galley_dir)}</embed>
        </revision>
      </submission_file>
    """

def keywords(row):
    if pd.isnull(row.keywords):
        return
    else:
        def xml(keyword):
            return f"""<keyword>{escape(keyword.strip())}</keyword>"""
        # get row contents and parse into keyword xml entry
        keywords = ''
        for i in row.keywords.split(','):
            keywords+=xml(i.strip())
        return f"""<keywords locale="en_US">{keywords}</keywords>"""

def date_published(row):
    return

def last_modified(row):
    return

def publication(row):
    return f"""<publication xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" locale="en_US" version="1" status="3" primary_contact_id="1" url_path="" seq="3" date_published="2021-08-25" section_ref="{row.section}" access_status="0" xsi:schemaLocation="http://pkp.sfu.ca native.xsd">
        <id type="internal" advice="ignore">{row.Record_ID}</id>
    <title locale="en_US">{escape(row.title)}</title>
	<prefix locale="en_US"></prefix>
	<abstract locale="en_US">{escape(row.abstract)}</abstract>
    <copyrightHolder locale="en_US">{row.copyright}</copyrightHolder>
    <copyrightYear>{row.year}</copyrightYear>
    {keywords(row)}
    {authors(row)}
    {article_galley(row)}
    <pages>{row.pages}</pages>
    </publication>
    """

def article_galley(row):
    if pd.isnull(row.galley):
        return ''
    else:
        return f"""<article_galley xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" locale="en_US" approved="false" xsi:schemaLocation="http://pkp.sfu.ca native.xsd">
          <id type="internal" advice="ignore">{row.Record_ID}</id>
          <name locale="en_US">PDF</name>
          <seq>0</seq>
          <submission_file_ref id="{article_count}" revision="1"/>
        </article_galley>
    """

def file(row, galley_dir):
    full_path = f'{galley_dir}/{row.galley}'.format(galley_dir, row.galley)
    if len(row.galley) > 127: 
        print(f'File name too long: {row.galley}; must be shorter than 127 chars')
        sys.exit()
    if exists(full_path):
        return encode(full_path)
    else:
        print(f'File not found: {row.galley}')
        sys.exit()

def encode(valid_full_path):
    import base64
    with open(valid_full_path, "rb") as pdf_file:
        encoded_string = base64.b64encode(pdf_file.read()).decode()
        
    return encoded_string

def issue():
    issue_title = input("Please input issue title and press enter: ")
    volume_number = input("Please input volume number and press enter: ")
    issue_number = input("Please input issue number and press enter: ")
    issue_year = input("Please input issue year and press enter: ")
    return f"""<issue xmlns="http://pkp.sfu.ca" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" published="1" current="1" access_status="1" url_path="" xsi:schemaLocation="http://pkp.sfu.ca native.xsd">
  <id type="internal" advice="ignore">249</id>
  <description locale="en_US"></description>
  <issue_identification>
    <volume>{volume_number}</volume>
    <number>{issue_number}</number>
    <year>{issue_year}</year>
    <title locale="en_US">{issue_title}</title>
  </issue_identification>
  <date_published>2021-09-07</date_published>
  <last_modified>2021-09-07</last_modified>
  {sections()}
"""

def sections():
    return """<!-- SECTIONS BLOCK -->
  <sections>
    <section ref="ART" seq="1" editor_restricted="1" meta_indexed="1" meta_reviewed="0" abstracts_not_required="1" hide_title="0" hide_author="1" abstract_word_count="0">
      <id type="internal" advice="ignore">2</id>
      <abbrev locale="en_US">ART</abbrev>
      <title locale="en_US">Article</title>
    </section>
    <section ref="Book" seq="1" editor_restricted="0" meta_indexed="1" meta_reviewed="1" abstracts_not_required="0" hide_title="0" hide_author="0" abstract_word_count="0">
      <id type="internal" advice="ignore">1</id>
      <abbrev locale="en_US">Book</abbrev>
      <title locale="en_US">Book Review</title>
    </section> <section ref="Edit" seq="1" editor_restricted="0" meta_indexed="1" meta_reviewed="1" abstracts_not_required="0" hide_title="0" hide_author="0" abstract_word_count="0"> <id type="internal" advice="ignore">1</id>
      <abbrev locale="en_US">Edit</abbrev>
      <title locale="en_US">Editorial</title>
    </section>
    <section ref="Gen" seq="1" editor_restricted="1" meta_indexed="1" meta_reviewed="0" abstracts_not_required="1" hide_title="0" hide_author="1" abstract_word_count="0">
      <id type="internal" advice="ignore">2</id>
      <abbrev locale="en_US">Gen</abbrev>
      <title locale="en_US">General Information</title>
    </section>
    <section ref="OA" seq="1" editor_restricted="0" meta_indexed="1" meta_reviewed="1" abstracts_not_required="0" hide_title="0" hide_author="0" abstract_word_count="0">
      <id type="internal" advice="ignore">1</id>
      <abbrev locale="en_US">OA</abbrev>
      <title locale="en_US">Online Article</title>
    </section>
    <section ref="In" seq="1" editor_restricted="0" meta_indexed="1" meta_reviewed="1" abstracts_not_required="0" hide_title="0" hide_author="0" abstract_word_count="0">
      <id type="internal" advice="ignore">1</id>
      <abbrev locale="en_US">In</abbrev>
      <title locale="en_US">Introduction</title>
    </section>
  </sections>
""" 

out = open(out_file, 'w')
out.write(f"""<?xml version="1.0" encoding="UTF-8"?>""")
out.write(issue())
out.write(""" <articles xmlns="http://pkp.sfu.ca" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://pkp.sfu.ca native.xsd">
""")
out.write('\n'.join(df.apply(convert_row, axis=1)))
out.write("</articles></issue>")
out.close()
print(f'\n\nSUCCESS!! Check results @ {out_file}')
