from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
import requests
from django.shortcuts import render
from plotly.offline import plot 
import plotly.express as px
import pandas as pd

data = []

class HomePageView(TemplateView):
    template_name = "pages/home.html"


class AboutPageView(TemplateView):
    template_name = "pages/about.html"


class FormPageView(TemplateView):
    template_name = "pages/form.html"
   
class MyBarChartView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["Authentic", "Non Authentic"]

    def get_providers(self):
        """Return names of datasets."""
        return ["Dataset 1", "Dataset 2"]

    def get_data(self):
        """Return 3 datasets to plot."""
        return data

    def get_options(self):
        """Configure options for the chart."""
        return {
            "title": {"display": True, "text": "My Bar Chart"},
            "scales": {"yAxes": [{"ticks": {"beginAtZero": True}}]},
        }
     
class CityPageView(TemplateView):
    template_name = "pages/result.html"

    def post(self, request):
        user_input_region = request.POST.get('region_name')
        user_input_city = request.POST.get('city_name')      # USER INPUT CAUGHT HERE 
        print(user_input_city)
        print(user_input_region)
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
        

        pie_val = [response.json()['plot1']['high'], response.json()['plot1']['medium'], response.json()['plot1']['low']]
        pie_names = ["High" , "Medium", "Low"]

        bar_val = [response.json()['plot2']['authentic'], response.json()['plot2']['nonauthentic']]
        bar_names = ["Authentic" , "Not Authentic"]

        df = pd.DataFrame({
            'values': pie_val,
            'names':  pie_names
        })

        df_bar = pd.DataFrame({
            'values': bar_val,
            'names':  bar_names
        })

        fig = px.pie(df, values='values', names='names', title='Severity of News')
        gantt_plot = plot(fig, output_type="div")
        
        fig2 = px.bar(df_bar, x='names', y='values', title='Authentic vs Non Authentic News Counts')
        fig2.update_yaxes(autorange="reversed")
        gantt_plot2 = plot(fig2, output_type="div")

        context = {'results': response.json()['result'], 'region': user_input_region,'city': user_input_city, 'plot_div': gantt_plot, 'plot_div2': gantt_plot2}
        return self.render_to_response(context=context)