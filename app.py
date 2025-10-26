from flask import Flask, jsonify, request
import json

AVERAGE_CAR_MPG = 24.9

app = Flask(__name__)

@app.route("/", methods=["GET"])
def requestForData():
    grade = request.args.get("grade", "default")
    brand = request.args.get("brand", "default")
    sortingType = request.args.get("sortingType", "default")

    file = open("Gas Station App/stations.json", "r")
    dictionary = json.load(file)
    file.close()
    
    if grade != "default" :
        dictionary = sortByGrade(dictionary, grade)
    if brand != "default" : 
        dictionary = sortByBrand(dictionary, brand)
    if sortingType != "default" :
        match sortingType :
            case "shortest":
                dictionary = sortByShortest(dictionary)
            case "cheapest":
                dictionary = sortByCheapest(dictionary)

    return jsonify(dictionary)

def sortByGrade(dictionary, grade) :
    filtered = {}
    for key, info in dictionary.items() :
        if info["prices"][grade] is not None :
            match grade :
                case "regular":
                    del info["prices"]["midgrade"]
                    del info["prices"]["premium"]
                    del info["prices"]["diesel"]
                    del info["prices"]["e85"]
                case "midgrade":
                    del info["prices"]["regular"]
                    del info["prices"]["premium"]
                    del info["prices"]["diesel"]
                    del info["prices"]["e85"]
                case "premium":
                    del info["prices"]["regular"]
                    del info["prices"]["midgrade"]
                    del info["prices"]["diesel"]
                    del info["prices"]["e85"]
                case "diesel":
                    del info["prices"]["regular"]
                    del info["prices"]["midgrade"]
                    del info["prices"]["premium"]
                    del info["prices"]["e85"]
                case "e85":
                    del info["prices"]["regular"]
                    del info["prices"]["midgrade"]
                    del info["prices"]["premium"]
                    del info["prices"]["diesel"]
            
            filtered[key] = info

    return filtered

def sortByBrand(dictionary, brand) :
    filtered = {}
    for key, info in dictionary.items() :
        if info["brand_name"].lower() == brand.lower() :
            filtered[key] = info
    
    return filtered

def sortByShortest(dictionary) :

    pass

def sortByCheapest(dictionary) :
    cheapest = {}
    lowest_price = 100
    
    for key, info in dictionary.items() :
        for value in info["prices"].values() :
            if value < lowest_price :
                lowest_price = value
                cheapest = dictionary[key]
                
    return cheapest

def updateData() :
    #update the .json to have acurate data
    #call the fabricator to replace old data
    pass
