# 1990958 Aaron Oviedo

import csv
from datetime import datetime


# class that contains methods to generate inventory files


class ProcessReports:
    def __init__(self, items):
        # add combined list
        self.items = items

    # FullInventory.csv. The items
    # should be sorted alphabetically by manufacturer. Each row should contain item
    # ID, manufacturer name, item type, price, service date, and list if it is damaged.
    # The item attributes must appear in this order.
    def full_inventory(self):
        with open('FullInventory.csv', 'w') as file:
            all_items = self.items
            # sort by keys so they can be organized by manufacturer..
            key_list = sorted(all_items.keys(), key=lambda x: all_items[x]['Manufacturer Name'])
            for item in key_list:
                item_id = item
                manu_name = all_items[item]['Manufacturer Name']
                item_type = all_items[item]['Item Type']
                item_price = all_items[item]['Price']
                service_date = all_items[item]['Service Date']
                item_damaged = all_items[item]['Damaged']
                file.write('{},{},{},{},{},{}\n'.format(item_id, manu_name, item_type,
                                                        item_price, service_date, item_damaged))

    # Item Type Inventory.csv. there should be a file for each item type and the item type
    # needs to be in the file name. Each row of the file should contain item ID,
    # manufacturer name, price,
    # service date, and list if it is damaged. The items should be sorted by their item ID.
    def item_type_list(self):
        all_items = self.items
        all_types = []
        key_list = sorted(all_items.keys())
        for item in all_items:
            item_type = all_items[item]['Item Type']
            # add new types to list for report generation if a file is added with different types
            if item_type not in all_types:
                all_types.append(item_type)
        for type in all_types:
            # assign new file name for each type
            file_name_type = type + 'Inventory.csv'
            with open(file_name_type, 'w') as file:
                for item in key_list:
                    item_id = item
                    manu_name = all_items[item]['Manufacturer Name']
                    item_price = all_items[item]['Price']
                    service_date = all_items[item]['Service Date']
                    item_damaged = all_items[item]['Damaged']
                    item_type = all_items[item]['Item Type']
                    # verify each row that is written matches file
                    if type == item_type:
                        file.write('{},{},{},{},{}\n'.format(item_id, manu_name,
                                                             item_price, service_date, item_damaged))

    # PastServiceDateInventory.csv  all the items that are past the service date
    # on the day the program is actually executed. Each row should contain: item ID,
    # manufacturer name, item type, price, service date, and list if it is damaged.
    # The items must appear in the order of service date from oldest to most recent
    def past_service_date(self):
        all_items = self.items
        # reverse = true makes dates go from oldest to most recent
        key_list = sorted(all_items.keys(), key=lambda x: datetime.strptime(all_items[x]['Service Date'],
                                                                            "%m/%d/%y").date(), reverse=True)
        with open('PastServiceDateInventory.csv', 'w') as file:
            for item in key_list:
                item_id = item
                manu_name = all_items[item]['Manufacturer Name']
                item_type = all_items[item]['Item Type']
                item_price = all_items[item]['Price']
                service_date = all_items[item]['Service Date']
                item_damaged = all_items[item]['Damaged']
                # compute todays date to verify expired items.
                current_date = datetime.now().date()
                expiration_date = datetime.strptime(service_date, "%m/%d/%y").date()
                if expiration_date < current_date:
                    file.write('{},{},{},{},{},{}\n'.format(item_id, manu_name, item_type,
                                                            item_price, service_date, item_damaged))

    # DamagedInventory.csv all items that are damaged. Each row should contain :
    # item ID, manufacturer name, item type, price, and service date.
    # The items must appear in the order of most expensive to least expensive.
    def damaged_inventory(self):
        all_items = self.items
        # order from most expensive to least expensive by reverse = true.
        key_list = sorted(all_items.keys(), key=lambda x: all_items[x]['Price'], reverse=True)
        with open('DamagedInventory.csv', 'w') as file:
            for item in key_list:
                item_id = item
                manu_name = all_items[item]['Manufacturer Name']
                item_type = all_items[item]['Item Type']
                item_price = all_items[item]['Price']
                service_date = all_items[item]['Service Date']
                item_damaged = all_items[item]['Damaged']
                if item_damaged:
                    file.write('{},{},{},{},{}\n').format(item_id, manu_name,
                                                          item_type, item_price, service_date)


# read in files and parse through the rows to assign the values.
if __name__ == "__main__":
    items_dict = {}
    files_list = ['ManufacturerList.csv', 'PriceList.csv', 'ServiceDatesList.csv']

    for file in files_list:
        with open(file, 'r') as input_csv:

            parse_csv = csv.reader(input_csv, delimiter=',')

            for row in parse_csv:
                # set item id immediately because its the common value
                item_ID = row[0]
                # separate commands based on what type of input file is entered (order of input)
                if file == files_list[0]:
                    # make 2 dimensional dict to organize by id as well and assign variables to each
                    items_dict[item_ID] = {}
                    manufact_name = row[1]
                    item_type = row[2]
                    damage_ind = row[3]
                    items_dict[item_ID]['Manufacturer Name'] = manufact_name.strip()
                    items_dict[item_ID]['Item Type'] = item_type.strip()
                    items_dict[item_ID]['Damaged'] = damage_ind.strip()
                elif file == files_list[1]:
                    item_price = row[1]
                    items_dict[item_ID]['Price'] = item_price
                elif file == files_list[2]:
                    service_date = row[1]
                    items_dict[item_ID]['Service Date'] = service_date

    # assign output to the class that will generate all of the reports
    inventory = ProcessReports(items_dict)
    # generate files from the methods defined above
    inventory.full_inventory()
    inventory.item_type_list()
    inventory.past_service_date()
    inventory.damaged_inventory()

    # create lists of all manufacturers and item types captured so far.
    prod_manu_list = []
    prod_types_list = []
    # loop through each item in the dictionary created before with indexes for each type of data.
    for item in items_dict:
        manu_index = items_dict[item]['Manufacturer Name']
        type_index = items_dict[item]['Item Type']
        # Because the files will change, this will add in the new manufacturers or product types that are introduced.
        # They can then be compared to the user query in the next section.
        if manu_index not in prod_manu_list:
            prod_manu_list.append(manu_index)
        if type_index not in prod_types_list:
            prod_types_list.append(type_index)

    # Query the user of an item by asking for manufacturer and item type with a single query.
    query_user = None
    # After output for one query, query the user again. Allow ‘q’ to quit.
    while query_user != 'q' and query_user != 'Q':
        print("Enter a Manufacturer Name and Product Type to search Inventory. (Ex: Apple computer)\n Enter q "
              "to quit: ")
        query_user = input()
        # Exit loop if q is entered or capital Q as mistype.
        if query_user == 'q' or query_user == 'Q':
            break
        # execute the loop for any other input
        else:
            user_manu = None
            user_type = None
            query_user = query_user.split()
            error = False
            # able to parse more than two words
            for input in query_user:
                # if the input is a duplicate manufacturer it will raise an error.
                if input in prod_manu_list:
                    if user_manu:
                        error = True
                    else:
                        # set unique input as manufacturer first
                        user_manu = input
                elif input in prod_types_list:
                    # if the input is a duplicate it will raise an error.
                    if user_type:
                        error = True
                    else:
                        # set unique input as product type first
                        user_type = input

            # Print a message(“No such item in inventory”) if either the manufacturer
            # or the item type are not in the inventory, more that one of either type
            # is submitted or the combination is not in the inventory.
            if not user_manu or not user_type or error:
                print("No such item in inventory.")
            else:
                # Sort the items based on price , Reverse orders from high to low, lambda allows for
                # full expression to be assigned to the price value from the list dictionary.
                key_list = sorted(items_dict.keys(), key=lambda x: items_dict[x]['Price'], reverse=True)

                # list of matching items that collects user input
                match_user_items = []

                # create a dict to collect items that are from differing manufacturers
                consider_items = {}

                for item in key_list:
                    # operates so that items type is the main requirement, while manufacturer can be assessed later.
                    if items_dict[item]['Item Type'] == user_type:
                        # Do not provide items that are past their service date or damaged.
                        service_expired = None
                        date_today = datetime.now().date()
                        service_date = items_dict[item]['Service Date']
                        expiration_date = datetime.strptime(service_date, "%m/%d/%y").date()
                        # comparison to trigger expiration flag
                        if expiration_date < date_today:
                            service_expired = True
                        # if manufacturer matches the user input it will be added to the match items list.
                        # Must not have expired service or be damaged.
                        if items_dict[item]['Manufacturer Name'] == user_manu:
                            if service_expired != True and not items_dict[item]['Damaged']:
                                match_user_items.append((item, items_dict[item]))
                        # otherwise add to items to consider. # Must not have expired service or be damaged.
                        else:
                            if service_expired != True and not items_dict[item]['Damaged']:
                                consider_items[item] = items_dict[item]

                # if the value exists and has been assigned, code will execute
                if match_user_items:
                    match = match_user_items[0]
                    match_name = match[0]
                    match_manu = match[1]['Manufacturer Name']
                    match_type = match[1]['Item Type']
                    match_price = match[1]['Price']
                    # Print “Your item is:” with the item ID, manufacturer name, item type and price on one line.
                    print("Your item is: {}, {}, {}, {}\n".format(match_name, match_manu, match_type, match_price))

                    if consider_items:
                        price_index = match_price
                        consider_item = None
                        consider_index = None
                        for item in consider_items:
                            if consider_index == None:
                                consider_item = consider_items[item]
                                # calculate price difference between closest item.
                                consider_index = abs(int(price_index) - int(consider_items[item]['Price']))
                                consider_name = item
                                consider_manu = consider_items[item]['Manufacturer Name']
                                consider_type = consider_items[item]['Item Type']
                                consider_price = consider_items[item]['Price']
                                continue
                            #store this difference for comparison with next item/
                            difference = abs(int(price_index) - int(consider_items[item]['Price']))

                            #evaluate and compare each loop to find the most expensive item that is similar.
                            # Price must be higher than the last to change
                            if difference < consider_index:
                                consider_item = item
                                consider_index = difference
                                consider_name = item
                                consider_manu = consider_items[item]['Manufacturer Name']
                                consider_type = consider_items[item]['Item Type']
                                consider_price = consider_items[item]['Price']

                        # print “You may, also, consider:” and print information about the same item type
                        # from another manufacturer that closes in price to the output item.
                        # Only print this if the same item from another manufacturer is in the inventory and
                        # is not damaged nor past its service date.
                        print("You may also consider: {}, {}, {}, {}\n".format(consider_name, consider_manu,
                                                                               consider_type, consider_price))
                    else:
                        print("No such item in inventory.")
