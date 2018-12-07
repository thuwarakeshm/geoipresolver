from django.shortcuts import render
from django.contrib.gis.geoip2 import GeoIP2

g = GeoIP2()
asian_countries = ["RW", "SO", "YE", "IQ", "SA", "IR", "TZ", "SY", "AM", "KE", "CD", "DJ", "UG", "CF", "SC", "JO", "LB", "KW", "OM", "QA", "BH", "AE", "IL", "TR", "ET", "ER", "EG", "SD", "BI", "AZ", "GE", "ZW", "ZM", "KM", "MW", "LS", "BW", "MU", "SZ", "RE", "ZA", "YT", "MZ", "MG", "AF", "PK", "BD", "TM", "TJ", "LK", "BT", "IN", "MV", "IO", "NP", "MM", "UZ", "KZ", "KG", "CC", "VN", "TH", "ID", "LA", "TW", "PH", "MY", "CN", "HK", "BN", "MO", "KH", "KR", "JP", "KP", "SG", "MN", "CX", "LY", "CM", "SN", "CG", "LR", "CI", "GH", "GQ", "NG", "BF", "TG", "GW", "MR", "BJ", "GA", "SL", "ST", "GM", "GN", "TD", "NE", "ML", "EH", "TN", "MA", "DZ", "AO", "NA", "SH", "CV", "PS", "SS"]

def getLocal(request):
    try:
        request.session.set_expiry(0)

        if request.session.__contains__('local'):
            local = request.session.__getitem__('local')
            return local
        else:
            remote = request.META['REMOTE_ADDR']
            country = g.country(remote)['country_code']
            # country = g.country('google.com')['country_code']
            if country in asian_countries:
                request.session.__setitem__('local', True)
                return True
            else:
                request.session.__setitem__('local', False)
                return False
    except:
        return False

def switchRemote(request):
    try:
        if 'remote' in request.GET.keys() and request.session.__contains__('local'):
            request.session.__setitem__('local', not request.session.__getitem__('local')) 
    except:
        pass

    
# Create your views here.
def index(request):

    switchRemote(request)

    local = getLocal(request)
    return render(request, 'geogost/index.html', {'local': local})

def link(request):
    local = getLocal(request)
    if local:
        return render(request, 'geogost/local.html', {})
    else:
        return render(request, 'geogost/global.html', {})