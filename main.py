import requests
import json
    
class Item:
    def __init__(self, name, itemid, quantity, price_list, world_list, not_on_market):
        self.name = name
        self.itemid = itemid
        self.quantity = quantity
        self.price_list = price_list
        self.world_list = world_list
        self.not_on_market = not_on_market

    def increment(self):
        self.quantity += 1

    def flag_not_on_market(self):
        self.not_on_market = True

    def append_world_price(self, listing):
        self.price_list.append(listing["pricePerUnit"])
        self.world_list.append(listing["worldName"])
    
    def get_itemid_str(self):
        return str(self.itemid)

class World:
    def __init__(self, name, furniture_totals, world_total_price):
        self.name = name
        self.furniture_totals = furniture_totals
        self.world_total_price = world_total_price

    def add_to_totals(self, furniture_name, furniture_count):
        self.furniture_totals.append([furniture_name, furniture_count])

    def add_to_price(self, amount):
        self.world_total_price += amount

class Shopper:
    def __init__(self, data):
        self.parse_shoppinglist(data)

    def parse_shoppinglist(self, data):
        
        itemid_list = []
        object_list = []
        
        for furniture in data["interiorFurniture"]:
            
            if furniture["itemId"] in itemid_list:
                itemid_index = itemid_list.index(furniture["itemId"])
                object_list[itemid_index].increment()
            else:
                itemid_list.append(furniture["itemId"])
                object_list.append(Item(furniture["name"], furniture["itemId"], 1, [], [], not_on_market=False))
        
        self.furnitures = object_list
        self.itemIds = itemid_list
        return object_list, itemid_list
    
    def flag_unresolved(self, price_list):
        for obj in self.furnitures:
            if obj.itemid in price_list["unresolvedItems"]:
                obj.flag_not_on_market()
    
    def get_prices(self, world_dc_region):
        prices = self.get_price_request(world_dc_region)
        self.flag_unresolved(prices)
        return self.process_price_listings(prices)

    def process_price_listings(self, prices):
        # maybe store these as member variables to be retrieved later
        total_cost = 0
        unique_worlds = set()
        not_on_market = []
        
        for furniture in self.furnitures:
            if furniture.not_on_market:
                not_on_market.append([furniture.name, furniture.itemid])
            else:
                for listing in prices["items"][furniture.get_itemid_str()]["listings"][:furniture.quantity]:
                    furniture.append_world_price(listing)
                    total_cost += listing["pricePerUnit"]
                    unique_worlds.add(listing["worldName"]) # replace with a `get_unique_worlds` call that loops furnitures to get worlds
        return total_cost, unique_worlds, not_on_market

    def get_price_request(self, world_dc_region):
        largest_quantity = self.get_largest_quantity()
        itemid_string = ','.join(str(x) for x in self.itemids)
        universalis_query = 'https://universalis.app/api/v2/{location}/{item_list}?listings={listings}&entries=0'            
        price_request = requests.get(universalis_query.format(
            location=world_dc_region, item_list=itemid_string, listings=largest_quantity))
        return price_request.json()

    def get_largest_quantity(self):
        largest_quantity = [furniture.quantity for furniture in self.furnitures]
        return max(largest_quantity)
    
    def create_worlds(self, furnitures, unique_worlds):
        world_list = [World(name, [], 0) for name in unique_worlds]
        for world in world_list:
            for furniture in furnitures:
                world_item_count = furniture.world_list.count(world.name)
                if world_item_count > 0 and not furniture.not_on_market:
                    # Super lazy and innacurate I know
                    world.add_to_price(int(sum(furniture.price_list)/world_item_count))
                    world.add_to_totals(furniture.name, world_item_count)
        return world_list
                
    def print_world_shopping_list(self, worlds):
        for world in worlds:
            
            print(f'Your shopping list for {world.name} will cost approx. {world.world_total_price:,} gil')
            print('------------------------')
            
            for furniture in world.furniture_totals:
                print(f'{furniture[1]}x {furniture[0]}')
            print('------------------------')
            print(' ')
    
    def make_shopping_list(self):
        total_cost, unique_worlds, not_on_market = self.get_prices('Light')
        worlds = self.create_worlds(self.furnitures, unique_worlds)
        
        self.print_world_shopping_list(worlds)
        self.print_footer(total_cost, unique_worlds, not_on_market)

    def print_footer(self, total_cost, unique_worlds, not_on_market):
        print(f"Total Cost: {total_cost:,} gil")
        print(f"Items found on {unique_worlds}")
        print('')
        print(f'Could not find these items on the market: {not_on_market}')    
        print("Thank you for shopping with us today!")

def main():
    makeplace_json = 'SaveMeiya.json'
    furniture_data = json.load(open(makeplace_json))
    shopper = Shopper(furniture_data)
    shopper.make_shopping_list()

if __name__ == '__main__':
    main()