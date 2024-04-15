from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from geopy.distance import geodesic
from math import atan2, degrees, radians, sin, cos, atan

import requests
import csv
import time

app = Flask(__name__)
socketio = SocketIO(app, allow_unsafe_werkzeug=True)

spot_key = '02pfMzOEoG1mT9UMNCG4WPsVmoIlA4RqY'
csv_file_path = 'out.csv'
cellNames = ['Date', 'Time', 'psi', 'temperature', 'altitude', 'CO2level', 'relativeHumidity', 'scdTemperature', 'bmp_temperature','bmp_pressure','bmp_altitude', 'duration', 'uSvh', 'uSvhError', 'cpm'] #'Date', 'Time', 'psi', 'temperature', 'altitude', 'CO2level', 'relativeHumidity', 'scdTemperature', 'bmp_temperature','bmp_pressure','bmp_altitude'
wantedCells = ['Date', 'Time', 'psi', 'CO2level', 'relativeHumidity', 'scdTemperature', 'bmp_temperature','bmp_pressure','bmp_altitude', 'duration', 'uSvh', 'cpm']
pos_csv = 'pos.csv'
pos_info = {
	'altitude': None,
	'azimuth': None,
	'distance': None,
	'view_angle': None, # atan(distance/altitude)
	'start_pos': [None, None],
	'current_pos': [None, None]
}
try:
	with open(pos_csv, 'r', encoding='utf-8-sig') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			for key, value in row.items():
				if value.isdigit():
					pos_info[key] = int(value)
				elif '.' in value and all(part.isdigit() for part in value.split('.')):
					pos_info[key] = float(value)
				elif ',' in value:
					values_list = [float(x.replace('[', '').replace(']', '')) for x in value.split(',')]
					pos_info[key] = values_list
				else:
					pos_info[key] = value
except Exception as e:
	print('no pos info file:', e)

client_rows = {}

@app.route('/')
def index():
	return render_template('index.html')

def calculate_azimuth(origin, destination):
	lat1, lon1 = radians(origin[0]), radians(origin[1])
	lat2, lon2 = radians(destination[0]), radians(destination[1])

	delta_lon = lon2 - lon1
	y = sin(delta_lon) * cos(lat2)
	x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(delta_lon)
	initial_bearing = atan2(y, x)

	azimuth = (degrees(initial_bearing) + 360) % 360
	return azimuth

def getspotpos(sid):
	try:
		global pos_info
		response = requests.get(f"https://api.findmespot.com/spot-main-web/consumer/rest-api/2.0/public/feed/{spot_key}/latest.json")
		response.raise_for_status()
		data = response.json()
		message = data['response']['feedMessageResponse']['messages']['message']
		pos_info['current_pos'] = [message['latitude'], message['longitude']]
		if pos_info['start_pos'] == [None, None]:
			pos_info['start_pos'] = [message['latitude'], message['longitude']]
		pos_info['azimuth'] = calculate_azimuth(pos_info['start_pos'], pos_info['current_pos'])
		pos_info['distance'] = geodesic(pos_info['start_pos'], pos_info['current_pos']).meters
		if pos_info['altitude']:
			pos_info['view_angle'] = degrees(atan(pos_info['distance']/float(pos_info['altitude'])))

		socketio.emit('update_pos', pos_info, namespace='/test', room=sid)
		with open(pos_csv, 'w', newline='', encoding='utf-8-sig') as csvfile:
			fieldnames = pos_info.keys()
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writeheader()
			writer.writerow(pos_info)
	except Exception as e:
		print('error accessing Spot API:', e)

def send_existing_rows(sid):
	global pos_info
	with open(csv_file_path, 'r', encoding='utf-8-sig') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		client_rows[sid] = []
		print(sid)
		for row in csv_reader:
			row = {key: value for key, value in row.items() if key in wantedCells}
			client_rows[sid].append(row)
			socketio.emit('update_table', row, namespace='/test', room=sid)
			pos_info['altitude'] = row['bmp_altitude']



def generate_data_from_csv(sid):
	global pos_info
	with open(csv_file_path, 'r', encoding='utf-8-sig') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			row = {key: value for key, value in row.items() if key in wantedCells}
			if row not in client_rows[sid]:
				socketio.emit('update_table', row, namespace='/test', room=sid)
				client_rows[sid].append(row)
				pos_info['altitude'] = row['bmp_altitude']
			time.sleep(0.1)


@socketio.on('connect', namespace='/test')
def connect():
	sid = request.sid
	# emit('connect', {'data': 'Connected'})
	send_existing_rows(sid)
	getspotpos(sid)



@socketio.on('datapls', namespace='/test')
def data_request():
	sid = request.sid
	print('request for data from ' + sid)
	generate_data_from_csv(sid)

@socketio.on('pospls', namespace='/test')
def pos_request():
	sid = request.sid
	print('position data request from ' + sid)
	getspotpos(sid)


if __name__ == '__main__':
	socketio.run(app, debug=True, allow_unsafe_werkzeug=True)