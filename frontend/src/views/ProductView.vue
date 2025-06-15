<template>
  <div class="content-header">
    <div class="container-fluid">
      <div class="row mb-2">
        <div class="col-sm-6">
          <h1 class="m-0">Productos</h1>
        </div>
      </div>
    </div>
  </div>

  <div class="content">
    <div class="container-fluid">
      <div class="row">
        <!-- Lista de Productos -->
        <div class="col-md-4">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">Selecciona un Producto</h3>
            </div>
            <div class="card-body">
              <div class="list-group">
                <a href="#" 
                   v-for="product in products" 
                   :key="product.id"
                   class="list-group-item list-group-item-action"
                   :class="{ active: selectedProduct?.id === product.id }"
                   @click.prevent="selectProduct(product)">
                  <div class="d-flex w-100 justify-content-between">
                    <h5 class="mb-1">{{ product.name }}</h5>
                    <small>${{ product.base_price }}</small>
                  </div>
                  <p class="mb-1">{{ product.description }}</p>
                </a>
              </div>
            </div>
          </div>
        </div>

        <!-- Área de Ingredientes -->
        <div class="col-md-8" v-if="selectedProduct">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">Personaliza tu {{ selectedProduct.name }}</h3>
            </div>
            <div class="card-body">
              <div class="row">
                <!-- Ingredientes Disponibles -->
                <div class="col-md-6">
                  <h4>Ingredientes Disponibles</h4>
                  <VueDraggable
                    class="list-group"
                    :list="availableIngredients"
                    :group="{ name: 'ingredients', pull: 'clone', put: false }"
                    :clone="cloneIngredient"
                    item-key="id">
                    <template #item="{ element }">
                      <div class="list-group-item">
                        <div class="d-flex w-100 justify-content-between">
                          <h6 class="mb-1">{{ element.name }}</h6>
                          <small>${{ element.price }}</small>
                        </div>
                        <small>{{ element.description }}</small>
                      </div>
                    </template>
                  </VueDraggable>
                </div>

                <!-- Ingredientes Seleccionados -->
                <div class="col-md-6">
                  <h4>Ingredientes Seleccionados</h4>
                  <VueDraggable
                    class="list-group"
                    v-model="selectedIngredients"
                    group="ingredients"
                    item-key="id">
                    <template #item="{ element }">
                      <div class="list-group-item">
                        <div class="d-flex w-100 justify-content-between align-items-center">
                          <div>
                            <h6 class="mb-1">{{ element.name }}</h6>
                            <small>${{ element.price }}</small>
                          </div>
                          <div class="btn-group">
                            <button class="btn btn-sm btn-outline-secondary"
                                    @click="decrementQuantity(element)"
                                    :disabled="element.quantity <= 1">
                              <i class="fas fa-minus"></i>
                            </button>
                            <span class="btn btn-sm">{{ element.quantity }}</span>
                            <button class="btn btn-sm btn-outline-secondary"
                                    @click="incrementQuantity(element)"
                                    :disabled="element.quantity >= maxQuantity">
                              <i class="fas fa-plus"></i>
                            </button>
                            <button class="btn btn-sm btn-outline-danger"
                                    @click="removeIngredient(element)">
                              <i class="fas fa-trash"></i>
                            </button>
                          </div>
                        </div>
                      </div>
                    </template>
                  </VueDraggable>

                  <!-- Total y Botón de Agregar al Carrito -->
                  <div class="mt-4">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                      <h5>Total:</h5>
                      <h5>${{ total }}</h5>
                    </div>
                    <button class="btn btn-primary btn-block"
                            @click="addToCart"
                            :disabled="!selectedProduct || selectedIngredients.length === 0">
                      Agregar al Carrito
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { VueDraggable } from 'vue-draggable-next'

export default {
  name: 'ProductView',
  components: {
    VueDraggable
  },
  
  setup() {
    const store = useStore()
    const selectedProduct = ref(null)
    const selectedIngredients = ref([])
    const maxQuantity = 5
    
    const products = computed(() => store.state.products)
    const availableIngredients = computed(() => {
      if (!selectedProduct.value) return []
      return selectedProduct.value.available_ingredients || []
    })
    
    const total = computed(() => {
      if (!selectedProduct.value) return 0
      const basePrice = selectedProduct.value.base_price
      const ingredientsTotal = selectedIngredients.value.reduce(
        (sum, ing) => sum + (ing.price * ing.quantity),
        0
      )
      return basePrice + ingredientsTotal
    })
    
    const selectProduct = (product) => {
      selectedProduct.value = product
      selectedIngredients.value = []
    }
    
    const cloneIngredient = (ingredient) => {
      return {
        ...ingredient,
        quantity: 1
      }
    }
    
    const incrementQuantity = (ingredient) => {
      if (ingredient.quantity < maxQuantity) {
        ingredient.quantity++
      }
    }
    
    const decrementQuantity = (ingredient) => {
      if (ingredient.quantity > 1) {
        ingredient.quantity--
      }
    }
    
    const removeIngredient = (ingredient) => {
      const index = selectedIngredients.value.indexOf(ingredient)
      if (index > -1) {
        selectedIngredients.value.splice(index, 1)
      }
    }
    
    const addToCart = () => {
      store.commit('addToCart', {
        product: selectedProduct.value,
        quantity: 1,
        selectedIngredients: [...selectedIngredients.value]
      })
      selectedProduct.value = null
      selectedIngredients.value = []
    }
    
    // Cargar productos al montar el componente
    store.dispatch('fetchProducts')
    
    return {
      products,
      selectedProduct,
      availableIngredients,
      selectedIngredients,
      maxQuantity,
      total,
      selectProduct,
      cloneIngredient,
      incrementQuantity,
      decrementQuantity,
      removeIngredient,
      addToCart
    }
  }
}
</script>

<style scoped>
.list-group {
  min-height: 200px;
  padding: 1rem;
  border: 2px dashed #dee2e6;
  border-radius: 0.25rem;
}

.list-group-item {
  cursor: move;
  margin-bottom: 0.5rem;
}

.list-group-item:last-child {
  margin-bottom: 0;
}
</style> 