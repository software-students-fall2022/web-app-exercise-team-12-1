##### Backend
- API to register and login user.
- API using which loged in user can add, edit and update it's event.


### Prerequisites
Below noted things you need to install to run this project in your system

- Node.js
- NPM
- MongoDB

### To Setup
Clone or download this repository

1. `cd ./backend`
2. `npm install`

### To Run
To run node server
1. `nodemon server.js`


## Overview
Two Schema, one for user info, the other for user's events

## Data Model

The application will store Users, and Users' Events

* users can have multiple events in dashboard
* each event can have multiple infomation


User:

```javascript
{
    userSchema = new mongoose.Schema({
        username: {type: String, required: true},
        password: {type: String},
        events:  [{ type: mongoose.Schema.Types.ObjectId, ref: 'event' }]
    });
}
```

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

