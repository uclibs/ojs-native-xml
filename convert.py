import pandas as pd

# set input file
df = pd.read_csv('test.csv', sep=',')

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

    if pd.isnull(row.authors):
        return
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
          <href src="/tmp/Files/{row.galley}"></href>
        </revision>
      </submission_file>
    """

def keywords(row):
    if pd.isnull(row.keywords):
        return
    else:
        def xml(keyword):
            return f"""<keyword>{keyword.strip()}</keyword>"""
        # get row contents and parse into keyword xml entry
        keywords = ''
        for i in row.keywords.split(','):
            keywords+=xml(i)
        return f"""<keywords locale="en_US">{keywords}</keywords>"""

def publication(row):
    return f"""<publication xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" locale="en_US" version="1" status="3" primary_contact_id="1" url_path="" seq="3" date_published="2021-08-25" section_ref="{row.section}" access_status="0" xsi:schemaLocation="http://pkp.sfu.ca native.xsd">
        <id type="internal" advice="ignore">{row.Record_ID}</id>
    <title locale="en_US">{row.title}</title>
	<prefix locale="en_US"></prefix>
	<abstract locale="en_US">{row.abstract}</abstract>
    {keywords(row)}
    {authors(row)}
    {article_galley(row)}
    </publication>
    """

def article_galley(row):
    if pd.isnull(row.galley):
        return ''
    else:
        return f"""<article_galley xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" locale="en_US" approved="false" xsi:schemaLocation="http://pkp.sfu.ca native.xsd">
          <id type="internal" advice="ignore">{row.Record_ID}</id>
          <name locale="en_US">{row.galley}</name>
          <seq>0</seq>
          <submission_file_ref id="{article_count}" revision="1"/>
        </article_galley>
    """

out = open('out.xml', 'a')
out.write("""<?xml version="1.0" encoding="UTF-8"?>
<articles xmlns="http://pkp.sfu.ca" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://pkp.sfu.ca native.xsd">
"""
)
out.write('\n'.join(df.apply(convert_row, axis=1)))
out.write("</articles>")
out.close()

