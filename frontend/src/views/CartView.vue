<template>
  <div class="content-header">
    <div class="container-fluid">
      <div class="row mb-2">
        <div class="col-sm-6">
          <h1 class="m-0">Carrito de Compras</h1>
        </div>
      </div>
    </div>
  </div>

  <div class="content">
    <div class="container-fluid">
      <div class="row">
        <div class="col-md-8">
          <!-- Lista de Items -->
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">Items en el Carrito</h3>
            </div>
            <div class="card-body p-0">
              <div class="table-responsive">
                <table class="table table-striped">
                  <thead>
                    <tr>
                      <th>Producto</th>
                      <th>Ingredientes</th>
                      <th>Cantidad</th>
                      <th>Precio</th>
                      <th>Subtotal</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(item, index) in cart" :key="index">
                      <td>{{ item.product.name }}</td>
                      <td>
                        <ul class="list-unstyled mb-0">
                          <li v-for="ing in item.selectedIngredients" :key="ing.id">
                            {{ ing.name }} x{{ ing.quantity }}
                          </li>
                        </ul>
                      </td>
                      <td>
                        <div class="btn-group">
                          <button class="btn btn-sm btn-outline-secondary"
                                  @click="decrementQuantity(index)"
                                  :disabled="item.quantity <= 1">
                            <i class="fas fa-minus"></i>
                          </button>
                          <span class="btn btn-sm">{{ item.quantity }}</span>
                          <button class="btn btn-sm btn-outline-secondary"
                                  @click="incrementQuantity(index)">
                            <i class="fas fa-plus"></i>
                          </button>
                        </div>
                      </td>
                      <td>${{ calculateItemPrice(item) }}</td>
                      <td>${{ calculateItemSubtotal(item) }}</td>
                      <td>
                        <button class="btn btn-sm btn-danger"
                                @click="removeItem(index)">
                          <i class="fas fa-trash"></i>
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <!-- Resumen del Pedido -->
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">Resumen del Pedido</h3>
            </div>
            <div class="card-body">
              <div class="d-flex justify-content-between mb-3">
                <h5>Total:</h5>
                <h5>${{ cartTotal }}</h5>
              </div>
              <div class="form-group">
                <label for="notes">Notas adicionales:</label>
                <textarea id="notes"
                         v-model="notes"
                         class="form-control"
                         rows="3"
                         placeholder="Instrucciones especiales..."></textarea>
              </div>
              <button class="btn btn-primary btn-block"
                      @click="placeOrder"
                      :disabled="cart.length === 0 || isProcessing">
                {{ isProcessing ? 'Procesando...' : 'Realizar Pedido' }}
              </button>
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
import { useRouter } from 'vue-router'

export default {
  name: 'CartView',
  
  setup() {
    const store = useStore()
    const router = useRouter()
    const notes = ref('')
    const isProcessing = ref(false)
    
    const cart = computed(() => store.state.cart)
    const cartTotal = computed(() => store.getters.cartTotal)
    
    const calculateItemPrice = (item) => {
      const basePrice = item.product.base_price
      const ingredientsPrice = item.selectedIngredients.reduce(
        (sum, ing) => sum + (ing.price * ing.quantity),
        0
      )
      return basePrice + ingredientsPrice
    }
    
    const calculateItemSubtotal = (item) => {
      return calculateItemPrice(item) * item.quantity
    }
    
    const incrementQuantity = (index) => {
      const item = cart.value[index]
      item.quantity++
    }
    
    const decrementQuantity = (index) => {
      const item = cart.value[index]
      if (item.quantity > 1) {
        item.quantity--
      }
    }
    
    const removeItem = (index) => {
      store.commit('removeFromCart', index)
    }
    
    const placeOrder = async () => {
      try {
        isProcessing.value = true
        await store.dispatch('createOrder', { notes: notes.value })
        router.push('/orders')
      } catch (error) {
        console.error('Error al crear la orden:', error)
        // Aquí podrías mostrar un mensaje de error al usuario
      } finally {
        isProcessing.value = false
      }
    }
    
    return {
      cart,
      cartTotal,
      notes,
      isProcessing,
      calculateItemPrice,
      calculateItemSubtotal,
      incrementQuantity,
      decrementQuantity,
      removeItem,
      placeOrder
    }
  }
}
</script> 