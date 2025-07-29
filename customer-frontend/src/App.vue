<template>
  <div class="h-screen bg-gray-50">
    <!-- Navigation Header -->
    <nav v-if="!isLoginPage" class="bg-white shadow-sm border-b sticky top-0 z-40">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <h1 class="text-lg md:text-xl font-semibold text-gray-900">Drive Now</h1>
            </div>
          </div>
          
          <!-- Mobile menu button -->
          <div class="flex items-center md:hidden">
            <button
              @click="mobileMenuOpen = !mobileMenuOpen"
              class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500"
            >
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          
          <!-- Desktop navigation -->
          <div class="hidden md:flex md:items-center md:space-x-4">
            <router-link
              v-for="item in navigation"
              :key="item.name"
              :to="item.to"
              class="text-gray-500 hover:text-gray-700 px-3 py-2 rounded-md text-sm font-medium"
              :class="{ 'text-blue-600 bg-blue-50': $route.name === item.name }"
            >
              {{ item.label }}
            </router-link>
            
            <!-- PWA Install Button -->
            <Button
              v-if="showInstallButton"
              @click="installPWA"
              size="sm"
              variant="outline"
              class="ml-2"
            >
              Install App
            </Button>
            
            <Dropdown
              :options="profileMenuOptions"
              class="ml-3"
            >
              <template #default="{ open }">
                <Avatar
                  size="sm"
                  label="User"
                  class="cursor-pointer"
                />
              </template>
            </Dropdown>
          </div>
        </div>
      </div>
      
      <!-- Mobile menu -->
      <div v-if="mobileMenuOpen" class="md:hidden">
        <div class="px-2 pt-2 pb-3 space-y-1">
          <router-link
            v-for="item in navigation"
            :key="item.name"
            :to="item.to"
            @click="mobileMenuOpen = false"
            class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50"
            :class="{ 'bg-blue-50 text-blue-600': $route.name === item.name }"
          >
            {{ item.label }}
          </router-link>
          
          <!-- PWA Install Button Mobile -->
          <Button
            v-if="showInstallButton"
            @click="installPWA"
            size="sm"
            variant="outline"
            class="w-full mt-2"
          >
            Install App
          </Button>
          
          <hr class="my-2">
          
          <button
            @click="() => { $router.push('/profile'); mobileMenuOpen = false; }"
            class="block w-full text-left px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50"
          >
            Profile
          </button>
          <button
            @click="() => { $router.push('/login'); mobileMenuOpen = false; }"
            class="block w-full text-left px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50"
          >
            Logout
          </button>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="flex-1">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      showInstallButton: false,
      mobileMenuOpen: false,
    }
  },
  mounted() {
    // Listen for PWA install availability
    window.addEventListener('pwa-install-available', () => {
      this.showInstallButton = true
    })
    
    // Hide install button after installation
    window.addEventListener('appinstalled', () => {
      this.showInstallButton = false
    })
  },
  computed: {
    isLoginPage() {
      return this.$route.name === 'Login'
    },
    navigation() {
      return [
        { name: 'Dashboard', label: 'Dashboard', to: '/' },
        { name: 'BookRide', label: 'Book Ride', to: '/book-ride' },
        { name: 'RideHistory', label: 'History', to: '/ride-history' },
        { name: 'Profile', label: 'Profile', to: '/profile' },
      ]
    },
    profileMenuOptions() {
      return [
        {
          label: 'Profile',
          onClick: () => this.$router.push('/profile'),
        },
        {
          label: 'Logout',
          onClick: () => {
            // TODO: Implement logout logic
            this.$router.push('/login')
          },
        },
      ]
    },
  },
  methods: {
    installPWA() {
      if (window.showInstallPrompt) {
        window.showInstallPrompt()
      }
    },
  },
}
</script>
