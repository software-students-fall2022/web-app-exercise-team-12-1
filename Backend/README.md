##### Backend
- User can add, delete, edit and search it's events.


### Prerequisites
Below noted things you need to install to run this project in your system

- pip install flask
- pip install pymongo

- Install mongoDB
- brew services start mongodb-community@6.0
  
### To Setup
Clone or download this repository

1. `cd ./backend`

### To Run
To run node server
1. `python server.js`


## Overview
Listening on localhost:5000

## Data Model

The application will store Events

* user can have multiple events in dashboard
* each event can have multiple infomation


Event:

```javascript
{
    eventSchema = new mongoose.Schema({
        name:{type: String},
        description: {type: String},
        status: {type: String},
        time: {type: String},
        date:{type: String},
    });
}
```

