##### Backend
- API to register and login user.
- API using which loged in user can add, edit and update it's event.


### Prerequisites
Below noted things you need to install to run this project in your system

- pip install flask
- pip install flask_mongoengine

### To Setup
Clone or download this repository

1. `cd ./backend`

### To Run
To run node server
1. `python server.js`


## Overview
Two Schema, one for user info, the other for user's events

## Data Model

The application will store Events

* users can have multiple events in dashboard
* each event can have multiple infomation



Course:

```javascript
{
    eventSchema = new mongoose.Schema({
        name:{type: String},
        description: {type: String},
        status: {type: String},
        time: {type: String},
        location: {type: String}
    });
}
```

