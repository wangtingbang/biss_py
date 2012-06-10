'''
Created on 2012-5-26

@author: sigh.differ
'''
base_url_pro = 'www.ncbi.com/protein/'

def clone_url_generator( file ):
    return

def nuc_url_generator( file ):
    return

def protein_url_generator(file):
    urls = []
    kw = ''
    try:
        f = open( file )
    except IOError, e:
        print 'IOError: error occurred in open file ' + file + ' in url_generator.protein_url_generator()'
        print e
    olines = f.readlines()
    for eachline in olines:
        try:
            kw = eachline
            print kw + '\n'
        except IOError, e:
            print 'IOError: error occurred in reading file ' + file + ' in url_generator.protein_url_generator()'
            print e
        if f.errors:
            # Maybe file read out
            print kw + '## file read out\n'
            break
        url = base_url_pro + kw
        urls.append(url)
        
    return urls

def pubmed_url_generator( file ):
    return