import './index.css'

import { createApp } from 'vue'
import router from './router'
import App from './App.vue'
import FormControl from './components/FormControl.vue'

import { 
  Button, 
  Input, 
  Card,
  Badge, 
  Dialog,
  Avatar,
  Dropdown,
  LoadingIndicator,
  setConfig, 
  frappeRequest, 
  resourcesPlugin 
} from 'frappe-ui'

let app = createApp(App)

setConfig('resourceFetcher', frappeRequest)

app.use(router)
app.use(resourcesPlugin)

// Register commonly used Frappe UI components globally
app.component('Button', Button)
app.component('Input', Input)
app.component('FormControl', FormControl)
app.component('Card', Card)
app.component('Badge', Badge)
app.component('Dialog', Dialog)
app.component('Avatar', Avatar)
app.component('Dropdown', Dropdown)
app.component('LoadingIndicator', LoadingIndicator)
app.mount('#app')

// Register Service Worker for PWA
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/assets/drive_now/frontend/sw.js')
      .then(registration => {
        console.log('Service Worker registered:', registration)
        
        // Check for updates periodically
        setInterval(() => {
          registration.update()
        }, 60000) // Check every minute
      })
      .catch(error => {
        console.error('Service Worker registration failed:', error)
      })
  })
}

// PWA Install Prompt
let deferredPrompt
window.addEventListener('beforeinstallprompt', (e) => {
  // Prevent Chrome 67 and earlier from automatically showing the prompt
  e.preventDefault()
  // Stash the event so it can be triggered later
  deferredPrompt = e
  // Update UI to show install button
  window.dispatchEvent(new Event('pwa-install-available'))
})

// Make install prompt available globally
window.showInstallPrompt = () => {
  if (deferredPrompt) {
    deferredPrompt.prompt()
    deferredPrompt.userChoice.then((choiceResult) => {
      if (choiceResult.outcome === 'accepted') {
        console.log('User accepted the install prompt')
      } else {
        console.log('User dismissed the install prompt')
      }
      deferredPrompt = null
    })
  }
}
