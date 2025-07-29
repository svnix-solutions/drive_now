<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Ride History</h1>
        <p class="mt-2 text-lg text-gray-600">View all your past rides</p>
      </div>

      <!-- Filters -->
      <Card class="p-6 mb-8">
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <FormControl
            label="Status"
            type="select"
            v-model="filters.status"
            :options="statusOptions"
            @change="applyFilters"
          />
          <FormControl
            label="From Date"
            type="date"
            v-model="filters.fromDate"
            @change="applyFilters"
          />
          <FormControl
            label="To Date"
            type="date"
            v-model="filters.toDate"
            @change="applyFilters"
          />
          <div class="flex items-end">
            <Button
              variant="ghost"
              @click="clearFilters"
              class="w-full"
            >
              Clear Filters
            </Button>
          </div>
        </div>
      </Card>

      <!-- Ride List -->
      <div v-if="isLoading" class="text-center py-12">
        <LoadingIndicator />
        <p class="mt-4 text-gray-500">Loading your rides...</p>
      </div>

      <div v-else-if="rides.length > 0" class="space-y-6">
        <Card
          v-for="ride in rides"
          :key="ride.name"
          class="p-6 hover:shadow-lg transition-shadow"
        >
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <div class="flex items-center justify-between mb-4">
                <div class="flex items-center space-x-4">
                  <Badge 
                    :variant="getRideStatusVariant(ride.status)"
                    :label="ride.status"
                  />
                  <span class="text-sm text-gray-500">
                    {{ formatDate(ride.creation) }}
                  </span>
                </div>
                <div class="text-right">
                  <div class="text-lg font-semibold text-gray-900">₹{{ ride.total_amount }}</div>
                  <div class="text-sm text-gray-500">{{ ride.vehicle_type }}</div>
                </div>
              </div>

              <div class="space-y-3">
                <div class="flex items-start">
                  <div class="flex-shrink-0 w-6 flex flex-col items-center">
                    <div class="w-3 h-3 bg-green-500 rounded-full"></div>
                    <div class="w-0.5 h-8 bg-gray-300 mt-1"></div>
                  </div>
                  <div class="ml-3 flex-1">
                    <div class="text-sm font-medium text-gray-900">Pickup</div>
                    <div class="text-sm text-gray-600">{{ ride.pickup_address }}</div>
                    <div class="text-xs text-gray-500">{{ formatTime(ride.pickup_time) }}</div>
                  </div>
                </div>

                <div class="flex items-start">
                  <div class="flex-shrink-0 w-6 flex flex-col items-center">
                    <div class="w-3 h-3 bg-red-500 rounded-full"></div>
                  </div>
                  <div class="ml-3 flex-1">
                    <div class="text-sm font-medium text-gray-900">Drop-off</div>
                    <div class="text-sm text-gray-600">{{ ride.drop_off_address }}</div>
                    <div class="text-xs text-gray-500">{{ formatTime(ride.drop_off_time) }}</div>
                  </div>
                </div>
              </div>

              <!-- Driver Info -->
              <div v-if="ride.driver_name" class="mt-4 flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                <Avatar
                  :label="ride.driver_name"
                  size="sm"
                />
                <div>
                  <div class="text-sm font-medium text-gray-900">{{ ride.driver_name }}</div>
                  <div class="text-xs text-gray-500">{{ ride.driver_phone }}</div>
                </div>
                <div class="ml-auto">
                  <div class="flex items-center text-xs text-gray-500">
                    <svg class="w-3 h-3 text-yellow-400 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                    </svg>
                    {{ ride.driver_rating || 'N/A' }}
                  </div>
                </div>
              </div>

              <!-- Action Buttons -->
              <div class="mt-4 flex items-center space-x-3">
                <Button
                  variant="ghost"
                  size="sm"
                  @click="viewRideDetails(ride)"
                >
                  View Details
                </Button>
                <Button
                  v-if="ride.status === 'Completed' && !ride.rating"
                  variant="subtle"
                  size="sm"
                  @click="rateRide(ride)"
                >
                  Rate Ride
                </Button>
                <Button
                  v-if="ride.status === 'In Progress'"
                  variant="subtle"
                  size="sm"
                  @click="trackRide(ride.name)"
                >
                  Track Ride
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  @click="bookAgain(ride)"
                >
                  Book Again
                </Button>
              </div>
            </div>
          </div>
        </Card>

        <!-- Load More Button -->
        <div v-if="hasMore" class="text-center">
          <Button
            variant="ghost"
            @click="loadMore"
            :loading="isLoadingMore"
          >
            Load More Rides
          </Button>
        </div>
      </div>

      <div v-else class="text-center py-12">
        <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </div>
        <h3 class="text-lg font-medium text-gray-900 mb-2">No rides found</h3>
        <p class="text-gray-500 mb-4">You haven't taken any rides yet</p>
        <Button @click="$router.push('/book-ride')">
          Book Your First Ride
        </Button>
      </div>
    </div>

    <!-- Ride Details Dialog -->
    <Dialog
      v-model="showRideDetails"
      :options="{ title: 'Ride Details', size: 'xl' }"
    >
      <template #body-content>
        <div v-if="selectedRide" class="space-y-6">
          <!-- Ride Summary -->
          <div class="bg-gray-50 p-4 rounded-lg">
            <div class="flex items-center justify-between mb-2">
              <Badge 
                :variant="getRideStatusVariant(selectedRide.status)"
                :label="selectedRide.status"
              />
              <span class="text-lg font-semibold">₹{{ selectedRide.total_amount }}</span>
            </div>
            <div class="text-sm text-gray-600">
              {{ formatDate(selectedRide.creation) }}
            </div>
          </div>

          <!-- Route Details -->
          <div class="space-y-4">
            <h4 class="font-medium text-gray-900">Route Details</h4>
            <div class="space-y-3">
              <div class="flex items-start">
                <div class="flex-shrink-0 w-6 flex flex-col items-center">
                  <div class="w-3 h-3 bg-green-500 rounded-full"></div>
                  <div class="w-0.5 h-8 bg-gray-300 mt-1"></div>
                </div>
                <div class="ml-3">
                  <div class="text-sm font-medium text-gray-900">{{ selectedRide.pickup_address }}</div>
                  <div class="text-xs text-gray-500">{{ formatTime(selectedRide.pickup_time) }}</div>
                </div>
              </div>
              <div class="flex items-start">
                <div class="flex-shrink-0 w-6 flex flex-col items-center">
                  <div class="w-3 h-3 bg-red-500 rounded-full"></div>
                </div>
                <div class="ml-3">
                  <div class="text-sm font-medium text-gray-900">{{ selectedRide.drop_off_address }}</div>
                  <div class="text-xs text-gray-500">{{ formatTime(selectedRide.drop_off_time) }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Fare Breakdown -->
          <div class="space-y-3">
            <h4 class="font-medium text-gray-900">Fare Breakdown</h4>
            <div class="space-y-2 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-600">Base fare</span>
                <span>₹{{ selectedRide.base_fare }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">Distance ({{ selectedRide.distance }} km)</span>
                <span>₹{{ selectedRide.distance_fare }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">Time ({{ selectedRide.duration }} min)</span>
                <span>₹{{ selectedRide.time_fare }}</span>
              </div>
              <div class="border-t pt-2 flex justify-between font-medium">
                <span>Total</span>
                <span>₹{{ selectedRide.total_amount }}</span>
              </div>
            </div>
          </div>
        </div>
      </template>
    </Dialog>

    <!-- Rate Ride Dialog -->
    <Dialog
      v-model="showRatingDialog"
      :options="{ title: 'Rate Your Ride', size: 'lg' }"
    >
      <template #body-content>
        <div v-if="rideToRate" class="text-center space-y-6">
          <div>
            <Avatar
              :label="rideToRate.driver_name"
              size="xl"
              class="mx-auto mb-4"
            />
            <h3 class="text-lg font-semibold text-gray-900">{{ rideToRate.driver_name }}</h3>
            <p class="text-sm text-gray-500">How was your ride?</p>
          </div>

          <div class="flex justify-center space-x-2">
            <button
              v-for="star in 5"
              :key="star"
              @click="rating = star"
              class="p-1"
            >
              <svg
                class="w-8 h-8"
                :class="star <= rating ? 'text-yellow-400' : 'text-gray-300'"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
              </svg>
            </button>
          </div>

          <FormControl
            label="Feedback (Optional)"
            v-model="feedback"
            type="textarea"
            placeholder="Tell us about your experience..."
            :rows="3"
          />

          <div class="flex space-x-3">
            <Button
              variant="ghost"
              class="flex-1"
              @click="showRatingDialog = false"
            >
              Skip
            </Button>
            <Button
              class="flex-1"
              :disabled="rating === 0"
              :loading="isSubmittingRating"
              @click="submitRating"
            >
              Submit Rating
            </Button>
          </div>
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script>
import { createResource } from 'frappe-ui'

export default {
  name: 'RideHistory',
  data() {
    return {
      rides: [],
      isLoading: false,
      isLoadingMore: false,
      hasMore: true,
      showRideDetails: false,
      selectedRide: null,
      showRatingDialog: false,
      rideToRate: null,
      rating: 0,
      feedback: '',
      isSubmittingRating: false,
      filters: {
        status: '',
        fromDate: '',
        toDate: ''
      },
      statusOptions: [
        { label: 'All', value: '' },
        { label: 'Completed', value: 'Completed' },
        { label: 'Cancelled', value: 'Cancelled' },
        { label: 'In Progress', value: 'In Progress' }
      ]
    }
  },
  resources: {
    rides() {
      return createResource({
        url: '/api/method/drive_now.api.customer.get_ride_history',
        makeParams() {
          return {
            ...this.filters,
            limit: 20,
            start: 0
          }
        },
        auto: true,
        onSuccess(data) {
          this.rides = data.message || []
          this.hasMore = (data.message || []).length === 20
        }
      })
    },
    submitRideRating() {
      return createResource({
        url: '/api/method/drive_now.api.customer.rate_ride',
        makeParams() {
          return {
            ride_id: this.rideToRate.name,
            rating: this.rating,
            feedback: this.feedback
          }
        },
        onSuccess() {
          this.showRatingDialog = false
          this.rating = 0
          this.feedback = ''
          this.rideToRate = null
          // Refresh rides list
          this.$resources.rides.reload()
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
    formatTime(timeString) {
      if (!timeString) return 'N/A'
      return new Date(timeString).toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
      })
    },
    applyFilters() {
      this.$resources.rides.reload()
    },
    clearFilters() {
      this.filters = {
        status: '',
        fromDate: '',
        toDate: ''
      }
      this.applyFilters()
    },
    loadMore() {
      // TODO: Implement pagination
      console.log('Load more rides')
    },
    viewRideDetails(ride) {
      this.selectedRide = ride
      this.showRideDetails = true
    },
    rateRide(ride) {
      this.rideToRate = ride
      this.showRatingDialog = true
    },
    async submitRating() {
      if (this.rating === 0) return

      this.isSubmittingRating = true
      try {
        await this.$resources.submitRideRating.submit()
      } finally {
        this.isSubmittingRating = false
      }
    },
    trackRide(rideId) {
      this.$router.push(`/ride-tracking/${rideId}`)
    },
    bookAgain(ride) {
      // Navigate to book ride page with pre-filled data
      this.$router.push({
        path: '/book-ride',
        query: {
          pickup: ride.pickup_address,
          destination: ride.drop_off_address,
          vehicleType: ride.vehicle_type
        }
      })
    }
  }
}
</script>