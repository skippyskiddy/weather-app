<template>
  <div id="app" class="center">
    <h1 class="header">Wanna know the weather, anywhere?</h1>
    <input v-model="location" type="text" placeholder="Enter a location" class="input">
    <button @click="fetchWeather">Get Weather</button>
    <div v-if="weatherData">
      <h2>{{ weatherData.location }}</h2>
      <p>Local time: {{ weatherData.local_time }}</p>
      <p>Temperature: {{ weatherData.temperature }}</p>
      <p>Condition: {{ weatherData.condition }} ({{ weatherData.description }})</p>
    </div>
    <p v-if="errorMessage">{{ errorMessage }}</p>
  </div>
</template>

<script setup lang="ts">
import axios from 'axios';
import { ref } from 'vue';

type WeatherData = {
  location: string;
    local_time: string;
    temperature: number;
    condition: string;
    description: string;
}

const weatherData = ref<WeatherData | null>(null);
const location = ref('')
const errorMessage = ref('');

const fetchWeather = async () => {
  try {
        const response = await axios.get<WeatherData>(`http://127.0.0.1:5000/weather?location=${location.value}`);
        weatherData.value = response.data;
        errorMessage.value = '';
      } catch (error) {
        if (error instanceof Error) {
          weatherData.value = null
          errorMessage.value = error.message;
        } else {
          throw error;
        }
      }
}
</script>

<style>
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

.header {
  margin-bottom: 20px;
}

.input {
  margin-bottom: 20px;
}
</style>
