import json, os, requests as r
import pandas as pd
from urllib.parse import quote


# os.system("mkdir sounds")
species = ['Acridotheres fuscus', 'Acrocephalus bistrigiceps', 'Aethopyga gouldiae', 'Alcippe cinerea', 'Arachnothera magna', 'Arborophila torqueola', 'Argya longirostris', 'Centropus andamanensis', 'Chelidorhynx hypoxanthus', 'Chloropsis cochinchinensis', 'Chloropsis hardwickii', 'Chloropsis jerdoni', 'Chrysococcyx maculatus', 'Cuculus micropterus', 'Cyornis concretus', 'Cyornis magnirostris', 'Cyornis poliogenys', 'Cyornis unicolor', 'Cypsiurus balasiensis', 'Dicaeum chrysorrheum', 'Dicaeum cruentatum', 'Dicaeum minullum', 'Dicrurus andamanensis', 'Eurystomus orientalis', 'Glaucidium cuculoides', 'Halcyon coromanda', 'Iole cacharensis', 'Ixobrychus cinnamomeus', 'Lanius tephronotus', 'Liocichla phoenicea', 'Locustella davidi', 'Loriculus vernalis', 'Macronus gularis', 'Motacilla citreola', 'Mystery mystery', 'Paradoxornis guttaticollis', 'Pellorneum ruficeps', 'Phylloscopus forresti', 'Phylloscopus inornatus', 'Phylloscopus subaffinis', 'Pluvialis squatarola', 'Pnoepyga pusilla', 'Polyplectron bicalcaratum', 'Pomatorhinus ruficollis', 'Psilopogon lineatus', 'Psittacula eupatria', 'Rimator malacoptilus', 'Riparia chinensis', 'Spelaeornis oatesi', 'Sphenocichla humei', 'Stachyridopsis ambigua', 'Sturnia malabarica', 'Todiramphus chloris']

sub_species = species[27:40]

for s in sub_species:
    print(s)
    url = f"https://www.xeno-canto.org/api/2/recordings?query={quote(s)}%20cnt:\"%3DIndia\""
    print(url)

    res = r.get(url);
    with open("noca-query.json", 'w') as dataset:
        dataset.write(res.content.decode())

    # Get the json entries from your downloaded json
    jsonFile = open('noca-query.json', 'r')
    values = json.load(jsonFile)
    jsonFile.close()

    # Create a pandas dataframe of records & convert to .csv file
    record_df = pd.DataFrame(values['recordings'])
    record_df.to_csv('xc-noca.csv', index=False)

    # Make wget input file
    url_list = []
    for file in record_df['file'].tolist():
        url_list.append(file)
    with open('xc-noca-urls.txt', 'w+') as f:
        for item in url_list:
            f.write("{}\n".format(item))

    os.system(f"wget -P sounds/\"{s}\" --trust-server-names -i xc-noca-urls.txt")
