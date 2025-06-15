<template>
  <div class="wrapper">
    <!-- Navbar -->
    <nav class="main-header navbar navbar-expand navbar-white navbar-light" v-if="isAuthenticated">
      <ul class="navbar-nav">
        <li class="nav-item">
          <a class="nav-link" data-widget="pushmenu" href="#" role="button">
            <i class="fas fa-bars"></i>
          </a>
        </li>
      </ul>
      
      <ul class="navbar-nav ml-auto">
        <li class="nav-item">
          <a class="nav-link" @click="logout" href="#" role="button">
            <i class="fas fa-sign-out-alt"></i> Cerrar Sesión
          </a>
        </li>
      </ul>
    </nav>

    <!-- Main Sidebar -->
    <aside class="main-sidebar sidebar-dark-primary elevation-4" v-if="isAuthenticated">
      <router-link to="/" class="brand-link">
        <span class="brand-text font-weight-light">Restaurant App</span>
      </router-link>

      <div class="sidebar">
        <nav class="mt-2">
          <ul class="nav nav-pills nav-sidebar flex-column" data-widget="treeview" role="menu">
            <li class="nav-item">
              <router-link to="/" class="nav-link">
                <i class="nav-icon fas fa-home"></i>
                <p>Inicio</p>
              </router-link>
            </li>
            
            <li class="nav-item" v-if="isAdmin">
              <router-link to="/products" class="nav-link">
                <i class="nav-icon fas fa-hamburger"></i>
                <p>Productos</p>
              </router-link>
            </li>
            
            <li class="nav-item" v-if="isAdmin">
              <router-link to="/ingredients" class="nav-link">
                <i class="nav-icon fas fa-pepper-hot"></i>
                <p>Ingredientes</p>
              </router-link>
            </li>
            
            <li class="nav-item">
              <router-link to="/orders" class="nav-link">
                <i class="nav-icon fas fa-clipboard-list"></i>
                <p>Órdenes</p>
              </router-link>
            </li>
            
            <li class="nav-item">
              <router-link to="/cart" class="nav-link">
                <i class="nav-icon fas fa-shopping-cart"></i>
                <p>
                  Carrito
                  <span class="badge badge-info right" v-if="cart.length">
                    {{ cart.length }}
                  </span>
                </p>
              </router-link>
            </li>
          </ul>
        </nav>
      </div>
    </aside>

    <!-- Content -->
    <div :class="{'content-wrapper': isAuthenticated}">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'App',
  setup() {
    const store = useStore()
    const router = useRouter()
    
    const isAuthenticated = computed(() => store.getters.isAuthenticated)
    const isAdmin = computed(() => store.getters.isAdmin)
    const cart = computed(() => store.state.cart)
    
    const logout = () => {
      store.commit('clearAuth')
      router.push('/login')
    }
    
    return {
      isAuthenticated,
      isAdmin,
      cart,
      logout
    }
  }
}
</script>

<style>
@import 'admin-lte/dist/css/adminlte.min.css';
@import '@fortawesome/fontawesome-free/css/all.min.css';

.content-wrapper {
  min-height: 100vh;
}
</style>
