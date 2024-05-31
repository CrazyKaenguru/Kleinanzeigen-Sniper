import httpx
from bs4 import BeautifulSoup
import json
import time







url = "https://www.kleinanzeigen.de/s-iphone-x/k0"


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
        items_list = []

        for item in items:
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
                                item_dict["price"] = "VB"
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

        # Save items as JSON objects in a file
        with open(filename + ".json", "w") as json_file:
            json.dump(items_list, json_file, indent=4)

        print("Items saved successfully.")
    else:
        print("Failed to fetch the webpage.")


def aiEdit(filename, produktname):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Initialize an empty list to store the extracted items
    for item in data:
        # Extract relevant fields
        link = item.get("link", "N/A")
        description = item.get("description", "N/A").strip()
        price = item.get("price", "N/A")
        vb = item.get("vb", "N/A")
        name = item.get("name", "N/A")
        # print(link+description)
        import os

        import google.generativeai as genai

        genai.configure(api_key="AIzaSyAy4nbD6gOXpam0Gk5FlEIZo7Ziu5Kp0ME")

        # Create the model
        # See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
        ]

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            safety_settings=safety_settings,
            generation_config=generation_config,
        )

        chat_session = model.start_chat(history=[])

        response = chat_session.send_message(
            "Verhalte dich wie ein programm, dass entscheidet ob die nachfolgenden informationen über ein angebot den folgenden anforderungen entsprechen. wenn ja, dann antworte mit 1 wenn nicht, antworte mit 0 und ignoriere urls Anforderung: kein defekt vorliegend, wenige gebrauchsspuren,muss ein "
            + produktname
            + " sein, muss ein Angebot sein Informationen: beschreibung: "
            + description
            + "   titel: "
            + name
            + " , triff nur eindeutige entscheidungen und antworte nur mit 0 wenn ersichtlich ist, dass die anforderungen nicht erfüllt wurden. Wenn keine expliziten angaben gemacht werden antworte mit 1"
        )

        print(response.text)
        if response.text.startswith("1"):
            {print(link)}
            time.sleep(5)


# getItems(url, "iPhone X")
aiEdit("iPhone X.json", "iPhone X")
