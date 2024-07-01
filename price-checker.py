import httpx
from bs4 import BeautifulSoup
import json
import time
from flask import Flask, render_template

import chatinteraction



def getItems(url, filename):
    # User-Agent header
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"

    # Additional headers
    headers = {"User-Agent": user_agent, "Referer": url}

    # Send a GET request to the URL with headers
    response = httpx.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse HTML content
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.find_all(class_="ad-listitem")
        
        # List to store items as dictionaries
        with open("./downloaded/"+filename + ".json", 'r') as file:
             previousdata = json.load(file)

        items_list = previousdata

        for index, item in enumerate(items):
            # Extract information from each item
            item_dict = {}

            # Extract link
            link = item.find(class_="ellipsis")
            if link and link.get("href"):
                # get description
                item_dict["link"] = "https://www.kleinanzeigen.de/" + link.get("href")
                articleresponse = httpx.get(
                    "https://www.kleinanzeigen.de/" + link.get("href"), headers=headers
                )
                if response.status_code == 200:
                    soup2 = BeautifulSoup(articleresponse.content, "html.parser")
                    description = soup2.find(id="viewad-description-text").text
                    item_dict["description"] = description
                    # print(soup2.find(id="viewad-description-text").text)

            else:
                item_dict["link"] = "Link not found"

            # Extract other information
            for subclass_name in [
                "aditem-main--middle--price-shipping--price",
                "ellipsis",
            ]:
                subclass = item.find(class_=subclass_name)
                if subclass:
                    if subclass_name == "ellipsis":
                        item_dict["name"] = subclass.text.strip()
                    else:
                        if (
                            subclass_name
                            == "aditem-main--middle--price-shipping--price"
                        ):
                            price = subclass.text.strip()
                            price = price.replace("\u20ac", "")
                            if price.endswith("VB"):
                                # Handle case where only VB is mentioned
                                priceVBremoved= price[:-2]
                                item_dict["price"] = int(priceVBremoved)
                                item_dict["vb"] = True
                            else:
                                try:
                                    
                                    
                                    item_dict["price"] = int(price)
                                    item_dict["vb"] = False
                                except ValueError:
                                    # Handle case where price is not available
                                    item_dict["price"] = "Price not available"
                                    item_dict["vb"] = False
                        else:
                            item_dict[subclass_name] = subclass.text.strip()

                else:
                    item_dict[subclass_name] = (
                        f"{subclass_name} not found for this item."
                    )
            # get description

            # Append item to list
            items_list.append(item_dict)
            print(f"{index+1} out of {len(items)} of Website loaded")
            

        # Save items as JSON objects in a file
        with open("./downloaded/"+filename + ".json", "w") as json_file:
            json.dump(items_list, json_file, indent=4)

        print("Items saved successfully.")
        
    else:
        print("Failed to fetch the webpage.")


def aiEdit(filename, produktname):
    with open("./downloaded/"+filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    output_file_path = f"./aiEdited/{filename}"

    # Start the JSON array
    with open(output_file_path, "w", encoding="utf-8") as json_file:
        json_file.write("[\n")

    for index, item in enumerate(data):
        # Extract relevant fields
        link = item.get("link", "N/A")
        description = item.get("description", "N/A").strip()
        price = item.get("price", "N/A")
        vb = item.get("vb", "N/A")
        name = item.get("name", "N/A")
        link = item.get("link", "N/A")
        
        if link == "Link not found":
            continue

        

       

        response = chatinteraction.request(
            f"Verhalte dich wie ein programm, dass entscheidet ob die nachfolgenden informationen über ein angebot den folgenden anforderungen entsprechen. wenn ja, dann antworte mit 1 wenn nicht, antworte mit 0 und ignoriere urls Anforderung: kein defekt vorliegend, wenige gebrauchsspuren, muss ein {produktname} sein, muss ein Angebot sein. Hier sind die infos zum ANgebot über dass du entscheiden sollst: beschreibung: {description} titel: {name} , triff nur eindeutige entscheidungen und antworte nur mit 0 wenn ersichtlich ist, dass die anforderungen nicht erfüllt wurden. Wenn keine expliziten angaben gemacht werden antworte mit 1"
        )

        
        print(f"{index} out of {len(data)} checked by AI")

        if response.startswith("1"):
            
            with open(output_file_path, "a", encoding="utf-8") as json_file:
                json.dump(item, json_file, indent=4)
                json_file.write(",\n")  # Add a comma and newline for better formatting
            time.sleep(7)

    # Remove the last comma and close the JSON array
    with open(output_file_path, "rb+") as json_file:
        json_file.seek(-2, 2)  # Move the cursor to the penultimate character (before the last comma and newline)
        json_file.truncate()  # Remove the last comma and newline
        json_file.write(b"\n]")  # Close the JSON array

app = Flask(__name__)


#@app.route("/")
#def home():
 #   return render_template("index.html")
#


#if __name__ == "__main__":
   # app.run(debug=True)
name="iPhone 11"
amountofpages=1


#for i in range(amountofpages):
getItems(f"https://www.kleinanzeigen.de/s-anbieter:privat/anzeige:angebote/versand:ja/preis:90:120/iphone-11/k0", name)


aiEdit(name+".json", name)
