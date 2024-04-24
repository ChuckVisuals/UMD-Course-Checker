const express = require("express");
const axios = require("axios");
const cron = require("node-cron");

const app = express();
const port = process.env.PORT || 5000;

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

// Function to make API calls based on data from the database
const performApiCalls = async () => {
  // Fetch data from the database (modify as per your database logic)
  const apiLinks = await fetchDataFromDatabase();

  // Execute separate API calls for each link
  for (const apiLink of apiLinks) {
    await makeApiCall(apiLink);
  }
};

// Schedule API calls every hour
cron.schedule("0 * * * *", async () => {
  console.log("Running scheduled API calls...");
  await performApiCalls();
});

// Function to fetch data from the database (modify as per your database logic)
const fetchDataFromDatabase = async () => {
  // Implement logic to fetch data from your database
  // Return an array of API links
  // Example: return ['https://api.example.com/endpoint1', 'https://api.example.com/endpoint2'];
};

// Function to make API call
const makeApiCall = async (apiLink) => {
  try {
    const response = await axios.get(apiLink);
    console.log("API Response for", apiLink, ":", response.data);
  } catch (error) {
    console.error("Error making API call for", apiLink, ":", error.message);
  }
};

// Serve your website here (add your routes, middleware, etc.)
app.get("/", (req, res) => {
  res.send("Hello, this is your website!");
});
