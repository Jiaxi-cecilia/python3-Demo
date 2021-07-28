import json
import requests

apikey = 'AIzaSyAfsGzE_rLnQntc-O7zuUYsL17bT7QFFEI'
autocomplete_url = 'https://maps.googleapis.com/maps/api/place/autocomplete/json'
geometrics_url = 'https://maps.googleapis.com/maps/api/place/details/json'
nearby_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

'''location of the input address'''
def autocomplete (location):
    params = {"input" : location, "key" : apikey}
    resp = requests.get(url = autocomplete_url, params = params)
    data = resp.json() #check the JSON responses content documentation,convert to an dictionary
    predictions = data["predictions"]
    ##same as data.get(predictions), contains an array of places with information about the place, see Placeautomation output as reference
    list_of_recommendations = []
    #construct a list of dictionary of all places to store all predicted details
    for p in predictions:
        locationdetails = {
        "name" : p.get("description"),
        "place_id" : p.get("place_id")
        }
        list_of_recommendations.append(locationdetails)
    return list_of_recommendations

'''get the place_id from previous function and apply to the next function to return the location details - longitude and latitude of the pplace'''
def geometrics (place_id):
    params = {"place_id" : place_id, "key" : apikey}
    resp = requests.get(url = geometrics_url, params = params)
    data = resp.json() #request/check the JSON responses content documentation,convert to an dictionary
    # need to return location in long/lati
    results = data["result"]
    #since we specify the place_is, so only the information of one place will be returned
    return results['geometry']['location']

'''requires location: the latitude / longitude around, radius in meters'''
def nearbysearch (latitude,longtitude):
    radius = 1500
    params = {"location":"{},{}". format(latitude,longtitude),"radius" : radius, "type": "restaurant", "key": apikey}
    resp = requests.get(url=nearby_url, params=params)
    data = resp.json()  # request/check the JSON responses content documentation,convert to an dictionary
    results = data.get("results") ##same as data["result"]
    next_token = data.get("next_page_token")

    nearbyoutput = []
    while next_token != "":
        for r in results: # for each object in the list of result which is a dictionary, get the name/types
            placedetails = {
                "name" : r.get("name"),
                "types": r.get("types")
            }
            nearbyoutput.append(placedetails) #construct a list of dictionary containing each restarurant's name and ts
        params = {"pagetoken":next_token,"key": apikey}
        resp = requests.get(url=nearby_url, params=params)
        data = resp.json()  # request/check the JSON responses content documentation,convert to an dictionary
        results = data.get("results")  ##same as data["result"]
        next_token = data.get("next_page_token") if data.get("next_page_token") else ""
    return nearbyoutput

if __name__ == "__main__":
    location = input("Please enter a location: ")
    recommendation = autocomplete(location)
    print(recommendation)
    geo = geometrics(recommendation[0]["place_id"])
    print(geo)
    if geo:
        nearby_restaurant = nearbysearch(geo["lat"],geo["lng"])
        print(nearby_restaurant)
    else:
        print("no result found")



