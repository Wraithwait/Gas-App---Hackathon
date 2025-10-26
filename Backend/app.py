from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def requestForData(): 
    grade = request.args.get("grade", "default").lower()
    brand = request.args.get("brand", "default").lower()
    sortingType = request.args.get("sortingType", "default").lower()

    file = open("stations.json", "r")
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

    return jsonify(list(dictionary.values()))

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
        if info["brand_name"].lower() == brand :
            filtered[key] = info
    
    return filtered

def sortByShortest(dictionary) :
    
    pass

def sortByCheapest(dictionary) :
    cheapest = None
    lowestPrice = float("inf")
    
    for key, info in dictionary.items() :
        prices = info["prices"].values()
        minPrice = float("inf")

        for p in prices :
            if p is not None and p < minPrice:
                minPrice = p

        if minPrice < lowestPrice : 
            lowestPrice = minPrice
            cheapest = {key: info}
