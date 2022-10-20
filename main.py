import requests
import json

def main():
    
    makeplace_json = 'SaveMeiya.json'
    furniture_data = json.load(open(makeplace_json))
    
    class Item:
        def __init__(self, name, itemid, quantity, price_list, world_list, not_on_market):
            self.name = name
            self.itemid = itemid
            self.quantity = quantity
            self.price_list = price_list
            self.world_list = world_list
            self.not_on_market = not_on_market
        
        def iterate(self):
            self.quantity += 1
            
        def flag(self):
            self.not_on_market = 1 
             
                
    def parse_shoppinglist(data):
        
        itemid_list = []
        object_list = []
        
        for furniture in data["interiorFurniture"]:
            
            if furniture["itemId"] in itemid_list:
                itemid_index = itemid_list.index(furniture["itemId"])
                object_list[itemid_index].iterate()
            else:
                itemid_list.append(furniture["itemId"])
                object_list.append(Item(furniture["name"], furniture["itemId"], 1, [], [], 0))
        
        return object_list, itemid_list
    
    def flag_unresolved(price_list):
        
        for obj in furnitures:
            if obj.itemid in price_list["unresolvedItems"]:
                obj.flag()
    
    def get_prices(world_dc_region):
        
        total_cost = 0
        unique_worlds = set()
        
        largest_quantity = []
        for furniture in furnitures:
            largest_quantity.append(furniture.quantity)
        largest_quantity = max(largest_quantity)
        
        itemid_string = ','.join(str(x) for x in itemids)
        
        universalis_query = 'https://universalis.app/api/v2/{location}/{item_list}?listings={listings}&entries=0'            
        price_request = requests.get(universalis_query.format(location=world_dc_region, item_list=itemid_string, listings=largest_quantity))
        
        prices = price_request.json()
        flag_unresolved(prices)
        
        for furniture in furnitures:
            if furniture.not_on_market == 0:
                #print('working on' + obj.name)
                temp_item_id = str(furniture.itemid)
                for listing in prices["items"][temp_item_id]["listings"][:furniture.quantity]:
                    furniture.price_list.append(listing["pricePerUnit"])
                    total_cost = total_cost + listing["pricePerUnit"]
                    furniture.world_list.append(listing["worldName"])
                    unique_worlds.add(listing["worldName"])
        
        return total_cost, unique_worlds           
    
       
    furnitures, itemids = parse_shoppinglist(furniture_data)
    total_cost, unique_worlds = get_prices('Light')
    print(f"Total Cost: {total_cost:,} gil")
    print(f"Items found on {unique_worlds}")
    print("All done!")
           

if __name__ == '__main__':
    main()