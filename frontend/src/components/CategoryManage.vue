<template>
  <div>
    <h2>Category Management</h2>
    <input
      type="text"
      v-model="searchQuery"
      placeholder="Search Categories"
      @input="filterCategories"
    />

    <form @submit.prevent="addCategory">
      <input
        type="text"
        v-model="newCategoryName"
        placeholder="New Category Name"
        required
      />
      <button type="submit">Add Category</button>
    </form>

    <table v-if="filteredCategories.length > 0">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="category in filteredCategories" :key="category.id">
          <td>{{ category.id }}</td>
          <td>{{ category.name }}</td>
        </tr>
      </tbody>
    </table>

    <div v-else>
      <p>no categories found</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      categories: [],
      filteredCategories: [],
      newCategoryName: "",
    };
  },
  mounted() {
    this.loadCategories();
  },
  methods: {
    async loadCategories() {
      try {
        const access_token = localStorage.getItem("access_token");
        const response = await axios.get("/api/categories", {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        });
        this.categories = response.data;
        this.filteredCategories = this.categories;
      } catch (error) {
        console.error("Error loading categories:", error);
      }
    },
    filterCategories() {
      const query = this.searchQuery.toLowerCase();
      this.filteredCategories = this.categories.filter((category) =>
        category.name.toLowerCase().includes(query)
      );
    },
    async addCategory() {
      if (!this.newCategoryName) return;

      try {
        const access_token = localStorage.getItem("access_token");
        const response = await axios.post(
          "/api/categories",
          {
            name: this.newCategoryName,
          },
          {
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
          }
        );
        this.categories.push(response.data);
        this.filteredCategories.push(response.data);
        this.newCategoryName = "";
        this.loadCategories();
      } catch (error) {
        console.error("Error adding category:", error);
      }
    },
  },
};
</script>
