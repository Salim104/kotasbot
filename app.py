from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient
from datetime import datetime

cluster = MongoClient("mongodb+srv://salimshaban885:salim@aplug0.k281jjd.mongodb.net/?retryWrites=true&w=majority")
db = cluster["shop"]
users = db["users"]
orders = db["orders"]

app = Flask(__name__)


@app.route("/", methods=["get", "post"])
def reply():
    text = request.form.get("Body")
    number = request.form.get("From")

    res = MessagingResponse()
    user = users.find_one({"number": number})
    if bool(user) == False:
        res.message("Hi, thanks for contacting *Musa's Khotas*.\nYou can choose from one of the options below: "
                    "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ For *Kotas*"
                    " Menu \n 3️⃣ For *Burgers* Menu \n 4️⃣ "
                    "To know our *working hours*  \n 5️⃣To get our *address* ")
        users.insert_one({"number": number, "status": "main", "messages": []})


    elif user["status"] == "main":
        try:
            option = int(text)
        except:
            res.message("Please enter a valid response")
            return str(res)
        if option == 1:
            res.message(
                "You can contact us through phone or e-mail.\n\n*Phone*: "
                "0633414546 \n*E-mail* : musakotas@gmail.com")
        elif option == 2:
            res.message("You have now entered *Kota Menu*.")
            users.update_one(
                {"number": number}, {"$set": {"status": "Kota"}})
            res.message("You can select one of the following *Kota Menu* to order from: "
                        "\n\n 1️⃣ *Basic Kota* = R15 \n Chips+Polony+vienna"
                        " \n 2️⃣  *Rise Kota* = R20* \n Chips+Polony+vienna+Special+Cheese"
                        " \n 3️⃣  *Rise plus Kota* = R25* \n Chips+Polony+vienna+Cheese+Egg+Special"
                        " \n 4️⃣  *Bull Kota* = R30* \n Chips+Polony+vienna+Cheese+Egg+Russian"
                        " \n 5️⃣  *Dulax Kota* = R40* \n Chips+Polony+vienna+Cheese+Egg+Russian+Burger"
                        " \n 6️⃣  *Quantum Kota* = R50* \n Chips+Polony+vienna+Cheese+Egg+Russian+Burger+Beacon+lettuce"
                        " \n 7️⃣  *Ibus Kota* = R160* \n Chips+Polony+vienna+Cheese+Egg+Russian+Burger+Beacon+lettuce"
                        " \n 0️⃣ To *Go back* ")

        elif option == 3:
            res.message("The best Burgers in the city(All comes with chips).")
            users.update_one(
                {"number": number}, {"$set": {"status": "burgers"}})
            res.message("You can select one of the following *burger Menu* to order from: "
                        "\n\n 1️⃣ *City burgers* = R25 \n Beef Pattie,lettuce,Tomatoe,Red onion,Cheese,Chips,Cucumber"
                        " \n 2️⃣  *The Mountain Burger* = R35* \n Beef Pattie,lettuce,Tomatoe,Red onion,Cheese,Chips,Chesse,Omlette Egg,Beacon,Chips"
                        " \n 3️⃣  *AmaleVelves Burger* = R45* \n Double Beef Pattie,lettuce,Tomatoe,Red onion, Double Cheese,Cucumber,Omlette,Beacon,Chips,"
                        " \n 4️⃣  *Rock burger* = R50* \n Double Beef Pattie,lettuce,Tomatoe,Red onion,Omlette,Double Cheese,Avocado,Beacon,Egg"
                        " \n 0️⃣ To *Go back* ")

        elif option == 4:
            res.message(
                "We work from *9 a.m. to 7 p.m*.")
        elif option == 5:
            res.message(
                "Our main shop is at *66 Eloff, Johannesburg CBD*")
        else:
            res.message("Please enter a valid response")
            return str(res)

         # ############################################################  Kotas page ####

    elif user["status"] == "Kota":
        try:
            option = int(text)
        except:
            res.message("Please enter a valid response")
            return str(res)
        if option == 0:
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            res.message("Hi, thanks for contacting *Musa's Khotas*.\nYou can choose from one of the options below: "
                        "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ For *Kotas*"
                        " Menu \n 3️⃣ For *Burgers* Menu \n 4️⃣ "
                        "To know our *working hours*  \n 5️⃣To get our *address* ")
        
        elif 1 <= option <= 7:
            kotas = ["Basic Kota", "Rise Kota", "Rise plus Kota", "Bull Kota", "Dulax Kota", "Quantum Kota", "Ibus Kota"]
            kota_description = ["Chips+Polony+vienna","Chips+Polony+vienna+Special+Cheese",
                               "Chips+Polony+vienna+Cheese+Egg+Special","Chips+Polony+vienna+Cheese+Egg+Russian",
                               "Chips+Polony+vienna+Cheese+Egg+Russian+Burger","Chips+Polony+vienna+Cheese+Egg+Russian+Burger+Beacon+lettuce",
                               "Chips+Polony+vienna+Cheese+Egg+Russian+Burger+Beacon+lettuce"]
            price = ["R15", "R20", "R25", "R30", "R40", "R50", "R160"]
            link_price = ["https://pay.ikhokha.com/the-hub-inc/mpr/basickota", "https://pay.ikhokha.com/the-hub-inc/mpr/risekota", "https://www.youtube.com"]

            selected_price = price[option - 1]
            selected = kotas[option - 1]
            selected_desc = kota_description[option - 1]
            link_price = link_price[option - 1]

            users.update_one({"number": number}, {"$set": {"status": "summary"}})
            users.update_one({"number": number}, {"$set": {"item": selected}})
            users.update_one({"number": number}, {"$set": {"selected_desc": selected_desc}})
            users.update_one({"number": number}, {"$set": {"selected_price": selected_price}})
            users.update_one({"number": number}, {"$set": {"link_price": link_price}})

            res.message("Do you want your kota to have one of the following bellow? \n\n Please *Select* one of the options below:"
                        " \n\n 1️⃣ Archer and Chilli"
                        " \n 2️⃣ Archer and No Chilli"
                        " \n 3️⃣ No Archer and Chilli"
                        " \n 4️⃣ No Archer and No Chilli"
                        " \n 0️⃣ Go back"
                        )
    #         ############################################ summary page

    elif user["status"] == "summary":
        try:
            option = int(text)
        except:
            res.message("Please enter a valid response")
            return str(res)
        if option == 0:
            users.update_one(
                {"number": number}, {"$set": {"status": "Kota"}})
            res.message("You can select one of the following *Kota Menu* to order from: "
                        "\n\n 1️⃣ *Basic Kota* = R15 \n Chips+Polony+vienna"
                        " \n 2️⃣  *Rise Kota* = R20* \n Chips+Polony+vienna+Special+Cheese"
                        " \n 3️⃣  *Rise plus Kota* = R25* \n Chips+Polony+vienna+Cheese+Egg+Special"
                        " \n 4️⃣  *Bull Kota* = R30* \n Chips+Polony+vienna+Cheese+Egg+Russian"
                        " \n 5️⃣  *Dulax Kota* = R40* \n Chips+Polony+vienna+Cheese+Egg+Russian+Burger"
                        " \n 6️⃣  *Quantum Kota* = R50* \n Chips+Polony+vienna+Cheese+Egg+Russian+Burger+Beacon+lettuce"
                        " \n 7️⃣  *Ibus Kota* = R160* \n Chips+Polony+vienna+Cheese+Egg+Russian+Burger+Beacon+lettuce"
                        " \n 0️⃣ To *Go back* ")
        elif 1 <= option <= 4:
            inside = ["Archer and Chilli", "Archer and No Chilli", "No Archer and Chilli", "No Archer and No Chilli"]
            selected = inside[option - 1]
            users.update_one(
                {"number": number}, {"$set": {"status": "payment"}})
            users.update_one(
                {"number": number}, {"$set": {"insideDesc": selected}})
            res.message(
                "*Order Summary*\n\n"
                f"you have ordered *{user['item']}*"
                f" \n ({user['selected_desc']})"
                f" \n ================================"
                f" \n *Amount Due = {user['selected_price']}*"
                " \n 1️⃣ Submit Payment"
                " \n 2️⃣ Go Back to Menu"
                " \n 0️⃣ Go back"
                )

    #         ######################################## payment page
    elif user["status"] == "payment":
        try:
            option = int(text)
        except:
            res.message("Please enter a valid response")
            return str(res)
        if option == 0:
            users.update_one(
                {"number": number}, {"$set": {"status": "summary"}})
            res.message(
                "Do you want your kota to have one of the following bellow? \n\n Please *Select* one of the options below:"
                " \n\n 1️⃣ Archer and Chilli"
                " \n 2️⃣ Archer and No Chilli"
                " \n 3️⃣ No Archer and Chilli"
                " \n 4️⃣ No Archer and No Chilli"
                " \n 0️⃣ Go back"
            )

        elif option == 1:
            res.message(
                "*Payment Mode*\n\n"
                f"you have ordered *{user['item']}*"
                f" \n ({user['selected_desc']})"
                f" \n =================="
                f" \n *Amount Due = {user['selected_price']}*\n\n"
                "Please *Click* on the link below to process payment\n"
                f"{user['link_price']}"
                " \n 1️⃣ Cancel Order"
                " \n 0️⃣ Go back")



    # ==================================== begger=================================

    elif user["status"] == "burgers":
        try:
            option = int(text)
        except:
            res.message("Please enter a valid response")
            return str(res)
        if option == 0:
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            res.message("Hi, Welcome back to *Musa's Khotas*.\nYou can choose from one of the options below: "
                        "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ For *Kotas*"
                        " Menu \n 3️⃣ For *Burgers* Menu \n 4️⃣ "
                        "To know our *working hours*  \n 5️⃣To get our *address* ")

        elif 1 <= option <= 4:
            burgers = ["City burgers", "The Mountain Burge", "AmaleVelves Burger", "Rock burger"]
            burger_price = ["R25", "R35", "R45", "R50"]
            burger_desc = ["Beef Pattie,lettuce,Tomatoe,Red onion,Cheese,Chips,Cucumber",
                         "Beef Pattie,lettuce,Tomatoe,Red onion,Cheese,Chips,Chesse,Omlette Egg,Beacon,Chips",
                         "Double Beef Pattie,lettuce,Tomatoe,Red onion, Double Cheese,Cucumber,Omlette,Beacon,Chips",
                         "Double Beef Pattie,lettuce,Tomatoe,Red onion,Omlette,Double Cheese,Avocado,Beacon,Egg"]
            link_price = ["https://pay.ikhokha.com/the-hub-inc/mpr/cityburgers", "https://pay.ikhokha.com/the-hub-inc/mpr/iphonese", "www.google.com",
                          "https://www.youtube.com"]

            selected = burgers[option - 1]
            burger_price = burger_price[option - 1]
            burger_desc = burger_desc[option - 1]
            link_price = link_price[option - 1]
            users.update_one({"number": number}, {"$set": {"status": "payment_burger"}})
            users.update_one({"number": number}, {"$set": {"item": selected}})
            users.update_one({"number": number}, {"$set": {"burger_price": burger_price}})
            users.update_one({"number": number}, {"$set": {"burger_desc": burger_desc}})
            users.update_one({"number": number}, {"$set": {"link_price": link_price}})


            res.message(
                " \n Please *confirm* your order by typing \n one of the following bellow option"
                " \n 1️⃣ Submit payment"
                " \n 0️⃣ Go back")

    elif user["status"] == "payment_burger":
        try:
            option = int(text)
        except:
            res.message("Please enter a valid response")
            return str(res)
        if option == 0:
            users.update_one(
                {"number": number}, {"$set": {"status": "burgers"}})
            res.message("You can select one of the following *burger Menu* to order from: "
                        "\n\n 1️⃣ *City burgers* = R25 \n Beef Pattie,lettuce,Tomatoe,Red onion,Cheese,Chips,Cucumber"
                        " \n 2️⃣  *The Mountain Burger* = R35* \n Beef Pattie,lettuce,Tomatoe,Red onion,Cheese,Chips,Chesse,Omlette Egg,Beacon,Chips"
                        " \n 3️⃣  *AmaleVelves Burger* = R45* \n Double Beef Pattie,lettuce,Tomatoe,Red onion, Double Cheese,Cucumber,Omlette,Beacon,Chips,"
                        " \n 4️⃣  *Rock burger* = R50* \n Double Beef Pattie,lettuce,Tomatoe,Red onion,Omlette,Double Cheese,Avocado,Beacon,Egg"
                        " \n 0️⃣ To *Go back* ")
        elif option == 1:
            users.update_one(
                {"number": number}, {"$set": {"status": "payment_done"}})
            res.message(
                "*Payment Mode*\n\n"
                f"you have ordered *{user['item']}*"
                f" \n ({user['burger_desc']})"
                f" \n =================="
                f" \n *Amount Due = {user['burger_price']}*\n\n"
                "Please *Click* on the link below to process payment\n"
                f"{user['link_price']}"
                " \n 0️⃣ Go back")

    elif user["status"] == "payment_done":
        try:
            option = int(text)
        except:
            res.message("Please enter a valid response")
            return str(res)
        if option == 0:
            users.update_one(
                {"number": number}, {"$set": {"status": "burgers"}})
            res.message("You can select one of the following *burger Menu* to order from: "
                        "\n\n 1️⃣ *City burgers* = R25 \n Beef Pattie,lettuce,Tomatoe,Red onion,Cheese,Chips,Cucumber"
                        " \n 2️⃣  *The Mountain Burger* = R35* \n Beef Pattie,lettuce,Tomatoe,Red onion,Cheese,Chips,Chesse,Omlette Egg,Beacon,Chips"
                        " \n 3️⃣  *AmaleVelves Burger* = R45* \n Double Beef Pattie,lettuce,Tomatoe,Red onion, Double Cheese,Cucumber,Omlette,Beacon,Chips,"
                        " \n 4️⃣  *Rock burger* = R50* \n Double Beef Pattie,lettuce,Tomatoe,Red onion,Omlette,Double Cheese,Avocado,Beacon,Egg"
                        " \n 0️⃣ To *Go back* ")








    users.update_one({"number": number}, {"$push": {"messages": {"text": text, "date": datetime.now()}}})
    return str(res)


if __name__ == "__main__":
    app.run()






