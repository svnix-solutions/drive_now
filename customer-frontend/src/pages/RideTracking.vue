<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center">
            <Button
              variant="ghost"
              @click="$router.back()"
              class="mr-3"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
              </svg>
            </Button>
            <h1 class="text-xl font-semibold text-gray-900">Track Ride</h1>
          </div>
          <div class="flex items-center space-x-3">
            <Badge 
              v-if="ride"
              :variant="getRideStatusVariant(ride.status)"
              :label="ride.status"
            />
          </div>
        </div>
      </div>
    </div>

    <div v-if="isLoading" class="flex items-center justify-center py-12">
      <LoadingIndicator />
      <span class="ml-3 text-gray-600">Loading ride details...</span>
    </div>

    <div v-else-if="ride" class="pb-8">
      <!-- Map Section -->
      <div class="bg-white">
        <div class="h-96 bg-gray-100 flex items-center justify-center">
          <div class="text-center">
            <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
            </svg>
            <p class="text-gray-500">Live tracking map will appear here</p>
          </div>
        </div>
      </div>

      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <!-- Main Content -->
          <div class="lg:col-span-2 space-y-6">
            <!-- Ride Progress -->
            <Card class="p-6">
              <h2 class="text-lg font-semibold text-gray-900 mb-4">Ride Progress</h2>
              <div class="space-y-4">
                <!-- Progress Steps -->
                <div class="flex items-center space-x-4">
                  <div class="flex flex-col items-center">
                    <div 
                      class="w-8 h-8 rounded-full flex items-center justify-center text-white text-sm"
                      :class="getStepClass('confirmed')"
                    >
                      <svg v-if="isStepCompleted('confirmed')" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                      </svg>
                      <span v-else>1</span>
                    </div>
                    <div class="text-xs text-center mt-2">
                      <div class="font-medium">Confirmed</div>
                      <div class="text-gray-500">{{ formatTime(ride.creation) }}</div>
                    </div>
                  </div>

                  <div class="flex-1 h-0.5 bg-gray-200">
                    <div 
                      class="h-full bg-blue-600 transition-all duration-500"
                      :style="{ width: getProgressWidth('pickup') }"
                    ></div>
                  </div>

                  <div class="flex flex-col items-center">
                    <div 
                      class="w-8 h-8 rounded-full flex items-center justify-center text-white text-sm"
                      :class="getStepClass('pickup')"
                    >
                      <svg v-if="isStepCompleted('pickup')" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                      </svg>
                      <span v-else>2</span>
                    </div>
                    <div class="text-xs text-center mt-2">
                      <div class="font-medium">Picked Up</div>
                      <div class="text-gray-500">{{ formatTime(ride.pickup_time) }}</div>
                    </div>
                  </div>

                  <div class="flex-1 h-0.5 bg-gray-200">
                    <div 
                      class="h-full bg-blue-600 transition-all duration-500"
                      :style="{ width: getProgressWidth('completed') }"
                    ></div>
                  </div>

                  <div class="flex flex-col items-center">
                    <div 
                      class="w-8 h-8 rounded-full flex items-center justify-center text-white text-sm"
                      :class="getStepClass('completed')"
                    >
                      <svg v-if="isStepCompleted('completed')" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                      </svg>
                      <span v-else>3</span>
                    </div>
                    <div class="text-xs text-center mt-2">
                      <div class="font-medium">Completed</div>
                      <div class="text-gray-500">{{ formatTime(ride.drop_off_time) }}</div>
                    </div>
                  </div>
                </div>
              </div>
            </Card>

            <!-- Route Details -->
            <Card class="p-6">
              <h2 class="text-lg font-semibold text-gray-900 mb-4">Route Details</h2>
              <div class="space-y-4">
                <div class="flex items-start">
                  <div class="flex-shrink-0 w-6 flex flex-col items-center">
                    <div class="w-3 h-3 bg-green-500 rounded-full"></div>
                    <div class="w-0.5 h-12 bg-gray-300 mt-1"></div>
                  </div>
                  <div class="ml-3 flex-1">
                    <div class="text-sm font-medium text-gray-900">Pickup Location</div>
                    <div class="text-sm text-gray-600">{{ ride.pickup_address }}</div>
                    <div class="text-xs text-gray-500 mt-1">
                      {{ ride.pickup_time ? 'Picked up at ' + formatTime(ride.pickup_time) : 'Waiting for pickup' }}
                    </div>
                  </div>
                </div>

                <div class="flex items-start">
                  <div class="flex-shrink-0 w-6 flex flex-col items-center">
                    <div class="w-3 h-3 bg-red-500 rounded-full"></div>
                  </div>
                  <div class="ml-3 flex-1">
                    <div class="text-sm font-medium text-gray-900">Drop-off Location</div>
                    <div class="text-sm text-gray-600">{{ ride.drop_off_address }}</div>
                    <div class="text-xs text-gray-500 mt-1">
                      {{ ride.drop_off_time ? 'Dropped at ' + formatTime(ride.drop_off_time) : 'Estimated arrival: ' + estimatedArrival }}
                    </div>
                  </div>
                </div>
              </div>
            </Card>

            <!-- Live Updates -->
            <Card v-if="ride.status === 'In Progress'" class="p-6">
              <h2 class="text-lg font-semibold text-gray-900 mb-4">Live Updates</h2>
              <div class="space-y-3">
                <div
                  v-for="update in liveUpdates"
                  :key="update.id"
                  class="flex items-start space-x-3"
                >
                  <div class="flex-shrink-0 w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                  <div class="flex-1">
                    <div class="text-sm text-gray-900">{{ update.message }}</div>
                    <div class="text-xs text-gray-500">{{ formatTime(update.timestamp) }}</div>
                  </div>
                </div>
              </div>
            </Card>
          </div>

          <!-- Sidebar -->
          <div class="space-y-6">
            <!-- Driver Info -->
            <Card v-if="ride.driver_name" class="p-6">
              <h3 class="text-lg font-semibold text-gray-900 mb-4">Your Driver</h3>
              <div class="text-center">
                <Avatar
                  :label="ride.driver_name"
                  size="xl"
                  class="mx-auto mb-3"
                />
                <h4 class="text-lg font-medium text-gray-900">{{ ride.driver_name }}</h4>
                <div class="flex items-center justify-center mt-1">
                  <svg class="w-4 h-4 text-yellow-400 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                  </svg>
                  <span class="text-sm text-gray-600">{{ ride.driver_rating || 'N/A' }}</span>
                </div>
              </div>

              <div class="mt-4 space-y-2">
                <div class="flex items-center justify-between text-sm">
                  <span class="text-gray-600">Vehicle</span>
                  <span class="font-medium">{{ ride.vehicle_number }}</span>
                </div>
                <div class="flex items-center justify-between text-sm">
                  <span class="text-gray-600">Model</span>
                  <span class="font-medium">{{ ride.vehicle_model || 'N/A' }}</span>
                </div>
              </div>

              <div class="mt-4 space-y-2">
                <Button
                  variant="outline"
                  class="w-full"
                  @click="callDriver"
                >
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                  </svg>
                  Call Driver
                </Button>
                <Button
                  variant="ghost"
                  class="w-full"
                  @click="messageDriver"
                >
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8-1.22 0-2.369-.233-3.409-.668l-1.736.866A1 1 0 016 19.14V17a8.996 8.996 0 01-3-6.717C3 5.578 7.03 2 12 2s9 3.578 9 8z"/>
                  </svg>
                  Message
                </Button>
              </div>
            </Card>

            <!-- Trip Summary -->
            <Card class="p-6">
              <h3 class="text-lg font-semibold text-gray-900 mb-4">Trip Summary</h3>
              <div class="space-y-3">
                <div class="flex items-center justify-between text-sm">
                  <span class="text-gray-600">Distance</span>
                  <span class="font-medium">{{ ride.distance || 'N/A' }} km</span>
                </div>
                <div class="flex items-center justify-between text-sm">
                  <span class="text-gray-600">Duration</span>
                  <span class="font-medium">{{ ride.duration || 'N/A' }} min</span>
                </div>
                <div class="flex items-center justify-between text-sm">
                  <span class="text-gray-600">Vehicle Type</span>
                  <span class="font-medium">{{ ride.vehicle_type }}</span>
                </div>
                <div class="border-t pt-3 flex items-center justify-between">
                  <span class="font-medium text-gray-900">Total Fare</span>
                  <span class="text-lg font-semibold text-gray-900">₹{{ ride.total_amount }}</span>
                </div>
              </div>
            </Card>

            <!-- Actions -->
            <Card v-if="ride.status !== 'Completed' && ride.status !== 'Cancelled'" class="p-6">
              <h3 class="text-lg font-semibold text-gray-900 mb-4">Actions</h3>
              <div class="space-y-2">
                <Button
                  variant="ghost"
                  class="w-full justify-start"
                  @click="shareTrip"
                >
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z"/>
                  </svg>
                  Share Trip
                </Button>
                <Button
                  v-if="ride.status === 'Confirmed'"
                  variant="ghost"
                  class="w-full justify-start text-red-600 hover:text-red-700"
                  @click="cancelRide"
                >
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                  </svg>
                  Cancel Ride
                </Button>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-12">
      <h2 class="text-2xl font-semibold text-gray-900 mb-2">Ride not found</h2>
      <p class="text-gray-600 mb-4">The ride you're looking for doesn't exist.</p>
      <Button @click="$router.push('/')">
        Go to Dashboard
      </Button>
    </div>
  </div>
</template>

<script>
import { createResource } from 'frappe-ui'

export default {
  name: 'RideTracking',
  props: {
    rideId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      ride: null,
      isLoading: true,
      liveUpdates: [],
      estimatedArrival: '15 min',
      refreshInterval: null
    }
  },
  resources: {
    rideDetails() {
      return createResource({
        url: '/api/method/drive_now.api.customer.get_ride_tracking',
        makeParams() {
          return { ride_id: this.rideId }
        },
        auto: true,
        onSuccess(data) {
          this.ride = data.message
          this.isLoading = false
          
          // Update live updates
          if (data.message && data.message.updates) {
            this.liveUpdates = data.message.updates
          }
        },
        onError() {
          this.isLoading = false
        }
      })
    },
    cancelRideResource() {
      return createResource({
        url: '/api/method/drive_now.api.customer.cancel_ride',
        makeParams() {
          return {
            ride_id: this.rideId,
            reason: 'Cancelled by customer'
          }
        },
        onSuccess() {
          this.$resources.rideDetails.reload()
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
    formatTime(timeString) {
      if (!timeString) return 'N/A'
      return new Date(timeString).toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
      })
    },
    isStepCompleted(step) {
      if (!this.ride) return false
      
      switch (step) {
        case 'confirmed':
          return true
        case 'pickup':
          return this.ride.pickup_time || this.ride.status === 'In Progress' || this.ride.status === 'Completed'
        case 'completed':
          return this.ride.status === 'Completed'
        default:
          return false
      }
    },
    getStepClass(step) {
      if (this.isStepCompleted(step)) {
        return 'bg-blue-600'
      } else if (this.isCurrentStep(step)) {
        return 'bg-blue-600'
      } else {
        return 'bg-gray-300'
      }
    },
    isCurrentStep(step) {
      if (!this.ride) return false
      
      switch (step) {
        case 'confirmed':
          return this.ride.status === 'Confirmed' && !this.ride.pickup_time
        case 'pickup':
          return this.ride.status === 'In Progress' && !this.ride.drop_off_time
        case 'completed':
          return false
        default:
          return false
      }
    },
    getProgressWidth(step) {
      if (!this.ride) return '0%'
      
      switch (step) {
        case 'pickup':
          return this.ride.pickup_time || this.ride.status === 'In Progress' || this.ride.status === 'Completed' ? '100%' : '0%'
        case 'completed':
          return this.ride.status === 'Completed' ? '100%' : '0%'
        default:
          return '0%'
      }
    },
    callDriver() {
      if (this.ride && this.ride.driver_phone) {
        window.location.href = `tel:${this.ride.driver_phone}`
      }
    },
    messageDriver() {
      // TODO: Implement messaging functionality
      console.log('Message driver')
    },
    shareTrip() {
      if (navigator.share) {
        navigator.share({
          title: 'Drive Now - Live Trip',
          text: `I'm on a ride from ${this.ride.pickup_address} to ${this.ride.drop_off_address}`,
          url: window.location.href
        })
      } else {
        // Fallback: Copy to clipboard
        navigator.clipboard.writeText(window.location.href)
        // TODO: Show success message
      }
    },
    async cancelRide() {
      if (confirm('Are you sure you want to cancel this ride?')) {
        try {
          await this.$resources.cancelRideResource.submit()
        } catch (error) {
          console.error('Error cancelling ride:', error)
        }
      }
    },
    startLiveTracking() {
      // Refresh ride details every 10 seconds if ride is in progress
      if (this.ride && (this.ride.status === 'Confirmed' || this.ride.status === 'In Progress')) {
        this.refreshInterval = setInterval(() => {
          this.$resources.rideDetails.reload()
        }, 10000)
      }
    }
  },
  watch: {
    ride: {
      handler(newRide) {
        if (newRide) {
          this.startLiveTracking()
        }
      },
      immediate: true
    }
  },
  beforeUnmount() {
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval)
    }
  }
}
</script>