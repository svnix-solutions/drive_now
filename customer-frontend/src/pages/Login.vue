<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <div class="text-center">
        <h1 class="text-4xl font-bold text-gray-900 mb-2">Drive Now</h1>
        <h2 class="text-2xl font-semibold text-gray-600">Welcome back</h2>
        <p class="mt-2 text-sm text-gray-500">Sign in to your account</p>
      </div>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <Card class="p-8">
        <form @submit.prevent="handleLogin" class="space-y-6">
          <div>
            <FormControl
              label="Email address"
              v-model="email"
              type="email"
              placeholder="Enter your email"
              :required="true"
            />
          </div>

          <div>
            <FormControl
              label="Password"
              v-model="password"
              type="password"
              placeholder="Enter your password"
              :required="true"
            />
          </div>

          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <input
                id="remember-me"
                name="remember-me"
                type="checkbox"
                v-model="rememberMe"
                class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label for="remember-me" class="ml-2 block text-sm text-gray-900">
                Remember me
              </label>
            </div>

            <div class="text-sm">
              <a href="#" class="font-medium text-blue-600 hover:text-blue-500">
                Forgot your password?
              </a>
            </div>
          </div>

          <div>
            <Button
              type="submit"
              class="w-full"
              :loading="isLoggingIn"
            >
              Sign in
            </Button>
          </div>
        </form>

        <div class="mt-6">
          <div class="relative">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-gray-300" />
            </div>
            <div class="relative flex justify-center text-sm">
              <span class="px-2 bg-white text-gray-500">Don't have an account?</span>
            </div>
          </div>

          <div class="mt-6">
            <Button
              variant="ghost"
              class="w-full"
              @click="showRegisterForm = true"
            >
              Create new account
            </Button>
          </div>
        </div>
      </Card>
    </div>

    <!-- Register Dialog -->
    <Dialog
      v-model="showRegisterForm"
      :options="{
        title: 'Create Account',
        size: 'xl'
      }"
    >
      <template #body-content>
        <form @submit.prevent="handleRegister" class="space-y-6">
          <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
            <FormControl
              label="First Name"
              v-model="registerForm.firstName"
              placeholder="Enter your first name"
              :required="true"
            />
            <FormControl
              label="Last Name"
              v-model="registerForm.lastName"
              placeholder="Enter your last name"
              :required="true"
            />
          </div>

          <FormControl
            label="Email address"
            v-model="registerForm.email"
            type="email"
            placeholder="Enter your email"
            :required="true"
          />

          <FormControl
            label="Phone Number"
            v-model="registerForm.phone"
            type="tel"
            placeholder="Enter your phone number"
            :required="true"
          />

          <FormControl
            label="Password"
            v-model="registerForm.password"
            type="password"
            placeholder="Create a password"
            :required="true"
          />

          <FormControl
            label="Confirm Password"
            v-model="registerForm.confirmPassword"
            type="password"
            placeholder="Confirm your password"
            :required="true"
          />

          <div class="flex items-center">
            <input
              id="agree-terms"
              name="agree-terms"
              type="checkbox"
              v-model="registerForm.agreeTerms"
              class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label for="agree-terms" class="ml-2 block text-sm text-gray-900">
              I agree to the 
              <a href="#" class="text-blue-600 hover:text-blue-500">Terms and Conditions</a>
            </label>
          </div>

          <div class="flex space-x-3">
            <Button
              type="button"
              variant="ghost"
              class="flex-1"
              @click="showRegisterForm = false"
            >
              Cancel
            </Button>
            <Button
              type="submit"
              class="flex-1"
              :loading="isRegistering"
              :disabled="!registerForm.agreeTerms"
            >
              Create Account
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
  name: 'Login',
  data() {
    return {
      email: '',
      password: '',
      rememberMe: false,
      isLoggingIn: false,
      showRegisterForm: false,
      isRegistering: false,
      registerForm: {
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        password: '',
        confirmPassword: '',
        agreeTerms: false,
      }
    }
  },
  resources: {
    login() {
      return createResource({
        url: '/api/method/login',
        makeParams() {
          return {
            usr: this.email,
            pwd: this.password,
          }
        },
        onSuccess(data) {
          console.log('Login successful:', data)
          this.$router.push('/')
        },
        onError(error) {
          console.error('Login failed:', error)
          // TODO: Show error message to user
        }
      })
    },
    register() {
      return createResource({
        url: '/api/method/frappe.core.doctype.user.user.sign_up',
        makeParams() {
          return {
            email: this.registerForm.email,
            full_name: `${this.registerForm.firstName} ${this.registerForm.lastName}`,
            password: this.registerForm.password,
          }
        },
        onSuccess(data) {
          console.log('Registration successful:', data)
          this.showRegisterForm = false
          // TODO: Show success message
        },
        onError(error) {
          console.error('Registration failed:', error)
          // TODO: Show error message to user
        }
      })
    }
  },
  methods: {
    async handleLogin() {
      if (!this.email || !this.password) {
        // TODO: Show validation error
        return
      }

      this.isLoggingIn = true
      try {
        await this.$resources.login.submit()
      } finally {
        this.isLoggingIn = false
      }
    },
    async handleRegister() {
      if (!this.validateRegisterForm()) {
        return
      }

      this.isRegistering = true
      try {
        await this.$resources.register.submit()
      } finally {
        this.isRegistering = false
      }
    },
    validateRegisterForm() {
      const { firstName, lastName, email, phone, password, confirmPassword, agreeTerms } = this.registerForm

      if (!firstName || !lastName || !email || !phone || !password || !confirmPassword) {
        // TODO: Show validation error
        return false
      }

      if (password !== confirmPassword) {
        // TODO: Show password mismatch error
        return false
      }

      if (!agreeTerms) {
        // TODO: Show terms agreement error
        return false
      }

      return true
    }
  }
}
</script>