#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pickle as p
import requests, json

with open('mark_model.data', 'rb') as f:
    mark_model = p.load(f)

url = "https://auto.ru/-/ajax/desktop/listing/"

headers = {
    ///...///
}

bodyType = brand = color = fuelType = modelDate = name = numberOfDoors = productionDate = transmission = engineDisplacement = enginePower = description = mileage = complectation = lk_summary_WD = steering_wheel = owners_number = pts = custom_cleared = purchase_date = Price = []
auto_ru = {}
id_ = 0

for mark in mark_model:
    if mark in ['MERCEDES', 'INFINITI', 'NISSAN', 'BMW', 'VOLKSWAGEN',
       'MITSUBISHI', 'TOYOTA', 'VOLVO', 'SKODA', 'LEXUS', 'AUDI', 'HONDA',
       'SUZUKI']:
        for model in mark_model[mark]:
            for page in range(1, 600):
                param = {
                    'catalog_filter' : [{"mark": mark, "model": model}],
                    'section': "used",
                    'category': "cars",
                    'sort': "fresh_relevance_1-desc",
                    "top_days":"1",
                    "geo_radius":200,
                    "geo_id":[213],
                    'page': page
                }
                response = requests.post(url, json=param, headers = headers)
                data = response.json()


                if data['offers'] != []:

                    for i in data['offers']:

                        # 1. bodyType:
                        try: bodyType = i['vehicle_info']['configuration']['human_name']
                        except: bodyType = None

                        # 2. brand
                        try: brand = i['vehicle_info']['mark_info']['code']
                        except: brand = None

                        # 3. color
                        try: color = i['color_hex']
                        except: color = None

                        # 4. fuelType
                        try: fuelType = i['lk_summary'].split()[-1]
                        except: fuelType = None

                        # 5. modelDate
                        try: modelDate = i['vehicle_info']['super_gen']['year_from']
                        except: modelDate = None

                        # 6. name
                        try: name =  i['vehicle_info']['tech_param']['human_name']
                        except: name = None

                        # 7. numberOfDoors
                        try: numberOfDoors = i['vehicle_info']['configuration']['doors_count']
                        except: numberOfDoors = None

                        # 8. productionDate
                        try: productionDate = i['documents']['year']
                        except: productionDate = None

                        # 9. vehicleConfiguration
                        try: transmission = i['vehicle_info']['tech_param']['transmission']
                        except: transmission = None

                        # 10. engineDisplacement
                        try: engineDisplacement = i['vehicle_info']['tech_param']['human_name'].split()[0]
                        except: engineDisplacement = None

                        # 11. enginePower
                        try: enginePower = i['vehicle_info']['tech_param']['power']
                        except: enginePower = None

                        # 12. description
                        try: description = i['description']
                        except: description = None

                        # 13. mileage
                        try: mileage = i['state']['mileage']
                        except: mileage = None

                        # 14. Комплектация
                        try: complectation = i['vehicle_info']['complectation']
                        except: complectation = None

                        # 15. Привод
                        try: lk_summary_WD = i['lk_summary'].split(', ')[-2]
                        except: lk_summary_WD = None

                        # 16. Руль
                        try: steering_wheel = i['vehicle_info']['steering_wheel']
                        except: steering_wheel = None

                        # 17. Владельцы
                        try: owners_number = i['documents']['owners_number']
                        except: owners_number = None

                        # 18. ПТС
                        try: pts = i['documents']['pts']
                        except: pts = None

                        # 19. Таможня
                        try: custom_cleared = i['documents']['custom_cleared']
                        except: custom_cleared = None

                        # 20. Владение
                        try: purchase_date =  i['documents']['purchase_date']
                        except: purchase_date = None

                        # 21. Price
                        try: Price = i['price_info']['RUR']
                        except: Price = None


                        auto_ru[id_] = {
                            'bodyType': bodyType,
                            'brand': brand,
                            'color': color,
                            'fuelType': fuelType,
                            'modelDate': modelDate,
                            'name': name,
                            'numberOfDoors': numberOfDoors,
                            'productionDate': productionDate,
                            'vehicleConfiguration': transmission,
                            'engineDisplacement': engineDisplacement,
                            'enginePower': enginePower,
                            'description': description,
                            'mileage': mileage,
                            'Комплектация': complectation,
                            'Привод': lk_summary_WD,
                            'Руль': steering_wheel,
                            'Владельцы': owners_number,
                            'ПТС': pts,
                            'Таможня': custom_cleared,
                            'Владение': purchase_date,
                            'Price': Price    
                        }

                        id_ += 1

                    print(f'Page: {page}', mark, model, id_)
                else:
                    break


# In[ ]:


import pandas as pd
auto_ru_csv = pd.DataFrame(auto_ru).T
auto_ru_csv.to_csv('15_04auto_ru_csv_99.csv', index=True)


# In[ ]:




