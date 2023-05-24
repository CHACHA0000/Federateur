from django.shortcuts import render
from .models import BiensImmobilier
from django.db.models import Q
import requests
from bs4 import BeautifulSoup

# Create your views here.
def index(request):
    biens_immobiliers = BiensImmobilier.objects.order_by('-id').all()
    return render(request, 'index.html', {'biens_immobiliers': biens_immobiliers})

def scrap(request):
    try:
        elemenet = BiensImmobilier.objects.latest('id')
        page = int(elemenet.page)+1
    except:
        page = 1
    # Collecter les données du site 1-	https://www.immobilier.com.tn/
    url1 = 'https://www.immobilier.com.tn/resultat-recherche?ta=2&r=0&tb=&pcs=&smi=&pma=&page='+str(page)
    response1 = requests.get(url1)
    soup1 = BeautifulSoup(response1.content, "html.parser")
    data1 = soup1.find_all('div', class_='col-12 layout-list')

    for item1 in data1:
        localisation = item1.find('div', class_='info').find('small').text.strip() 
        prix = item1.find('div', class_='price price-location').find('span').text.strip()
        url = item1.find('a', class_='annonce-card annonce-square')
        href = url.get('href')
        result = item1.find('ul', class_='amenities').find('li')
        if result is not None:
            pieces = result.text.strip()
        else:
            pieces = "N/A"
        superficie = item1.contents[1].find('ul', class_='amenities').find('li').text.strip()
        description = item1.find('div',class_='description').text.strip()
        type = item1.find('ul', class_='amenities').text.strip()
        site = 'https://www.immobilier.com.tn/'
        url = href
            
        BiensImmobilier.objects.create(site=site, url=url, localisation=localisation, prix=prix, pieces=pieces, superficie=superficie, description=description, type=type, page=page)
    
    biens_immobiliers = BiensImmobilier.objects.order_by('-id').all()
    return render(request, 'index.html', {'biens_immobiliers': biens_immobiliers})

def search(request):
    query = request.POST.get('query')
    biens_immobiliers = BiensImmobilier.objects.filter(Q(site__contains=query)|Q(localisation__contains=query)|Q(prix__contains=query)|Q(pieces__contains=query)|Q(superficie__contains=query)|Q(description__contains=query)|Q(type__contains=query))
    return render(request, 'index.html', {'biens_immobiliers': biens_immobiliers})
