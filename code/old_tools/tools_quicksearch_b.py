import pandas as pd

# #############################################################################
# Journal 2
# #############################################################################

# df_j2_c = pd.read_csv  ("a_processed_data/journal_2_urls.csv")
df_j2_c = pd.read_excel("a_processed_data/journal_3_urls.xlsx")

print(len(df_j2_c))

df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('mendeley', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('github', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('bitbucket', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('sourceforge', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('drive.google', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('dropbox.com', case=False, na=False)]

print(len(df_j2_c))

df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('w3.org', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('amazonaws.com', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('prismstandard.org', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('elsevier.com', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('purl.org', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('https://www.sciencedirect.com/', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('www.sciencedirect.com/', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('doi.org', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('credit.niso.org', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('creativecommons.org', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('youtube.com', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('wired.com', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('uber.com', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('jstor.org', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('nature.com', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('sws.geonames.org', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('washintongpost.com', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('theguardian.com', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('theverge.com', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('ieeexplore.org', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('inrix.com', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('journals.sagepub.com', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('keras.io', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('link.springer.com', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('papers.ssrn.com', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('ssrn.com', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('tinyurl.com', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('towardsdatascience.com', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('bloomberg.com', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('businessinsider.com', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('cnn.com', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('dji.com', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('forbes.com', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('web.archive.org', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('r-project.org', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('amazon.com', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('trid.trb.org', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('techcrunch.com', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('pdfs.semanticscholar.org', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('pubsonline.informs.org', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('google.com', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('mdpi.com', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('mckinsey.com', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('nytimes.com', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('openstreetmap.org', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('tandfonline.com/doi', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('gov.uk', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('pytorch.org', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('pypi.org', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('onlinelibrary.wiley.com/doi', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('dictionary.casrai.org', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('http://arxiv.org', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.contains('citeseerx.ist.psu.edu', case=False, na=False)]
df_j2_c = df_j2_c[~df_j2_c['url'].str.lower().str.startswith('10.')]
df_j2_c = df_j2_c[~df_j2_c['url'].str.lower().str.startswith('arxiv:')]
df_j2_c = df_j2_c[~df_j2_c['url'].str.lower().str.startswith('doi:')]
df_j2_c = df_j2_c[~df_j2_c['url'].str.lower().str.startswith('http://null/schema/dtds/')]
df_j2_c = df_j2_c[~df_j2_c['url'].str.lower().str.startswith('http://10.')]


df_j2_c = df_j2_c[df_j2_c['url'] != 'http://']
df_j2_c = df_j2_c[df_j2_c['url'] != 'ANSI/NISO']

df_j2_c = df_j2_c[df_j2_c['url'].str.len() >= 15]

print(len(df_j2_c))
