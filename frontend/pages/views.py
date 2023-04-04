from django.views.generic import TemplateView
import requests


class HomePageView(TemplateView):
    template_name = "pages/home.html"


class AboutPageView(TemplateView):
    template_name = "pages/about.html"


class FormPageView(TemplateView):
    template_name = "pages/form.html"
   
     
class CityPageView(TemplateView):
    template_name = "pages/result.html"

    def post(self, request):
        user_input_region = request.POST.get('region_name')
        user_input_city = request.POST.get('city_name')      # USER INPUT CAUGHT HERE 
        user_input_state = request.POST.get('state_name')      # USER INPUT CAUGHT HERE 
        user_input_country = request.POST.get('country_name')      # USER INPUT CAUGHT HERE 

        url = "http://127.0.0.1:8001/api/my_api"
        params = {
            "region": user_input_region,
            "city": user_input_city,
        }
        response = requests.get(url, params=params)
        print(response.status_code)
        if response.status_code == 200:
            print(response.json())

        context = {'results': response.json()['result'].split('\n'),'region': '{}'.format(user_input_region),'city': '{}'.format(user_input_city), 'state': '{}'.format(user_input_state), 'country': '{}'.format(user_input_country)}
        return self.render_to_response(context=context)