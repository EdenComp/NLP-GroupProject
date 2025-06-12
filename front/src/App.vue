<script setup lang="ts">
import { ref } from 'vue'
import confetti from 'canvas-confetti'
import { getPath } from './services/api'

const githubUser1 = ref('')
const githubUser2 = ref('')
const handshakeChain = ref<string[]>([])
const isLoading = ref(false)
const errorMessage = ref('')

async function processHandshake() {
  if (githubUser1.value && githubUser2.value) {
    isLoading.value = true
    errorMessage.value = ''

    try {
      const path = await getPath(githubUser1.value, githubUser2.value)
      handshakeChain.value = path

      confetti({
        particleCount: 150,
        spread: 90,
        origin: { y: 0.6 }
      })
    } catch (error) {
      console.error(error)
      errorMessage.value = error instanceof Error ? error.message : 'Failed to fetch path data'
      handshakeChain.value = []
    } finally {
      isLoading.value = false
    }
  }
}

function getAvatarUrl(username: string): string {
  return `https://github.com/${username}.png`
}
</script>

<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-indigo-100 via-sky-100 to-white px-4">

    <div class="flex gap-8 items-center justify-center mb-10">
      <img
        src="/CAULogo.png"
        alt="CAU Logo"
        class="h-16 hover:scale-105 transition-transform duration-300"
      />
      <img
        src="/EpitechLogo.png"
        alt="Epitech Logo"
        class="h-12 hover:scale-105 transition-transform duration-300"
      />
    </div>

    <div class="w-full max-w-5xl text-center space-y-10">
      <h1 class="text-5xl font-extrabold text-gray-800 tracking-tight">GitHub Handshake</h1>

      <div class="flex flex-col md:flex-row justify-center gap-6">
        <input
          v-model="githubUser1"
          type="text"
          placeholder="GitHub username 1"
          class="flex-1 min-w-0 px-5 py-3 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-400 text-lg transition"
        />
        <input
          v-model="githubUser2"
          type="text"
          placeholder="GitHub username 2"
          class="flex-1 min-w-0 px-5 py-3 border border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-400 text-lg transition"
        />
      </div>

      <button
        @click="processHandshake"
        :disabled="isLoading || !githubUser1 || !githubUser2"
        class="mt-2 px-8 py-3 bg-indigo-600 text-white font-semibold rounded-xl shadow-md hover:bg-indigo-700 active:scale-95 transition text-lg disabled:bg-gray-400 disabled:cursor-not-allowed"
      >
        <span v-if="isLoading">⏳ Processing...</span>
        <span v-else>🔍 Process</span>
      </button>

      <div v-if="errorMessage" class="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded-xl">
        {{ errorMessage }}
      </div>

      <div v-if="handshakeChain.length" class="space-y-8 mt-8">
        <div class="flex flex-wrap justify-center items-center gap-4">
          <template v-for="(user, index) in handshakeChain" :key="index">
            <a
              :href="`https://github.com/${user}`"
              target="_blank"
              class="group flex items-center space-x-3 px-5 py-2 bg-white rounded-full shadow-md text-gray-700 font-medium hover:shadow-lg transition transform hover:scale-105 hover:-translate-y-1"
            >
              <img
                :src="getAvatarUrl(user)"
                alt="avatar"
                class="w-9 h-9 rounded-full object-cover border border-gray-200 group-hover:border-indigo-400 transition"
              />
              <span class="text-lg">{{ user }}</span>
            </a>
            <span v-if="index < handshakeChain.length - 1" class="text-2xl text-gray-500">➝</span>
          </template>
        </div>

        <p class="text-gray-600 text-xl">
          You are <span class="font-semibold text-indigo-700">{{ handshakeChain.length - 2 }}</span>
          handshakes away from each other.
        </p>
      </div>
    </div>
  </div>
</template>
