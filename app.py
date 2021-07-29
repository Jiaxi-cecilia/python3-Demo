import requests
import tkinter as tk
from tkinter import filedialog,Text

root = tk.Tk() #attaching everything to the root
root.title("Cecilia's App")

def format_response(nearby_restaurant):
    try:
        one = nearby_restaurant[0]
        name=one["name"]
        description = one["types"]
        final = "Name: %s \nDescription: %s" %(name,description)
    except:
        final ="There is no recommendation around!"
    return final

    # print("The No.1 recommended restaurant: \n")
    # print(one["name"])
    # print("it services as: \n")
    # print(one["types"])


def map(location):
    global nearby_restaurant
    apikey = 'AIzaSyAfsGzE_rLnQntc-O7zuUYsL17bT7QFFEI'
    autocomplete_url = 'https://maps.googleapis.com/maps/api/place/autocomplete/json'
    geometrics_url = 'https://maps.googleapis.com/maps/api/place/details/json'
    nearby_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

    def autocomplete(location):
        params = {"input": location, "key": apikey}
        resp = requests.get(url=autocomplete_url, params=params)
        data = resp.json()
        predictions = data["predictions"]
        list_of_recommendations = []
        for p in predictions:
            locationdetails = {
                "name": p.get("description"),
                "place_id": p.get("place_id")
            }
            list_of_recommendations.append(locationdetails)
        return list_of_recommendations

    def geometrics(place_id):
        params = {"place_id": place_id, "key": apikey}
        resp = requests.get(url=geometrics_url, params=params)
        data = resp.json()
        results = data["result"]
        return results['geometry']['location']

    '''requires location: the latitude / longitude around, radius in meters'''

    def nearbysearch(latitude, longtitude):
        radius = 1500
        params = {"location": "{},{}".format(latitude, longtitude), "radius": radius, "type": "restaurant",
                  "key": apikey}
        resp = requests.get(url=nearby_url, params=params)
        data = resp.json()
        results = data.get("results")
        next_token = data.get("next_page_token")

        nearbyoutput = []
        for r in results:
            placedetails = {
                "name": r.get("name"),
                "types": r.get("types")
                }
            nearbyoutput.append(placedetails)
        return nearbyoutput

    recommendation = autocomplete(location)
    print(recommendation[0])
    geo = geometrics(recommendation[0]["place_id"])
    print(geo)
    if geo:
        nearby_restaurant = nearbysearch(geo["lat"],geo["lng"])

    Label3["text"] = format_response(nearby_restaurant)



canvas = tk.Canvas(root,height = 600, width = 600, bg = "#263D42") #we want to attach thecanvas to root
canvas.pack()

###frame 1
frame = tk.Frame(root,bg = "white")
frame.place(relwidth=0.8,relheight=0.2,relx=0.1,rely=0.1)

Button = tk.Button(frame, text = "Search",font=(None,15),padx=10,pady=5,fg="black",bg="#263D42",command=lambda : map(entry.get()))
Button.place(relx=0.7,rely=0.5,relwidth=0.25,relheight=0.4)

entry = tk.Entry(frame, bg = "#263D42",fg = "white",width = 25,font=(None,15),bd=3)
entry.place(relx=0.1,rely=0.5,relwidth=0.6,relheight=0.4)

Label = tk.Label(frame, text = "Hungry? Find a restaurant nearby!", fg = "#263D42",font=(None,15))
Label.place(relx=0.25,rely=0.2,relwidth=0.5,relheight=0.2)

#frame2
lowerframe = tk.Frame(root, bg="white")
lowerframe.place(relwidth=0.8,relheight=0.625,relx=0.1,rely=0.325)

Label2 = tk.Label(lowerframe, text = "No1. Restaurant around you:", font = (None,20),fg = "#263D42",)
Label2.pack(side="top")

Label3 = tk.Label(lowerframe,  bg = "#263D42",font=(None,15),fg = "white", wraplength=300)
Label3.place(relx=0.1,rely=0.1,relwidth=0.8,relheight=0.8)

root.mainloop()