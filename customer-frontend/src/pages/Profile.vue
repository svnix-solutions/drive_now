<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">My Profile</h1>
        <p class="mt-2 text-lg text-gray-600">Manage your account settings</p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Profile Info -->
        <div class="lg:col-span-2 space-y-6">
          <Card class="p-6">
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-xl font-semibold text-gray-900">Personal Information</h2>
              <Button 
                v-if="!isEditing"
                variant="subtle"
                @click="isEditing = true"
              >
                Edit
              </Button>
            </div>

            <form v-if="isEditing" @submit.prevent="updateProfile" class="space-y-6">
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <FormControl
                  label="First Name"
                  v-model="profileForm.firstName"
                  :required="true"
                />
                <FormControl
                  label="Last Name"
                  v-model="profileForm.lastName"
                  :required="true"
                />
              </div>

              <FormControl
                label="Email Address"
                v-model="profileForm.email"
                type="email"
                :required="true"
              />

              <FormControl
                label="Phone Number"
                v-model="profileForm.phone"
                type="tel"
                :required="true"
              />

              <FormControl
                label="Address"
                v-model="profileForm.address"
                placeholder="Enter your address"
              />

              <div class="flex space-x-3">
                <Button
                  type="button"
                  variant="ghost"
                  @click="cancelEdit"
                >
                  Cancel
                </Button>
                <Button
                  type="submit"
                  :loading="isUpdating"
                >
                  Save Changes
                </Button>
              </div>
            </form>

            <div v-else class="space-y-4">
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700">First Name</label>
                  <p class="mt-1 text-sm text-gray-900">{{ userProfile.firstName || 'Not provided' }}</p>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">Last Name</label>
                  <p class="mt-1 text-sm text-gray-900">{{ userProfile.lastName || 'Not provided' }}</p>
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700">Email Address</label>
                <p class="mt-1 text-sm text-gray-900">{{ userProfile.email || 'Not provided' }}</p>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700">Phone Number</label>
                <p class="mt-1 text-sm text-gray-900">{{ userProfile.phone || 'Not provided' }}</p>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700">Address</label>
                <p class="mt-1 text-sm text-gray-900">{{ userProfile.address || 'Not provided' }}</p>
              </div>
            </div>
          </Card>

          <!-- Ride Statistics -->
          <Card class="p-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-6">Ride Statistics</h2>
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div class="text-center">
                <div class="text-2xl font-bold text-gray-900">{{ rideStats.totalRides || 0 }}</div>
                <div class="text-sm text-gray-500">Total Rides</div>
              </div>
              <div class="text-center">
                <div class="text-2xl font-bold text-gray-900">₹{{ rideStats.totalSpent || 0 }}</div>
                <div class="text-sm text-gray-500">Total Spent</div>
              </div>
              <div class="text-center">
                <div class="text-2xl font-bold text-gray-900">{{ rideStats.avgRating || 0 }}★</div>
                <div class="text-sm text-gray-500">Average Rating</div>
              </div>
              <div class="text-center">
                <div class="text-2xl font-bold text-gray-900">{{ rideStats.savedMoney || 0 }}</div>
                <div class="text-sm text-gray-500">CO₂ Saved (kg)</div>
              </div>
            </div>
          </Card>

          <!-- Payment Methods -->
          <Card class="p-6">
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-xl font-semibold text-gray-900">Payment Methods</h2>
              <Button 
                variant="subtle"
                @click="showAddPaymentMethod = true"
              >
                Add Method
              </Button>
            </div>

            <div v-if="paymentMethods.length > 0" class="space-y-4">
              <div
                v-for="method in paymentMethods"
                :key="method.id"
                class="flex items-center justify-between p-4 border border-gray-200 rounded-lg"
              >
                <div class="flex items-center">
                  <div class="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center mr-3">
                    <svg class="w-5 h-5 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M4 4a2 2 0 00-2 2v1h16V6a2 2 0 00-2-2H4z"/>
                      <path fill-rule="evenodd" d="M18 9H2v5a2 2 0 002 2h12a2 2 0 002-2V9zM4 13a1 1 0 011-1h1a1 1 0 110 2H5a1 1 0 01-1-1zm5-1a1 1 0 100 2h1a1 1 0 100-2H9z" clip-rule="evenodd"/>
                    </svg>
                  </div>
                  <div>
                    <div class="text-sm font-medium text-gray-900">
                      {{ method.type === 'card' ? 'Credit Card' : 'UPI' }}
                    </div>
                    <div class="text-sm text-gray-500">{{ method.details }}</div>
                  </div>
                </div>
                <div class="flex items-center space-x-2">
                  <Badge v-if="method.isDefault" label="Default" variant="subtle" />
                  <Button
                    variant="ghost"
                    size="sm"
                    @click="removePaymentMethod(method.id)"
                  >
                    Remove
                  </Button>
                </div>
              </div>
            </div>

            <div v-else class="text-center py-8">
              <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg class="w-8 h-8 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M4 4a2 2 0 00-2 2v1h16V6a2 2 0 00-2-2H4z"/>
                  <path fill-rule="evenodd" d="M18 9H2v5a2 2 0 002 2h12a2 2 0 002-2V9zM4 13a1 1 0 011-1h1a1 1 0 110 2H5a1 1 0 01-1-1zm5-1a1 1 0 100 2h1a1 1 0 100-2H9z" clip-rule="evenodd"/>
                </svg>
              </div>
              <h3 class="text-lg font-medium text-gray-900 mb-2">No payment methods</h3>
              <p class="text-gray-500 mb-4">Add a payment method to book rides easily</p>
            </div>
          </Card>
        </div>

        <!-- Sidebar -->
        <div class="space-y-6">
          <!-- Profile Picture -->
          <Card class="p-6 text-center">
            <Avatar
              :label="userProfile.firstName + ' ' + userProfile.lastName"
              size="xl"
              class="mx-auto mb-4"
            />
            <h3 class="text-lg font-semibold text-gray-900">
              {{ userProfile.firstName }} {{ userProfile.lastName }}
            </h3>
            <p class="text-sm text-gray-500">{{ userProfile.email }}</p>
            <Button
              variant="ghost"
              size="sm"
              class="mt-4"
              @click="changeProfilePicture"
            >
              Change Photo
            </Button>
          </Card>

          <!-- Account Actions -->
          <Card class="p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Account</h3>
            <div class="space-y-3">
              <Button
                variant="ghost"
                class="w-full justify-start"
                @click="showChangePassword = true"
              >
                Change Password
              </Button>
              <Button
                variant="ghost"
                class="w-full justify-start"
                @click="downloadData"
              >
                Download My Data
              </Button>
              <Button
                variant="ghost"
                class="w-full justify-start text-red-600 hover:text-red-700"
                @click="showDeleteAccount = true"
              >
                Delete Account
              </Button>
            </div>
          </Card>
        </div>
      </div>
    </div>

    <!-- Add Payment Method Dialog -->
    <Dialog
      v-model="showAddPaymentMethod"
      :options="{ title: 'Add Payment Method', size: 'lg' }"
    >
      <template #body-content>
        <!-- Payment method form would go here -->
        <div class="text-center py-8">
          <p class="text-gray-500">Payment method integration coming soon...</p>
        </div>
      </template>
    </Dialog>

    <!-- Change Password Dialog -->
    <Dialog
      v-model="showChangePassword"
      :options="{ title: 'Change Password', size: 'lg' }"
    >
      <template #body-content>
        <form @submit.prevent="changePassword" class="space-y-6">
          <FormControl
            label="Current Password"
            v-model="passwordForm.currentPassword"
            type="password"
            :required="true"
          />
          <FormControl
            label="New Password"
            v-model="passwordForm.newPassword"
            type="password"
            :required="true"
          />
          <FormControl
            label="Confirm New Password"
            v-model="passwordForm.confirmPassword"
            type="password"
            :required="true"
          />
          <div class="flex space-x-3">
            <Button
              type="button"
              variant="ghost"
              class="flex-1"
              @click="showChangePassword = false"
            >
              Cancel
            </Button>
            <Button
              type="submit"
              class="flex-1"
              :loading="isChangingPassword"
            >
              Change Password
            </Button>
          </div>
        </form>
      </template>
    </Dialog>
  </div>
</template>

<script>
import { createResource } from 'frappe-ui'

export default {
  name: 'Profile',
  data() {
    return {
      isEditing: false,
      isUpdating: false,
      isChangingPassword: false,
      showAddPaymentMethod: false,
      showChangePassword: false,
      showDeleteAccount: false,
      userProfile: {
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        address: ''
      },
      profileForm: {
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        address: ''
      },
      passwordForm: {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      },
      rideStats: {
        totalRides: 0,
        totalSpent: 0,
        avgRating: 0,
        savedMoney: 0
      },
      paymentMethods: []
    }
  },
  resources: {
    userProfile() {
      return createResource({
        url: '/api/method/drive_now.api.customer.get_profile',
        auto: true,
        onSuccess(data) {
          if (data.message) {
            this.userProfile = data.message
            this.rideStats = data.message.stats || {}
          }
        }
      })
    },
    paymentMethods() {
      return createResource({
        url: '/api/method/drive_now.api.customer.get_payment_methods',
        auto: true,
        onSuccess(data) {
          this.paymentMethods = data.message || []
        }
      })
    },
    updateProfile() {
      return createResource({
        url: '/api/method/drive_now.api.customer.update_profile',
        makeParams() {
          return this.profileForm
        },
        onSuccess(data) {
          this.userProfile = { ...this.userProfile, ...this.profileForm }
          this.isEditing = false
          // TODO: Show success message
        },
        onError(error) {
          console.error('Failed to update profile:', error)
          // TODO: Show error message
        }
      })
    }
  },
  methods: {
    cancelEdit() {
      this.profileForm = { ...this.userProfile }
      this.isEditing = false
    },
    async updateProfile() {
      this.isUpdating = true
      try {
        await this.$resources.updateProfile.submit()
      } finally {
        this.isUpdating = false
      }
    },
    async changePassword() {
      if (this.passwordForm.newPassword !== this.passwordForm.confirmPassword) {
        // TODO: Show password mismatch error
        return
      }

      this.isChangingPassword = true
      try {
        // TODO: Implement change password API call
        console.log('Changing password...')
        this.showChangePassword = false
        this.passwordForm = {
          currentPassword: '',
          newPassword: '',
          confirmPassword: ''
        }
      } finally {
        this.isChangingPassword = false
      }
    },
    changeProfilePicture() {
      // TODO: Implement profile picture change
      console.log('Change profile picture')
    },
    removePaymentMethod(methodId) {
      if (confirm('Are you sure you want to remove this payment method?')) {
        // TODO: Implement remove payment method
        console.log('Remove payment method:', methodId)
      }
    },
    downloadData() {
      // TODO: Implement data download
      console.log('Download user data')
    }
  },
  watch: {
    userProfile: {
      handler(newProfile) {
        this.profileForm = { ...newProfile }
      },
      immediate: true,
      deep: true
    }
  }
}
</script>