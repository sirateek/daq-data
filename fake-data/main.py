import pymongo
import random

myclient = pymongo.MongoClient("mongodb+srv://Tdean:12345@daq.fg7tz9x.mongodb.net/?retryWrites=true&w=majority")
daq = myclient["HappyEWater"]

elect = daq["Electric"]

endFocusedTime = 1669475129144
diff = 7230000

focusedTime = endFocusedTime - diff
amp = 0.5

for x in elect.find({"timestamp": {"$gte": focusedTime, "$lte": endFocusedTime}}):
    fake_amp = amp + (random.randint(0, 999999) / 10000000)
    fake_amp = round(fake_amp, 7)
    print(fake_amp)
    elect.update_one({"_id": x["_id"]}, {"$set": {"amp": fake_amp, "watt": fake_amp * 5}})
