<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Welcome Section -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Welcome back!</h1>
        <p class="mt-2 text-lg text-gray-600">Ready for your next ride?</p>
      </div>

      <!-- Quick Actions -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <Card
          class="p-6 cursor-pointer hover:shadow-lg transition-shadow"
          @click="$router.push('/book-ride')"
        >
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-semibold text-gray-900">Book a Ride</h3>
              <p class="text-sm text-gray-500">Find a ride now</p>
            </div>
          </div>
        </Card>

        <Card
          class="p-6 cursor-pointer hover:shadow-lg transition-shadow"
          @click="$router.push('/ride-history')"
        >
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
                <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-semibold text-gray-900">Ride History</h3>
              <p class="text-sm text-gray-500">View past rides</p>
            </div>
          </div>
        </Card>

        <Card
          class="p-6 cursor-pointer hover:shadow-lg transition-shadow"
          @click="$router.push('/profile')"
        >
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center">
                <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-semibold text-gray-900">Profile</h3>
              <p class="text-sm text-gray-500">Manage your account</p>
            </div>
          </div>
        </Card>

        <Card class="p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-10 h-10 bg-yellow-100 rounded-full flex items-center justify-center">
                <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                </svg>
              </div>
            </div>
            <div class="ml-4">
              <h3 class="text-lg font-semibold text-gray-900">₹0</h3>
              <p class="text-sm text-gray-500">Wallet Balance</p>
            </div>
          </div>
        </Card>
      </div>

      <!-- Active Ride Section -->
      <div v-if="activeRide" class="mb-8">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">Active Ride</h2>
        <Card class="p-6">
          <div class="flex items-center justify-between">
            <div class="flex-1">
              <div class="flex items-center mb-2">
                <Badge 
                  :variant="getRideStatusVariant(activeRide.status)"
                  :label="activeRide.status"
                />
              </div>
              <div class="space-y-2">
                <div class="flex items-center text-sm text-gray-600">
                  <div class="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                  {{ activeRide.pickup_address }}
                </div>
                <div class="flex items-center text-sm text-gray-600">
                  <div class="w-3 h-3 bg-red-500 rounded-full mr-2"></div>
                  {{ activeRide.drop_off_address }}
                </div>
              </div>
            </div>
            <div class="flex space-x-3">
              <Button
                variant="subtle"
                @click="trackRide(activeRide.name)"
              >
                Track Ride
              </Button>
              <Button
                v-if="activeRide.status === 'Confirmed'"
                variant="subtle"
                theme="red"
                @click="cancelRide(activeRide.name)"
              >
                Cancel
              </Button>
            </div>
          </div>
        </Card>
      </div>

      <!-- Recent Rides -->
      <div>
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-semibold text-gray-900">Recent Rides</h2>
          <Button
            variant="ghost"
            @click="$router.push('/ride-history')"
          >
            View All
          </Button>
        </div>

        <div v-if="recentRides.length > 0" class="space-y-4">
          <Card
            v-for="ride in recentRides.slice(0, 3)"
            :key="ride.name"
            class="p-6"
          >
            <div class="flex items-center justify-between">
              <div class="flex-1">
                <div class="flex items-center justify-between mb-2">
                  <Badge 
                    :variant="getRideStatusVariant(ride.status)"
                    :label="ride.status"
                  />
                  <span class="text-sm font-medium text-gray-900">₹{{ ride.total_amount }}</span>
                </div>
                <div class="space-y-1">
                  <div class="flex items-center text-sm text-gray-600">
                    <div class="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                    {{ ride.pickup_address }}
                  </div>
                  <div class="flex items-center text-sm text-gray-600">
                    <div class="w-2 h-2 bg-red-500 rounded-full mr-2"></div>
                    {{ ride.drop_off_address }}
                  </div>
                </div>
                <p class="text-xs text-gray-500 mt-2">
                  {{ formatDate(ride.creation) }}
                </p>
              </div>
            </div>
          </Card>
        </div>

        <div v-else class="text-center py-12">
          <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">No rides yet</h3>
          <p class="text-gray-500 mb-4">Book your first ride to get started</p>
          <Button @click="$router.push('/book-ride')">
            Book Your First Ride
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { createResource } from 'frappe-ui'

export default {
  name: 'Dashboard',
  data() {
    return {
      activeRide: null,
      recentRides: [],
    }
  },
  resources: {
    activeRide() {
      return createResource({
        url: '/api/method/drive_now.api.customer.get_active_ride',
        auto: true,
        onSuccess(data) {
          this.activeRide = data.message
        }
      })
    },
    recentRides() {
      return createResource({
        url: '/api/method/drive_now.api.customer.get_ride_history',
        params: { limit: 5 },
        auto: true,
        onSuccess(data) {
          this.recentRides = data.message || []
        }
      })
    }
  },
  methods: {
    getRideStatusVariant(status) {
      const variants = {
        'Draft': 'subtle',
        'Confirmed': 'solid',
        'In Progress': 'solid',
        'Completed': 'solid',
        'Cancelled': 'subtle'
      }
      return variants[status] || 'subtle'
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },
    trackRide(rideId) {
      this.$router.push(`/ride-tracking/${rideId}`)
    },
    async cancelRide(rideId) {
      if (confirm('Are you sure you want to cancel this ride?')) {
        try {
          // TODO: Implement cancel ride API call
          console.log('Cancelling ride:', rideId)
          // Refresh active ride data
          this.$resources.activeRide.reload()
        } catch (error) {
          console.error('Error cancelling ride:', error)
        }
      }
    }
  }
}
</script>