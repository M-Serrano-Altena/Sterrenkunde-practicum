# Marc Serrano Altena
# 04-11-2022
# dit programma kijkt wanneer een bepaald persoon aan de beurt is voor het sterrenkunde practicum

from googleapiclient.errors import HttpError
import email
import base64
from Google import create_service
from math import trunc

# gegevens om te verbinden met gmail
CLIENT_SECRET_FILE = 'client_secret_file.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# maak verbinding met gmail
service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES) 

# zoek naar bepaalde e-mails
def search_messages(service, user_id, search_string):
    try:
        search_id = service.users().messages().list(userId=user_id, q=search_string).execute()

        number_results = search_id['resultSizeEstimate']

        final_list = []
        if number_results > 0:
            message_ids = search_id['messages']

            for ids in message_ids:
                final_list.append(ids['id'])

            return final_list

        else:
            print("There were 0 results for that search string, returning an empty string")
            return ""

    except HttpError as error:
        print(f"An error has occurred: {error}")


# lees de e-mail en bepaal waar op de lijst iemand aan de beurt is
def get_message(service, user_id, msg_id, naam):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id, format='raw').execute()

        msg_raw = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))

        msg_str = email.message_from_bytes(msg_raw)

        content_types = msg_str.get_content_maintype()

        if content_types == 'multipart':
            # part 1 is plain text, _ is html text
            part1, *_, = msg_str.get_payload()
            part1 = part1.get_payload()
            part1 = base64.b64decode(part1)
            part1 = part1.decode('utf-8')

            tussenvoegsels = ['de', 'van', 'van de', 'van der', 'van den', 'el', 'le', 'ter', 'ten']
            full_name = "place-holder"
            begin = False
            counter = 0
            stand_by = False
            semi_stand_by = False
            overig = False
            stop = False
            lines = part1.split('\n')
            
            for line in enumerate(lines):
                line = list(line)

                line[1] = line[1].replace("\r", "")
                line = tuple(line)

                if line[1] == "" or line[1].casefold() in tussenvoegsels:
                    continue

                if "De volgende" in line[1] and "studenten staan stand-by" in line[1]:
                    begin = True
                    stand_by = True
                
                elif stand_by:
                    counter += 0.5

                if "De volgende studenten staan semi-stand-by" in line[1]:
                    stand_by = False
                    counter = 0
                    semi_stand_by = True

                elif semi_stand_by:
                    counter += 0.5

                if line[1] == "De rest van de lijst in volgorde:":
                    semi_stand_by = False
                    counter = 0
                    overig = True

                elif overig:
                    counter += 0.5
                
                if counter % 1 == 0 and begin:
                    stop = False
                    lines[line[0] - 1] = lines[line[0] - 1].replace("\r", "")
                    
                    if lines[line[0] - 1].casefold() in tussenvoegsels:  
                        lines[line[0] - 2] = lines[line[0] - 2].replace("\r", "")
                        full_name = f"{line[1]} {lines[line[0] - 1]} {lines[line[0] - 2]}"
                    
                    elif lines[line[0] - 1].casefold() == "":
                        lines[line[0] - 2] = lines[line[0] - 2].replace("\r", "")
                        full_name = f"{line[1]} {lines[line[0] - 2]}"

                    else:
                        full_name = f"{line[1]} {lines[line[0] - 1]}"

                # casefold maakt alles lower case
                if naam.casefold() in full_name.casefold() and not stop:
                    stop = True
                    if stand_by and counter != 0:
                        print()
                        print(f"{full_name}: {round(counter)}e op stand-by, kan tot 4 uur 's middags opgeroepen worden")


                    elif semi_stand_by and counter != 0:
                        print()
                        print(f"{full_name}: {round(counter)}e op semi-stand-by, waarschijnlijk eerst volgende heldere dag aan de beurt", end="")

                        if counter <= 15:
                            print(f", maar als {round(counter)} mensen afvallen ben je vandaag aan de beurt.")


                    elif overig and counter != 0:
                        print()
                        print(f"{full_name}: {round(counter)}e in de overige lijst, waarschijnlijk op de {trunc(counter / 30) + 3}e heldere dag aan de beurt.")

            return 

    except HttpError as error:
        print(f"An error has occurred: {error}")

# main programma
if __name__ == '__main__':
    msg_ids = search_messages(service, 'me', 'from:m.r.sloot@uva.nl subject: stand-by')
    naam = input("Voer je (volledige) naam in: ")
    
    # de derde parameter is iemands (volledige) naam
    get_message(service, 'me', msg_ids[0], naam) 