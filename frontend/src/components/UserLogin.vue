<template>
  <div>
    <h2>Login</h2>
    <form @submit.prevent="loginUser">
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit">Login</button>
    </form>
    <div v-if="errorMessage">{{ errorMessage }}</div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      username: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    async loginUser() {
      try {
        const response = await axios.post("/login", {
          username: this.username,
          password: this.password,
        });
        // Handle successful login (e.g., store token, redirect)
        const { access_token, user_info } = response.data;
        localStorage.setItem("access_token", access_token);
        localStorage.setItem("user_info", JSON.stringify(user_info));

        if (user_info.role === "admin") {
          this.$router.push("/admin_dashboard");
        } else {
          this.$router.push("/user_dashboard");
        }
      } catch (error) {
        this.errorMessage = error.response.data.message || "Login failed.";
      }
    },
  },
};
</script>

<style scoped></style>
