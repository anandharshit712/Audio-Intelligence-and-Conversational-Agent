const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const authRoutes = require('./auth');

// const cors = require('cors');

// const corsOptions = {
//   origin: 'https://apps.beamhash.com:3000', // Allow only the HTTPS version
//   methods: 'GET,POST',
//   allowedHeaders: 'Content-Type',
// };

// app.use(cors(corsOptions));


const app = express();
const PORT = 3000;

const mysql = require('mysql');

// Create a MySQL connection
const connection = mysql.createConnection({
  host: '0.0.0.0',  // Use 127.0.0.1 instead of ::1
  user: 'root',
  password: 'admin',
  database: 'login_audio_app',
});

connection.connect((err) => {
  if (err) {
    console.error('Error connecting to MySQL: ' + err.stack);
    return;
  }
  console.log('Connected to MySQL as id ' + connection.threadId);
});

// Middleware to parse JSON and serve static files
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public'))); // Serve static files
app.use(express.json());

// Mount the auth routes
app.use('/auth', authRoutes);

// Start the server
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
 // console.log(`Server running at https://apps.beamhash.com:${PORT}`);
  //console.log(`Server running at https://apps.beamhash.com`)
  
});
