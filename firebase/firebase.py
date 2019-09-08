import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import json
import numpy as np

from datetime import date

cred = credentials.Certificate("C:/Users/Harrison/Documents/helpinghand-secret.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

doc_ref = db.collection(u'users').document(u'testUser')

input_file = open('positive.json')
json_array = json.load(input_file)['testUser']

#############################################################################################
# Get mean of first 10 heartbeats, anxiety leads to 8~20 extra beats per minute
avg10 = np.average(json_array[:10][0]['heartbeat']) + 9
# Are they still in withdrawal?
withdrawal = doc_ref.get().to_dict()['hhAssistance']

print(avg10)
# If heartbeat spikes above mean, set boolean and timestamp
for i in range(0, len(json_array)-3):
	tick = json_array[i]
	print(tick)
	ravg2 = np.average(json_array[i:i+3][0]['heartbeat'])

	# If anxiety AND not exercising AND has new withdrawal
	if ravg2 > avg10 and tick['steps'] < 14 and not withdrawal:
		doc_ref.update({
		    u'hhAssistance': True,
		    u'withdrawalTime': (date.today().strftime('%d/%m/%Y') + ' ' + tick['timestamp'])
		})
		print('updated')
		# update withdrawal flag
		withdrawal = doc_ref.get().to_dict()['hhAssistance']