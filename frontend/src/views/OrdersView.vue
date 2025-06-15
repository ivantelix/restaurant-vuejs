<template>
  <div class="content-header">
    <div class="container-fluid">
      <div class="row mb-2">
        <div class="col-sm-6">
          <h1 class="m-0">Órdenes</h1>
        </div>
      </div>
    </div>
  </div>

  <div class="content">
    <div class="container-fluid">
      <div class="row">
        <div class="col-12">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">Lista de Órdenes</h3>
              <div class="card-tools">
                <div class="input-group input-group-sm">
                  <input type="text"
                         v-model="searchQuery"
                         class="form-control"
                         placeholder="Buscar...">
                  <div class="input-group-append">
                    <button class="btn btn-default">
                      <i class="fas fa-search"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div class="card-body p-0">
              <div class="table-responsive">
                <table class="table table-striped">
                  <thead>
                    <tr>
                      <th>#</th>
                      <th>Cliente</th>
                      <th>Estado</th>
                      <th>Total</th>
                      <th>Fecha</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="order in filteredOrders" :key="order.id">
                      <td>{{ order.id }}</td>
                      <td>{{ order.user.username }}</td>
                      <td>
                        <span :class="getStatusBadgeClass(order.status)">
                          {{ getStatusText(order.status) }}
                        </span>
                      </td>
                      <td>${{ order.total }}</td>
                      <td>{{ formatDate(order.created_at) }}</td>
                      <td>
                        <div class="btn-group">
                          <button class="btn btn-sm btn-info"
                                  @click="showOrderDetails(order)">
                            <i class="fas fa-eye"></i>
                          </button>
                          <button v-if="isAdmin && order.status === 'pending'"
                                  class="btn btn-sm btn-success"
                                  @click="updateOrderStatus(order.id, 'accept')">
                            <i class="fas fa-check"></i>
                          </button>
                          <button v-if="isAdmin && order.status === 'pending'"
                                  class="btn btn-sm btn-danger"
                                  @click="updateOrderStatus(order.id, 'reject')">
                            <i class="fas fa-times"></i>
                          </button>
                          <button v-if="isAdmin && order.status === 'accepted'"
                                  class="btn btn-sm btn-primary"
                                  @click="updateOrderStatus(order.id, 'complete')">
                            <i class="fas fa-flag-checkered"></i>
                          </button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Detalles -->
    <div class="modal fade" id="orderDetailsModal" tabindex="-1" role="dialog">
      <div class="modal-dialog modal-lg" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Detalles de la Orden #{{ selectedOrder?.id }}</h5>
            <button type="button" class="close" data-dismiss="modal">
              <span>&times;</span>
            </button>
          </div>
          <div class="modal-body" v-if="selectedOrder">
            <div class="row mb-3">
              <div class="col-md-6">
                <strong>Cliente:</strong> {{ selectedOrder.user.username }}
              </div>
              <div class="col-md-6">
                <strong>Fecha:</strong> {{ formatDate(selectedOrder.created_at) }}
              </div>
            </div>
            
            <div class="table-responsive">
              <table class="table">
                <thead>
                  <tr>
                    <th>Producto</th>
                    <th>Ingredientes</th>
                    <th>Cantidad</th>
                    <th>Precio</th>
                    <th>Subtotal</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in selectedOrder.items" :key="item.id">
                    <td>{{ item.product.name }}</td>
                    <td>
                      <ul class="list-unstyled mb-0">
                        <li v-for="ing in item.selected_ingredients" :key="ing.id">
                          {{ ing.name }} x{{ ing.quantity }}
                        </li>
                      </ul>
                    </td>
                    <td>{{ item.quantity }}</td>
                    <td>${{ item.unit_price }}</td>
                    <td>${{ item.quantity * item.unit_price }}</td>
                  </tr>
                </tbody>
                <tfoot>
                  <tr>
                    <td colspan="4" class="text-right"><strong>Total:</strong></td>
                    <td><strong>${{ selectedOrder.total }}</strong></td>
                  </tr>
                </tfoot>
              </table>
            </div>
            
            <div class="mt-3" v-if="selectedOrder.notes">
              <strong>Notas:</strong>
              <p class="mb-0">{{ selectedOrder.notes }}</p>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">
              Cerrar
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import $ from 'jquery'

export default {
  name: 'OrdersView',
  
  setup() {
    const store = useStore()
    const searchQuery = ref('')
    const selectedOrder = ref(null)
    
    const orders = computed(() => store.state.orders)
    const isAdmin = computed(() => store.getters.isAdmin)
    
    const filteredOrders = computed(() => {
      if (!searchQuery.value) return orders.value
      const query = searchQuery.value.toLowerCase()
      return orders.value.filter(order => 
        order.id.toString().includes(query) ||
        order.user.username.toLowerCase().includes(query) ||
        order.status.toLowerCase().includes(query)
      )
    })
    
    const getStatusBadgeClass = (status) => {
      const classes = {
        pending: 'badge badge-warning',
        accepted: 'badge badge-success',
        rejected: 'badge badge-danger',
        completed: 'badge badge-info'
      }
      return classes[status] || 'badge badge-secondary'
    }
    
    const getStatusText = (status) => {
      const texts = {
        pending: 'Pendiente',
        accepted: 'Aceptado',
        rejected: 'Rechazado',
        completed: 'Completado'
      }
      return texts[status] || status
    }
    
    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleString()
    }
    
    const showOrderDetails = (order) => {
      selectedOrder.value = order
      $('#orderDetailsModal').modal('show')
    }
    
    const updateOrderStatus = async (orderId, action) => {
      try {
        await store.dispatch('updateOrderStatus', { orderId, status: action })
        await store.dispatch('fetchOrders')
      } catch (error) {
        console.error('Error al actualizar el estado:', error)
        // Aquí podrías mostrar un mensaje de error al usuario
      }
    }
    
    onMounted(() => {
      store.dispatch('fetchOrders')
    })
    
    return {
      searchQuery,
      selectedOrder,
      filteredOrders,
      isAdmin,
      getStatusBadgeClass,
      getStatusText,
      formatDate,
      showOrderDetails,
      updateOrderStatus
    }
  }
}
</script>

<style scoped>
.badge {
  font-size: 0.9em;
  padding: 0.4em 0.6em;
}
</style> 