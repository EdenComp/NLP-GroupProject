const API_BASE_URL = import.meta.env.PROD ? (import.meta.env.VITE_API_URL || 'http://localhost:5000') : '/api'

export type PathResponse = {
  path: string[]
}

export async function getPath(user1: string, user2: string): Promise<string[]> {
  const response = await fetch(`${API_BASE_URL}/path/${user1}/${user2}`)
  
  if (!response.ok) {
    throw new Error(`API request failed: ${response.status} ${response.statusText}`)
  }
  
  const data: PathResponse = await response.json()
  return data.path
}