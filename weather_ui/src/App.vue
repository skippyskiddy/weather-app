<template>
  <!-- The main application container -->
  <div id="app" class="center">
    <!-- The main application header -->
    <h1 class="header">Wanna know the weather, anywhere?</h1>
    <!-- The text input for the location, bound to the location variable -->
    <input v-model="location" type="text" placeholder="Enter a location" class="input">
    <!-- The button that triggers the fetchWeather function -->
    <button @click="fetchWeather">Get Weather</button>
    <!-- Conditional rendering of the weather data if it exists -->
    <div v-if="weatherData">
      <h2>{{ weatherData.location }}</h2>
      <p>Local time: {{ weatherData.local_time }}</p>
      <p>Temperature: {{ weatherData.temperature }}</p>
      <p>Condition: {{ weatherData.condition }} ({{ weatherData.description }})</p>
    </div>
    <!-- Conditional rendering of the error message if it exists -->
    <p v-if="errorMessage">{{ errorMessage }}</p>
  </div>
</template>

<script setup lang="ts">
// Importing required modules
import axios from 'axios';
import { ref } from 'vue';

// Defining the structure of the weather data
type WeatherData = {
  location: string;
  local_time: string;
  temperature: number;
  condition: string;
  description: string;
}

// Setting up reactive variables
const weatherData = ref<WeatherData | null>(null);
const location = ref('')
const errorMessage = ref('');

// Function to fetch the weather data for the given location
const fetchWeather = async () => {
  try {
    // Making a GET request to the weather API
    const response = await axios.get<WeatherData>(`http://127.0.0.1:5000/weather?location=${location.value}`);
    // Storing the returned data
    weatherData.value = response.data;
    // Clearing any previous error message
    errorMessage.value = '';
  } catch (error) {
    // If an error occurred, clear the weather data and store the error message
    if (error instanceof Error) {
      weatherData.value = null
      errorMessage.value = error.message;
    } else {
      // If the error is not an instance of Error, re-throw it
      throw error;
    }
  }
}
</script>

<style>
/* Centering the content in the main application container */
#app {
  text-align: center;
  margin-top: 60px;
}

.center {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

/* Adding a bottom margin to the header */
.header {
  margin-bottom: 20px;
}

/* Adding a bottom margin to the input */
.input {
  margin-bottom: 20px;
}
</style>
