'''
Obtaining an GeoJSON isochrone with the TravelTime API

Segro team, S2DS August 2020 - Aug. 23, 2020
Contact: M. Fortin, L. Burmistrov
REQUIREMENT: One needs an API ID and key: see https://docs.traveltime.com/api/overview/getting-keys
              You then get Your_ID and Your_Key which are used in the headers dictionary
Based on https://traveltime.com/blog/time-map-endpoint-tutorial and https://traveltime.com/blog/how-to-create-a-geojson-isochrone
'''

import requests
import json
import geojson
from vincenty import vincenty
import os.path

def farthest_point(filename):
    '''returns the distance and location of the farthest away place from the departure point  *as the crow flies* using https://pypi.org/project/vincenty/0.1.4/
    Input: filename from which it extracts the coordinates of the departure point
    Output: distance (in km) and location (latitude, longitude) of the farthest away point
    Disclaimer: can certainly be improved as brute force is used to obtain the farthest point'''
    latitude,longitude = [float(x) for x in filename.split('_')[1:3] if x] # extract the coordinates of the departure point from the filename
    departure = (latitude, longitude) # definition of the departure point
    distance_max=0;contour_dmax=0;index_dmax=0 # initialization of the data: maximum distance distance_max, contour_dmax the contour where distance_max is found and index_dmax the index where it is found in the data file
    data = geojson.load(open(filename+'.geojson')) # loading the data file
    for contour_number in range(len(data[0]["geometry"]["coordinates"][:])):
        for index in range(len(data[0]["geometry"]["coordinates"][contour_number][0])):
            longitude_arr,latitude_arr=data[0]["geometry"]["coordinates"][contour_number][0][index]
            arrival=(latitude_arr,longitude_arr)
            if (vincenty(departure, arrival)>distance_max): # distance computed with Vincenty's formula
                distance_max=vincenty(departure, arrival)
                index_dmax=index
                contour_dmax=contour_number
                
    return distance_max,data[0]["geometry"]["coordinates"][contour_dmax][0][index_dmax][1],data[0]["geometry"]["coordinates"][contour_dmax][0][index_dmax][0]


def external_contour_coordinates(dataDict={},filename=''):
    ''' Obtains the maximum and minium latitude and longitude of the catchment area. From this we can construct a tetragon with the vertices (max_lat,max_lon), (max_lat,min_lon), (min_lat,max_lon), (min_lat,min_lon)
    Input: the filename, used to then open and read the file
    Output: minimum latitude, maximum latitude, minimum longitude, maximum longitude
    '''
    max_lat=-180;max_lon=-180;min_lat=+180;min_lon=+180 #initiates the values of the max and min of the latitude and longitude
    if(len(filename) != 0):
        #data = geojson.load(open(filename+'.geojson')) # reads the file
        data = geojson.load(open(filename)) # reads the file
        for contour_number in range(len(data[0]["geometry"]["coordinates"][:])):
            # for a given contour of index contour_number find the max/min the lat/long and compares it to the current values max_lat, min_lat, ... and update these latter values if need be
            if (max_lat<=max(coor[1] for coor in data[0]["geometry"]["coordinates"][contour_number][0][:] )): max_lat=max(coor[1] for coor in data[0]["geometry"]["coordinates"][contour_number][0][:] )
            if (max_lon<=max(coor[0] for coor in data[0]["geometry"]["coordinates"][contour_number][0][:] )): max_lon=max(coor[0] for coor in data[0]["geometry"]["coordinates"][contour_number][0][:] )
            if (min_lat>=min(coor[1] for coor in data[0]["geometry"]["coordinates"][contour_number][0][:] )): min_lat=min(coor[1] for coor in data[0]["geometry"]["coordinates"][contour_number][0][:] )
            if (min_lon>=min(coor[0] for coor in data[0]["geometry"]["coordinates"][contour_number][0][:] )): min_lon=min(coor[0] for coor in data[0]["geometry"]["coordinates"][contour_number][0][:] )

    else:
        data=dataDict
        for contour_number in range(len(data['features'][0]["geometry"]["coordinates"][:])):
            # for a given contour of index contour_number find the max/min the lat/long and compares it to the current values max_lat, min_lat, ... and update these latter values if need be
            if (max_lat<=max(coor[1] for coor in data['features'][0]["geometry"]["coordinates"][contour_number][0][:] )): max_lat=max(coor[1] for coor in data['features'][0]["geometry"]["coordinates"][contour_number][0][:] )
            if (max_lon<=max(coor[0] for coor in data['features'][0]["geometry"]["coordinates"][contour_number][0][:] )): max_lon=max(coor[0] for coor in data['features'][0]["geometry"]["coordinates"][contour_number][0][:] )
            if (min_lat>=min(coor[1] for coor in data['features'][0]["geometry"]["coordinates"][contour_number][0][:] )): min_lat=min(coor[1] for coor in data['features'][0]["geometry"]["coordinates"][contour_number][0][:] )
            if (min_lon>=min(coor[0] for coor in data['features'][0]["geometry"]["coordinates"][contour_number][0][:] )): min_lon=min(coor[0] for coor in data['features'][0]["geometry"]["coordinates"][contour_number][0][:] )
        
    return min_lat,max_lat,min_lon,max_lon



def remap_linear_ring(linear_ring):
    ''' Additional routines adapted from https://traveltime.com/blog/how-to-create-a-geojson-isochrone '''
    return list(map(lambda c: [c['lng'], c['lat']], linear_ring))


def shapes_to_multipolygon(shapes):
    ''' Additional routines adapted from https://traveltime.com/blog/how-to-create-a-geojson-isochrone '''
    allRings = []
    for shape in shapes:
        shell = remap_linear_ring(shape["shell"])
        holes = list(map(lambda h:remap_linear_ring(h), shape["holes"]))
        rings = [shell]
        rings.extend(holes)
        allRings.append(rings)

    return {
        "type": "MultiPolygon",
        "coordinates": allRings
    }


def json_to_geojson(response):
    ''' Additional routines adapted from https://traveltime.com/blog/how-to-create-a-geojson-isochrone '''
    response_data = response.json()
    multi_polygons = list(map(lambda r: shapes_to_multipolygon(r["shapes"]), response_data["results"]))
    features = list(map(lambda mp: {'geometry': mp, 'type': 'Feature', 'properties': {}}, multi_polygons ))

    return {
        "type": "FeatureCollection",
        "features": features
    }

def API_request(travel_time_in_minutes=60,
                transportation_mean="driving",
                latitude=51.510078,
                longitude=-0.134952,
                start_time="2020-02-03T09:00:00Z",
                request_id="This is a test",
                returnGeoDataFrame=False):
    ''' 
    Calling the TravelTime API route
    Input: 
     - a departure request named request_id: places which are reachable from an initial location within a given time using a chosen mean of transportation.
     location of the origin: with latitude and longitude (decimal degrees) 
     - starting date and time: start_time (extended ISO-8601 format) 
     - mean of transportation: transportation_mean (string) cf API documentation: https://docs.traveltime.com/api/reference/time-map#departure_searches-transportation-type
     - travel time: travel_time_in_minutes in minutes.
    Output: 2 files (json and geojson) with the same name containing the catchment areas, that is the areas you can reach before start_time+travel_time_in_minutes
    '''
    # Input for the API
    print("!!!! WARNING: the travel time you entered is taken as being in **MINUTES**")
    payload_dict={"departure_searches":[{"id":request_id,"coords":{"lat": latitude,"lng": longitude},"transportation":{"type": transportation_mean},"departure_time":start_time,"travel_time":int(travel_time_in_minutes*60)}]}
    payload=json.dumps(payload_dict)

    ttp_creds = json.load(open('../ttp_creds.json'))

    headers = {
        'Host': 'api.traveltimeapp.com',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Application-Id': ttp_creds["application_id"],
        'X-Api-Key': ttp_creds["application_key"]
    }
    url = "http://api.traveltimeapp.com/v4/time-map"

    filename="Request_"+str(latitude)+"_"+str(longitude)+"_"+transportation_mean+"_"+start_time.replace(":","-")+"_"+str(travel_time_in_minutes)+"min"
    geo_data_dir='./data_ttapi/'
    if(returnGeoDataFrame == False):
        # Sending a request to the API 
        geo_data_file_name = geo_data_dir+filename+".geojson"
        data_file_name = geo_data_dir+filename+".json"
        if os.path.isfile(geo_data_file_name)==False: # check if the file does not exist already. If so skip the API request
            response = requests.request("POST", url, headers=headers, data = payload)
            if response.status_code != 200: # This means something went wrong.
                print('GET /tasks/ {}'.format(response.status_code))
                print("{}: {}".format(response.json()['description'],response.json()['additional_info']))
                exit()
            # Printing the request from the API to a JSON file 
            with open(data_file_name, 'w') as f:
                json.dump(response.json(), f)
                f.close()
            # Converting the request to GeoJSON and print it in a file
            geo_data=json_to_geojson(response)
            with open(geo_data_file_name, 'w') as f:
                json.dump(geo_data, f)
                f.close()
            return geo_data_file_name, data_file_name, external_contour_coordinates(dataDict=geo_data,filename='')
        else:
            print(filename+' already exists!')
            return geo_data_file_name, data_file_name, external_contour_coordinates(dataDict={},filename=geo_data_file_name)
    else:
        response = requests.request("POST", url, headers=headers, data = payload)
        if response.status_code != 200: # This means something went wrong.
            print('GET /tasks/ {}'.format(response.status_code))
            print("{}: {}".format(response.json()['description'],response.json()['additional_info']))
            exit()
        geo_data = json_to_geojson(response)
        return geo_data, external_contour_coordinates(dataDict=geo_data,filename='')




def travel_between_locations(transportation_mean="driving",
                             start_time="2020-08-10T09:00:00Z",
                             location_list=[
                                 {"id": "London center","coords": {"lat": 51.508930,"lng": -0.131387}},
                                 {"id": "Hyde Park","coords": {"lat": 51.508824,"lng": -0.167093}}
                                 ]):
    ''' 
    Calling the TravelTime API route:         https://docs.traveltime.com/api/reference/routes
    Input: 
    - mean of transportation: transportation_mean (string) cf API documentation: https://docs.traveltime.com/api/reference/time-map#departure_searches-transportation-type
    - starting date and time: start_time (extended ISO-8601 format) 
    - a location list containing the departure and arrival points. For now we only use a unique destination. Formatting:
    location_list=[departure_dict,arrival_dict] with 
    departure_dict={"id": departure_name,"coords": {"lat": latitude_departure,"lng": longitude_departure}} and 
    arrival_dict={"id": arrival_name,"coords": {"lat": latitude_arrival,"lng": longitude_arrival}}
    with the latitude and longitude of the departure and arrival points in decimal degrees
    Output: 
    - travel time: travel_time_in_minutes in minutes.
    - distance between the departure and arrival: distance_in_km in kilometers.
    '''
    
    request_id="This is a request"
    if(len(location_list))==2: # in principle we can put 2 destinations. For simplicity for now we will use only one
        payload_dict={"locations": [location_list[i] for i in range(len(location_list))],"departure_searches": [{"id": request_id,"departure_location_id": location_list[0]["id"],"arrival_location_ids":[location_list[i]["id"] for i in range(1,len(location_list))],"transportation": {"type": transportation_mean},"departure_time": start_time,"properties": ["travel_time", "distance"]}]}
        payload=json.dumps(payload_dict)
        ttp_creds = json.load(open('../ttp_creds.json'))

        headers = {'Host': 'api.traveltimeapp.com','Content-Type': 'application/json','Accept': 'application/json','X-Application-Id':ttp_creds["application_id"],'X-Api-Key': ttp_creds["application_key"]}
        url = "http://api.traveltimeapp.com/v4/routes"

        #Sending a request to the API 
        response = requests.request("POST", url, headers=headers, data = payload)
        if response.status_code != 200: # This means something went wrong.
            print('GET /tasks/ {}'.format(response.status_code))
            print("{}: {}".format(response.json()['description'],response.json()['additional_info']))
            exit()
        else:
            output=response.json()
            travel_time_in_minutes=output['results'][0]['locations'][0]['properties'][0]['travel_time']/60
            distance_in_km=output['results'][0]['locations'][0]['properties'][0]['distance']/1e3
            return travel_time_in_minutes,distance_in_km

    elif(len(location_list))>=3:#4: # in principle we can put 2 destinations. For simplicity for now we will use only one.
        print("Error: too many input locations")
        exit()
    else:
        print("Error: not few input locations")
        exit()


def API_request_2(departure_list=
                  [{'coords': {'lat': 51.664115, 'lng': -0.029189},
                    'departure_time': '2019-11-11T09:00:00Z',
                    'id': 'Enfield',
                    'transportation': {'type': 'driving'},
                    'travel_time': 2700.0}],
                  intersection_list=[],
                  union_list=[],
                  filename="Request",
                  returnGeoDataFrame=False):
    ''' 
    Calling the TravelTime API route
    Input: 
     - a departure_list containing the locations for which one wants to obtain the catchment areas. Formatting:
       departure_list=
       [{"id":request_id_1,"coords":{"lat": latitude_1,"lng": longitude_1},"transportation":
       {"type":transportation_mean_1},"departure_time":start_time_1,"travel_time":travel_time_in_minutes_1*60},
       {"id":request_id_2,"coords":{"lat": latitude_2,"lng": longitude_2},"transportation":
       {"type":transportation_mean_2},"departure_time":start_time_2,"travel_time":travel_time_in_minutes_2*60}, 
       ...] with 
       - request_id_i the name of the i-th request (with i between 1 and 10)
       - latitude_i and longitude_i the latitude and longitude of the departure points in decimal degrees
       - transportation_mean_i the mean of transportation
       - starting date and time: start_time_i (extended ISO-8601 format) 
       - travel_time_in_minutes_i the travel time in minutes.
     - an intersection_list containing the request ids of the catchment areas for which intersections will be calculated. Formatting:
        intersection_list=[
        {"id":request_id_1+"+"+request_id_2 , "search_ids": [request_id_1,request_id_2]},
        {"id":request_id_1+"+"+request_id_3 , "search_ids": [request_id_1,request_id_3]},
        ...] with 
       -  "id": the id that is given to the intersection calculation
       -  "search_ids": the list of the request ids for which the intersection will be calculated.
       Warning: the number of calculated intersections ranges from 0 to 10 and an intersection can only be calculated for requests that are listed in the departure_list.
     - a union_list containing the request ids of the catchment areas for which union will be calculated. Formatting:
        union_list=[
        {"id":request_id_1+"+"+request_id_2 , "search_ids": [request_id_1,request_id_2]},
        {"id":request_id_1+"+"+request_id_3 , "search_ids": [request_id_1,request_id_3]},
        ...] with 
       -  "id": the id that is given to the union calculation
       -  "search_ids": the list of the request ids for which the union will be calculated.
       Warning: the number of calculated unions ranges from 0 to 10 and an union can only be calculated for requests that are listed in the departure_list.
    Output:      
    - 2 files (json and geojson) containing the catchments areas, unions and intersections. The order of these various areas in the output list can be obtained from the json file: print([json_file_content['results'][index]['search_id'] for index in range(len(json_file_content["results"]))])   
    '''

    #Rename the request_id as a series of increasing numbers. This ensures that the ouput is in the same order as the input
    for index in range(len(departure_list)):
        id_departure=str(index)
        departure_list[index]["id"] = id_departure

    ### For now we disable requests for intersections and unions
    print("For now we disable the request for intersections and unions")
    #payload_dict={"departure_searches":departure_list,"intersections": intersection_list,"unions": union_list}
    payload_dict={"departure_searches":departure_list,"intersections":[],"unions":[]}
    
    payload=json.dumps(payload_dict)
    ttp_creds = json.load(open('../ttp_creds.json'))

    headers = {
        'Host': 'api.traveltimeapp.com',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Application-Id': ttp_creds["application_id"],
        'X-Api-Key': ttp_creds["application_key"]
    }
    url = "http://api.traveltimeapp.com/v4/time-map"

    geo_data_dir='./data_ttapi/'
    if(returnGeoDataFrame == False):
        # Sending a request to the API 
        geo_data_file_name = geo_data_dir+filename+".geojson"
        data_file_name = geo_data_dir+filename+".json"
        if os.path.isfile(geo_data_file_name)==False: # check if the file does not exist already. If so skip the API request
            response = requests.request("POST", url, headers=headers, data = payload)
            if response.status_code != 200: # This means something went wrong.
                print('GET /tasks/ {}'.format(response.status_code))
                print("{}: {}".format(response.json()['description'],response.json()['additional_info']))
                exit()
                
            # Printing the request from the API to a JSON file 
            with open(data_file_name, 'w') as f:
                json.dump(response.json(), f)
                f.close()
            # Converting the request to GeoJSON and print it in a file
            geo_data=json_to_geojson(response)
            with open(geo_data_file_name, 'w') as f:
                json.dump(geo_data, f)
                f.close()
            return geo_data_file_name, data_file_name, external_contour_coordinates(dataDict=geo_data,filename='')
        else:
            print(filename+' already exists!')
            return geo_data_file_name, data_file_name, external_contour_coordinates(dataDict={},filename=geo_data_file_name)
    else:
        response = requests.request("POST", url, headers=headers, data = payload)
        if response.status_code != 200: # This means something went wrong.
            print('GET /tasks/ {}'.format(response.status_code))
            print("{}: {}".format(response.json()['description'],response.json()['additional_info']))
            exit()
        geo_data = json_to_geojson(response)
        return geo_data, external_contour_coordinates(dataDict=geo_data,filename='')


def main():
    returnGeoDataFrame=True
    if(returnGeoDataFrame == True):
        geo_dict, maxminlist = API_request(returnGeoDataFrame=returnGeoDataFrame)
        print(type(geo_dict))
        print(type(maxminlist))
        print(maxminlist)
        geo_dict, maxminlist = API_request_2(returnGeoDataFrame=returnGeoDataFrame)
        print(type(geo_dict))
        print(type(maxminlist))
        print(maxminlist)
        
    returnGeoDataFrame=False
    if(returnGeoDataFrame == False):
        geo_data_file_name, data_file_name, maxminlist = API_request(returnGeoDataFrame=returnGeoDataFrame)
        print(type(maxminlist))
        print(geo_data_file_name)
        print(data_file_name)
        print(maxminlist)
        print(geo_data_file_name)
        geo_data_file_name, data_file_name, maxminlist = API_request_2(returnGeoDataFrame=returnGeoDataFrame)
        print(type(maxminlist))
        print(geo_data_file_name)
        print(data_file_name)
        print(maxminlist)
        print(geo_data_file_name)
    
    time,distance=travel_between_locations()
    print("Time={} minute(s), distance={} km".format(time,distance))

    
if __name__ == "__main__":
    main()



