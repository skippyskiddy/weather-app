<template>
  <div id="app" class="center">
    <h1>Weather App</h1>
    <input v-model="location" type="text" placeholder="Enter a location">
    <button @click="fetchWeather">Get Weather</button>
    <div v-if="weatherData">
      <h2>{{ weatherData.location }}</h2>
      <p>Local time: {{ weatherData.local_time }}</p>
      <p>Temperature: {{ weatherData.temperature }}</p>
      <p>Condition: {{ weatherData.condition }} ({{ weatherData.description }})</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',
  data() {
    return {
      location: '',
      weatherData: null,
    };
  },
  methods: {
    async fetchWeather() {
      const response = await axios.get(`http://127.0.0.1:5000/weather?location=${this.location}`);
      this.weatherData = response.data;
    },
  },
};
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
</style>
