<template>
  <div class="min-h-screen bg-gray-50 py-4 md:py-8">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="mb-4 md:mb-8">
        <h1 class="text-2xl md:text-3xl font-bold text-gray-900">Book a Ride</h1>
        <p class="mt-1 md:mt-2 text-base md:text-lg text-gray-600">Choose your pickup and destination</p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 md:gap-8">
        <!-- Booking Form -->
        <div class="space-y-4 md:space-y-6 order-2 lg:order-1">
          <Card class="p-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-6">Trip Details</h2>
            
            <form @submit.prevent="searchRides" class="space-y-6">
              <!-- Pickup Location -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Pickup Location
                </label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <div class="w-3 h-3 bg-green-500 rounded-full"></div>
                  </div>
                  <Input
                    v-model="pickupLocation"
                    placeholder="Enter pickup location"
                    class="pl-10"
                    @input="searchPickupLocations"
                  />
                </div>
                <!-- Pickup suggestions dropdown -->
                <div v-if="pickupSuggestions.length > 0" class="mt-1 bg-white border border-gray-300 rounded-md shadow-lg max-h-60 overflow-auto">
                  <div
                    v-for="suggestion in pickupSuggestions"
                    :key="suggestion.id"
                    @click="selectPickupLocation(suggestion)"
                    class="px-4 py-2 hover:bg-gray-50 cursor-pointer border-b border-gray-100 last:border-b-0"
                  >
                    <div class="font-medium text-gray-900">{{ suggestion.name }}</div>
                    <div class="text-sm text-gray-500">{{ suggestion.address }}</div>
                  </div>
                </div>
              </div>

              <!-- Destination Location -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Destination
                </label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <div class="w-3 h-3 bg-red-500 rounded-full"></div>
                  </div>
                  <Input
                    v-model="destinationLocation"
                    placeholder="Where are you going?"
                    class="pl-10"
                    @input="searchDestinationLocations"
                  />
                </div>
                <!-- Destination suggestions dropdown -->
                <div v-if="destinationSuggestions.length > 0" class="mt-1 bg-white border border-gray-300 rounded-md shadow-lg max-h-60 overflow-auto">
                  <div
                    v-for="suggestion in destinationSuggestions"
                    :key="suggestion.id"
                    @click="selectDestinationLocation(suggestion)"
                    class="px-4 py-2 hover:bg-gray-50 cursor-pointer border-b border-gray-100 last:border-b-0"
                  >
                    <div class="font-medium text-gray-900">{{ suggestion.name }}</div>
                    <div class="text-sm text-gray-500">{{ suggestion.address }}</div>
                  </div>
                </div>
              </div>

              <!-- Ride Type Selection -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-3">
                  Choose Ride Type
                </label>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  <div
                    v-for="vehicle in availableVehicles"
                    :key="vehicle.type"
                    @click="selectedVehicleType = vehicle.type"
                    class="relative border rounded-lg p-4 cursor-pointer hover:bg-gray-50 transition-colors"
                    :class="{
                      'border-blue-500 bg-blue-50': selectedVehicleType === vehicle.type,
                      'border-gray-300': selectedVehicleType !== vehicle.type
                    }"
                  >
                    <div class="flex items-center justify-between">
                      <div class="flex items-center">
                        <div class="flex-shrink-0">
                          <div class="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center">
                            <svg class="w-5 h-5 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
                              <path d="M8 16.5a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0zM15 16.5a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0z"/>
                              <path d="M3 4a1 1 0 00-1 1v10a1 1 0 001 1h1.05a2.5 2.5 0 014.9 0H10a1 1 0 001-1V5a1 1 0 00-1-1H3zM14 7a1 1 0 00-1 1v6.05A2.5 2.5 0 0115.95 16H17a1 1 0 001-1V8a1 1 0 00-1-1h-3z"/>
                            </svg>
                          </div>
                        </div>
                        <div class="ml-3">
                          <div class="text-sm font-medium text-gray-900">{{ vehicle.name }}</div>
                          <div class="text-xs text-gray-500">{{ vehicle.description }}</div>
                        </div>
                      </div>
                      <div class="text-right">
                        <div class="text-sm font-medium text-gray-900">₹{{ vehicle.estimatedFare }}</div>
                        <div class="text-xs text-gray-500">{{ vehicle.estimatedTime }}</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Schedule Options -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-3">
                  When do you need this ride?
                </label>
                <div class="flex space-x-4">
                  <label class="flex items-center">
                    <input
                      type="radio"
                      value="now"
                      v-model="scheduleType"
                      class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300"
                    />
                    <span class="ml-2 text-sm text-gray-900">Now</span>
                  </label>
                  <label class="flex items-center">
                    <input
                      type="radio"
                      value="scheduled"
                      v-model="scheduleType"
                      class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300"
                    />
                    <span class="ml-2 text-sm text-gray-900">Schedule for later</span>
                  </label>
                </div>
                
                <div v-if="scheduleType === 'scheduled'" class="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <FormControl
                    label="Date"
                    v-model="scheduledDate"
                    type="date"
                    :min="today"
                  />
                  <FormControl
                    label="Time"
                    v-model="scheduledTime"
                    type="time"
                  />
                </div>
              </div>

              <!-- Action Buttons -->
              <div class="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-4">
                <Button
                  variant="ghost"
                  class="flex-1"
                  @click="$router.push('/')"
                >
                  Cancel
                </Button>
                <Button
                  type="submit"
                  class="flex-1"
                  :disabled="!canSearchRides"
                  :loading="isSearching"
                >
                  Find Rides
                </Button>
              </div>
            </form>
          </Card>
        </div>

        <!-- Map/Preview Section -->
        <div class="space-y-4 md:space-y-6 order-1 lg:order-2">
          <Card class="p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Route Preview</h3>
            
            <!-- Placeholder for map -->
            <div class="bg-gray-100 rounded-lg h-48 md:h-64 flex items-center justify-center">
              <div class="text-center">
                <svg class="w-12 h-12 text-gray-400 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <p class="text-sm text-gray-500">Map will appear here</p>
              </div>
            </div>

            <!-- Trip Summary -->
            <div v-if="selectedPickupCoords && selectedDestinationCoords" class="mt-4 space-y-3">
              <div class="flex items-center justify-between text-sm">
                <span class="text-gray-600">Distance:</span>
                <span class="font-medium">{{ estimatedDistance }} km</span>
              </div>
              <div class="flex items-center justify-between text-sm">
                <span class="text-gray-600">Estimated Time:</span>
                <span class="font-medium">{{ estimatedDuration }} mins</span>
              </div>
              <div class="flex items-center justify-between text-sm">
                <span class="text-gray-600">Estimated Fare:</span>
                <span class="font-medium text-lg">₹{{ estimatedFare }}</span>
              </div>
            </div>
          </Card>

          <!-- Available Drivers -->
          <Card v-if="nearbyDrivers.length > 0" class="p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Nearby Drivers</h3>
            <div class="space-y-3">
              <div
                v-for="driver in nearbyDrivers"
                :key="driver.id"
                class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
              >
                <div class="flex items-center">
                  <Avatar
                    :label="driver.name"
                    size="sm"
                    class="mr-3"
                  />
                  <div>
                    <div class="text-sm font-medium text-gray-900">{{ driver.name }}</div>
                    <div class="text-xs text-gray-500">{{ driver.vehicle }} • {{ driver.rating }}★</div>
                  </div>
                </div>
                <div class="text-right">
                  <div class="text-sm font-medium text-gray-900">{{ driver.distance }} km away</div>
                  <div class="text-xs text-gray-500">{{ driver.estimatedArrival }} mins</div>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { createResource } from 'frappe-ui'

export default {
  name: 'BookRide',
  data() {
    return {
      pickupLocation: '',
      destinationLocation: '',
      selectedPickupCoords: null,
      selectedDestinationCoords: null,
      pickupSuggestions: [],
      destinationSuggestions: [],
      selectedVehicleType: 'standard',
      scheduleType: 'now',
      scheduledDate: '',
      scheduledTime: '',
      isSearching: false,
      estimatedDistance: 0,
      estimatedDuration: 0,
      estimatedFare: 0,
      availableVehicles: [
        {
          type: 'standard',
          name: 'Standard',
          description: 'Affordable rides',
          estimatedFare: 120,
          estimatedTime: '5-8 min'
        },
        {
          type: 'premium',
          name: 'Premium',
          description: 'Comfortable rides',
          estimatedFare: 180,
          estimatedTime: '3-6 min'
        },
        {
          type: 'luxury',
          name: 'Luxury',
          description: 'Premium experience',
          estimatedFare: 250,
          estimatedTime: '5-10 min'
        }
      ],
      nearbyDrivers: []
    }
  },
  computed: {
    today() {
      return new Date().toISOString().split('T')[0]
    },
    canSearchRides() {
      return this.pickupLocation && this.destinationLocation && this.selectedVehicleType
    }
  },
  resources: {
    searchPlaces() {
      return createResource({
        url: '/api/method/drive_now.api.customer.search_places',
        makeParams(query) {
          return { query }
        }
      })
    },
    getFareEstimate() {
      return createResource({
        url: '/api/method/drive_now.api.customer.get_fare_estimate',
        makeParams() {
          return {
            pickup_latitude: this.selectedPickupCoords?.lat,
            pickup_longitude: this.selectedPickupCoords?.lng,
            drop_latitude: this.selectedDestinationCoords?.lat,
            drop_longitude: this.selectedDestinationCoords?.lng,
            vehicle_type: this.selectedVehicleType
          }
        },
        onSuccess(data) {
          if (data.message) {
            this.estimatedDistance = data.message.distance
            this.estimatedDuration = data.message.duration
            this.estimatedFare = data.message.fare
          }
        }
      })
    },
    bookRide() {
      return createResource({
        url: '/api/method/drive_now.api.customer.book_ride',
        makeParams() {
          return {
            pickup_address: this.pickupLocation,
            pickup_latitude: this.selectedPickupCoords?.lat,
            pickup_longitude: this.selectedPickupCoords?.lng,
            drop_off_address: this.destinationLocation,
            drop_off_latitude: this.selectedDestinationCoords?.lat,
            drop_off_longitude: this.selectedDestinationCoords?.lng,
            vehicle_type: this.selectedVehicleType,
            scheduled_time: this.scheduleType === 'scheduled' ? 
              `${this.scheduledDate} ${this.scheduledTime}` : null
          }
        },
        onSuccess(data) {
          console.log('Ride booked successfully:', data)
          this.$router.push('/')
        },
        onError(error) {
          console.error('Failed to book ride:', error)
        }
      })
    }
  },
  methods: {
    async searchPickupLocations() {
      if (this.pickupLocation.length > 2) {
        try {
          const response = await this.$resources.searchPlaces.submit(this.pickupLocation)
          this.pickupSuggestions = response.message || []
        } catch (error) {
          console.error('Error searching pickup locations:', error)
        }
      } else {
        this.pickupSuggestions = []
      }
    },
    async searchDestinationLocations() {
      if (this.destinationLocation.length > 2) {
        try {
          const response = await this.$resources.searchPlaces.submit(this.destinationLocation)
          this.destinationSuggestions = response.message || []
        } catch (error) {
          console.error('Error searching destination locations:', error)
        }
      } else {
        this.destinationSuggestions = []
      }
    },
    selectPickupLocation(location) {
      this.pickupLocation = location.name
      this.selectedPickupCoords = {
        lat: location.latitude,
        lng: location.longitude
      }
      this.pickupSuggestions = []
      this.calculateFareEstimate()
    },
    selectDestinationLocation(location) {
      this.destinationLocation = location.name
      this.selectedDestinationCoords = {
        lat: location.latitude,
        lng: location.longitude
      }
      this.destinationSuggestions = []
      this.calculateFareEstimate()
    },
    async calculateFareEstimate() {
      if (this.selectedPickupCoords && this.selectedDestinationCoords) {
        try {
          await this.$resources.getFareEstimate.submit()
        } catch (error) {
          console.error('Error calculating fare estimate:', error)
        }
      }
    },
    async searchRides() {
      if (!this.canSearchRides) return

      this.isSearching = true
      try {
        await this.$resources.bookRide.submit()
      } finally {
        this.isSearching = false
      }
    }
  },
  watch: {
    selectedVehicleType() {
      this.calculateFareEstimate()
    }
  }
}
</script>