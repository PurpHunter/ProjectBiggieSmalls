
Project structure
AI Files/
├── central_server/
│   └── models/                    # Stores exported global model
├── federated_learning/
│   ├── export_model.py            # Export global model to file
│   ├── federated_server.py        # Central Flask server
│   └── build_vectorizer.py        # Optional: build vectorizer for clients
├── devices/
│   ├── device_A/
│   │   ├── client.py              # Device A client script
│   │   ├── crew_A.csv             # Local dataset
│   │   └── global_vectorizer.joblib
│   ├── device_B/
│   │   ├── client.py              # Device B client script
│   │   ├── crew_B.csv             # Local dataset
│   │   └── global_vectorizer.joblib
│   └── device_C/
│       ├── client.py              # Device C client script
│       ├── crew_C.csv             # Local dataset
│       └── global_vectorizer.joblib
├── requirements.txt               # All dependencies
└── README.md

Requirement
pip install -r requirements.txt

start central server
python federated_learning/federated_server.py


test server if needed
curl http://127.0.0.1:5000/global_model
 
 should return
 {"coef": null, "intercept": null, "n_samples": 0}


 
 Prepare Each Device

Ensure each device folder has:

client.py

Its CSV (crew_A/B/C.csv)

global_vectorizer.joblib

Paths inside client.py are relative to the script using Path(__file__).resolve().parent.



Device A:
python -m devices.device_A.client

Device B:
python -m devices.device_B.client

Device C:
python -m devices.device_C.client


Each client will:

Train on its local data

Compute a federated update

Send it to the central server

You should see messages like:

Local update sent.


Verify Federated Updates

On the server terminal, you should see POST requests:

127.0.0.1 - - [21:13:27] "POST /federated_update HTTP/1.1" 200 -

Export the Global Model

After clients have sent updates:

python federated_learning/export_model.py


Model saved to:

central_server/models/mental_health_classifier.joblib

Use the Model in AI Scripts
import joblib

model = joblib.load("central_server/models/mental_health_classifier.joblib")
# Use model.predict() or other operations



Updating / Retraining

Add new data to device CSVs

Run device clients again, updates sent to server

Export the updated global model

Repeat as needed





Federated learning structure for new memebers


+----------------+          +------------------+          +----------------+
| Device A       |          | Device B         |          | Device C       |
| (crew_A.csv)   |          | (crew_B.csv)     |          | (crew_C.csv)   |
| client.py      |          | client.py        |          | client.py      |
+----------------+          +------------------+          +----------------+
         |                         |                          |
         | Train local model        | Train local model        | Train local model
         | Compute federated update | Compute federated update | Compute federated update
         v                         v                          v
                 +-----------------------------------------+
                 |           Central Server                 |
                 |  federated_server.py (Flask API)        |
                 |  Stores/aggregates global model         |
                 +-----------------------------------------+
                                    |
                                    | Updates global model weights
                                    v
                     +-------------------------------+
                     | Export Global Model           |
                     | export_model.py               |
                     | Saves: mental_health_classifier.joblib |
                     +-------------------------------+
                                    |
                                    v
                     +-------------------------------+
                     | AI Applications / Scripts     |
                     | Load model with joblib        |
                     | Use for predictions or combined |
                     +-------------------------------+
