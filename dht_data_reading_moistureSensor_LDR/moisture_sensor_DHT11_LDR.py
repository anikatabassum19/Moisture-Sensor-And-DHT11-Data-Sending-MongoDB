import serial.tools.list_ports
from pymongo.mongo_client import MongoClient
import time

# Establish a connection to MongoDB
uri = "mongodb+srv://orchi19:orchi4466@cluster0.sylimnz.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri)

db = client['sensorreadings']
collection = db['readings']

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
portList = []

for onePort in ports:
    portList.append(str(onePort))
    print(str(onePort))

val = input("select port: ")

for x in range(0, len(portList)):
    if portList[x].startswith("/dev/" + str(val)):
        portVar = "/dev/" + str(val)
        print(portList[x])

serialInst.baudrate = 9600
serialInst.port = portVar
serialInst.open()

while True:
    if serialInst.in_waiting:
        packet = serialInst.readline()
        try:
            decoded_packet = packet.decode('utf-8')
            print(decoded_packet)
            
            # Extract temperature and humidity values
            decoded_packet = decoded_packet.strip()
            
            temperature_str = None
            if "Temperature: " in decoded_packet:
                temperature_str = decoded_packet.split("Temperature: ")[1].split(" °C")[0].strip()
            
            humidity_str = None
            if "Humidity: " in decoded_packet:
                humidity_str = decoded_packet.split("Humidity: ")[1].split(" %")[0].strip()
            
            moisture_str = None
            if "Moisture Value is: " in decoded_packet:
                moisture_str = decoded_packet.split("Moisture Value is: ")[1].strip()
            
            # Print the values
            if temperature_str:
                print("Temperature Value:", temperature_str, "°C")
            else:
                print("Temperature Value: N/A")
            
            if humidity_str:
                print("Humidity Value:", humidity_str, "%")
            else:
                print("Humidity Value: N/A")
            
            if moisture_str:
                print("Moisture Value:", moisture_str)
            else:
                print("Moisture Value: N/A")
            
            # Convert temperature, humidity, and moisture to float if possible
            try:
                temperature = float(temperature_str) if temperature_str else None
                humidity = float(humidity_str) if humidity_str else None
                moisture = float(moisture_str) if moisture_str else None
            except ValueError:
                print("Invalid temperature, humidity, or moisture value")
                continue
            
            # Prepare the data to be sent
            data = {
                'temperature': temperature,
                'humidity': humidity,
                'moisture': moisture
            }
            
            # Insert the data into the MongoDB collection
            collection.insert_one(data)
            time.sleep(2)
                
        except UnicodeDecodeError:
            decoded_packet = packet.decode('latin-1')
            print(decoded_packet)
            
# Close the MongoDB connection
client.close()


