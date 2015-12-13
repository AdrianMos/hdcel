'''
Created on 26.04.2014

@author: Adrian Raul Mos
'''
import os.path
import sys
#add the current folder to the python paths
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from article import Article
#from haiducel.articles import Articles
from articles import *
#from haiducel.articles import HaiducelArticles
from export import Export
from operations import Operations
from pathbuilder import PathBuilder
import time




def main():
    print("*******************************************")
    print("*** Actualizare date magazinul Haiducel ***")
    print("*******************************************")
    print("Adrian Mos, V 2.7, 11.10.2015\n")
    
    
    try:
        
        while True:
            print("1. Iesire\n"
                  "2. Actualizare Nancy (NAN)\n"
                  "3. Actualizare BabyDreams (HDRE)\n" 
                  "4. Actualizare Bebex (BEB)\n"
                  "5. Actualizare BebeBrands (HBBA)\n"
                  "6. Actualizare BabyShops (HMER)\n"
                  "7. Actualizare KidsDecor (HDEC) - nu merge, caractere ilegale in feed, feed-nu se descarca\n"
                  "8. Actualizare Hubners (HHUB)\n"
                  )
            userInput = input('>> ')
            
            if userInput=="1":
                sys.exit("Program terminat.")
                break
            elif userInput=="2":
                #supplierPaths = PathBuilder("NAN")
                supplierFeed = NANArticles("NAN")    
                #supplierCode = "NAN"   
                break
            elif userInput=="3":
                #supplierPaths = PathBuilder("HDRE")
                supplierFeed = HDREArticles("HDRE")
                #supplierCode = "HDRE"
                break
            elif userInput=="4":
                supplierFeed = BEBArticles("BEB")
                break
            elif userInput=="5":
                supplierFeed = BebeBrandsArticles("HBBA")
                break
            elif userInput=="6":
                supplierFeed = BabyShopsArticles("HMER")
                break
            elif userInput=="7":
                supplierFeed = KidsDecorArticles("HDEC")
                break
            elif userInput=="8":
                supplierFeed = HubnersArticles("HHUB")
                break
            else:
                sys.exit("Comanda invalida. Program terminat.")
        
                
        print("\n*** Articole de tipul " + supplierFeed.__class__.__name__ + " ***")
        
        
        userInput=""
        while (userInput!="y" and userInput!="n"):
            userInput = input('Descarc feed nou? y/n:\n>> ').lower()
            if userInput=="y":
                supplierFeed.DownloadFeed()
        
        
        print("\n*** Import date din feed " + supplierFeed.code)
        supplierFeed.Import()
        supplierFeed.Convert()
        print("    Articole importate: "+ str(supplierFeed.articleList.__len__()))
        
        supplierFeed.RemoveCrapArticles()
        print("    Articole importate, dupa eliminare: "+ str(supplierFeed.articleList.__len__()))
        
        print("\n*** Import articole din baza de date Haiducel, distribuitor " + supplierFeed.code)
        haiducelArticles = HaiducelArticles("Haiducel")
        haiducelArticles.Import()
        haiducelArticlesFiltered = haiducelArticles.FilterBySupplier(supplierFeed.code)
        print("    Articole importate: "+ str(haiducelArticlesFiltered.articleList.__len__()))
        
        
    
        print("\n************ COMPARARI ************")
        
        print("\n*** Articole existente")
        updatedArticles, updateMessages = Operations.ExtractUpdatedArticles(haiducelArticlesFiltered, supplierFeed)
        # Set the saving paths & code for the updated articles identical to the supplier's paths
        # The updated articles belong to the supplier.
        updatedArticles.paths = supplierFeed.paths    
        print("    Articole actualizate: "+ str(updateMessages.__len__())) 
        export1 = Export()
        filenameArticlesToUpdate = supplierFeed.code + "/out/" + supplierFeed.code + ' articole existente cu modificari in pret sau status ' + time.strftime("%Y-%m-%d") + '.csv'
        export1.ExportPriceAndAvailabilityAndMessages(updatedArticles, updateMessages, filenameArticlesToUpdate)
        
        print("\n*** Articole noi active")
        articlesNew = Operations.SubstractArticles(supplierFeed, haiducelArticlesFiltered)
        articlesNew = Operations.RemoveUnavailableArticles(articlesNew)
        articlesNew.paths = supplierFeed.paths
        filenameArticlesNew = supplierFeed.code + "/out/" + supplierFeed.code + ' articole noi ' + time.strftime("%Y-%m-%d") + '.csv'
        print("    Articole noi in feed: " + str(articlesNew.articleList.__len__()))
        #export1.ExportPriceAndAvailability(articlesNew, filenameArticlesNew)
        export1.ExportAllData(articlesNew, filenameArticlesNew)
        
        print("\n*** Articole sterse din feed")
        articlesRemoved = Operations.SubstractArticles(haiducelArticlesFiltered, supplierFeed)
        filenameArticlesToRemove = supplierFeed.code + "/out/" + supplierFeed.code + ' articole de sters ' + time.strftime("%Y-%m-%d") + '.csv'
        print("    Articole ce nu mai exista in feed: " + str(articlesRemoved.articleList.__len__()))
        export1.ExportArticlesForDeletion (articlesRemoved, filenameArticlesToRemove)
        
        userInput = input('\nDescarc imaginile pentru articolele noi? y/n:\n>> ')
        if userInput.lower()=="y":
            articlesNew.DownloadImages();
            
    except Exception as ex:
        print("\n\n Eroare: " + repr(ex) + "\n")
      
   
    userInput = input('\nApasati enter pentru iesire.\n>> ')
    print("\n*** Program terminat ***")
    
    
    
    #for art in articlesNewNAN.articleList:
    #    print(art.id, art.title)
        
    #for art in updatedArticles.articleList:
    #print(art)
    #for art in articlesRemovedNAN.articleList:
    #    print(art.id, art.title)
    
    #for art in updatedArticles.articleList:
     #   print (art.imagesNew)
    '''
    
    for art in existingArticlesNAN.articleList:
        try:
            print("Supplier: *" + art.supplier +  "*")
        except:
            print("!!! Cannot display data for: " + art.id)
    ''' 
    
    #csv.SaveNewArticles(newFeed, existingData, saveTitle=True, saveImages=True, saveDistribuitor=True)
    
    #compareArticles 
    #  -> new articles - full description
    #  -> updated articles - only updated fields
    
    
    
    
    '''
    articles = BabyDreamsArticles()
    
    articles.Import()
    articles.CheckForDuplicity()
    articles.ComputePrices()
    articles.ComputeAvailability()
    articles.ComputeCategory()
                   --> read mappings from file
                   
    articles.ComputeDescription()
    articles.ComputeImagePaths()
    
    articles.SaveNewArticles()
    articles.SaveUpdatedArticles()
    '''
    
    
    
    
    '''
    articlesDummy1 = Articles()
    articlesDummy1.Add("5", "item2  ", 15, "Inactive", "category1", "NAN")
    articlesDummy1.Add("2", "item1", 10, "Active", "category1", "NAN")
    articlesDummy1.Add("3", "item2", 10, "Active", "category1", "NAN")
    
    articlesDummy2 = Articles()
    articlesDummy2.Add("2", "item1", 10, "Inactive", "category1", "NAN")
    articlesDummy2.Add("5", "item2", 10, "Active", "category1", "NAN")
    articlesDummy2.Add("3", "item2", 20, "Active", "category1", "NAN")
    '''



if __name__ == '__main__':
    main()
