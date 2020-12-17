from flask import Flask, render_template, request

import fitbit
import gather_keys_oauth2 as Oauth2
import jinja2
import os

app = Flask(__name__)

CLIENT_ID = '22BY8R'
CLIENT_SECRET = '641ae9179acffcc3f752fdc0b766ad3f'

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                       extensions=['jinja2.ext.autoescape'],
                                       autoescape=True)

server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN,
                             refresh_token=REFRESH_TOKEN)


@app.route("/", methods=['GET', 'POST'])
def main_handler():
    if request.method == 'POST':
        startdate = request.form.get('trip-start')
        name = request.form.get('username')
        if name:
            print("test")
            oneDayData = auth2_client.intraday_time_series('activities/calories', startdate, detail_level='15min')
            calorie = oneDayData['activities-calories'][0]['value']
            calorieTrim = calorie.replace('"', '')
            if calorieTrim >= "3000":
                photourl = "https://imagesvc.meredithcorp.io/v3/mm/image?url=https%3A%2F%2Fstatic.onecms.io%2Fwp-content%2Fuploads%2Fsites%2F19%2F2020%2F10%2F12%2Fmy_resipes_seo_19_holiday_buffalochickenlasagna_5108-2000.jpg"
                recipeName = "Buffalo Chicken Lasagna"
                recipeURL = "https://www.myrecipes.com/recipe/buffalo-chicken-lasagna"
            elif "2500" < calorieTrim < "3000":
                photourl = "https://imagesvc.meredithcorp.io/v3/mm/image?url=https%3A%2F%2Fstatic.onecms.io%2Fwp-content%2Fuploads%2Fsites%2F19%2F2018%2F05%2F21%2Fchicken-fried-rice-burrito-dcms-large-image-2000.jpg"
                recipeName = "Fried Rice Burrito"
                recipeURL = "https://www.myrecipes.com/recipe/fried-rice-burrito"
            elif "2000" < calorieTrim < "2500":
                photourl = "https://imagesvc.meredithcorp.io/v3/mm/image?url=https%3A%2F%2Fstatic.onecms.io%2Fwp-content%2Fuploads%2Fsites%2F19%2F2019%2F03%2F04%2Fcrispy-salmon-salad-with-roasted-butternut-squash-1811-p28-2000.jpg"
                recipeName = "Crispy Salmon Salad With Roasted Butternut Squash"
                recipeURL = "https://www.myrecipes.com/recipe/crispy-salmon-salad-with-roasted-butternut-squash"
            elif "1500" < calorieTrim < "2000":
                photourl = "https://imagesvc.meredithcorp.io/v3/mm/image?url=https%3A%2F%2Fstatic.onecms.io%2Fwp-content%2Fuploads%2Fsites%2F19%2F2020%2F10%2F06%2F2020_018_My_Recipes_09292053_PSD202816-bit29-2000.jpg"
                recipeName = "Vegetarian White Bean Chili"
                recipeURL = "https://www.myrecipes.com/recipe/vegetarian-white-bean-chili"
            else:
                photourl = "https://imagesvc.meredithcorp.io/v3/mm/image?url=https%3A%2F%2Fstatic.onecms.io%2Fwp-content%2Fuploads%2Fsites%2F19%2F2019%2F07%2F23%2FOnePotSausageandFallVegetableGnocchi_66.jpg"
                recipeName = "Savory Sausage, Veggie, and Gnocchi Soup"
                recipeURL = "https://www.myrecipes.com/recipe/savory-sausage-veggie-gnocchi-soup"
            return render_template('data.html',
                                   name=name,
                                   startdate=startdate,
                                   calorieTrim=calorieTrim,
                                   photourl= photourl,
                                   recipeName= recipeName,
                                   recipeURL=recipeURL)
        else:
            return render_template('form.html',
                                   page_title="Information Form - Error")
    else:
        return render_template('form.html', page_title="Information Form")


if __name__ == "__main__":
    app.run(host='localhost', port=5000)
