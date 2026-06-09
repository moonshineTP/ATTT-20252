---
name: vue-pinia-best-practices
description: "Use for Pinia stores, state management patterns, store setup, and reactivity with stores. Load when working on game.ts, content.ts, audio.ts stores or adding new Pinia stores."
version: 1.0.0
license: MIT
metadata:
  author: github.com/vuejs-ai (adapted for heritage-game)
---

# Pinia Best Practices — Heritage Game

## Store Setup Pattern (Composition Style — Required)

```typescript
// stores/example.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useExampleStore = defineStore('example', () => {
  // 1. state refs
  const value = ref<string>('')

  // 2. computed (getters)
  const upperValue = computed(() => value.value.toUpperCase())

  // 3. actions
  function setValue(v: string) {
    value.value = v
  }

  // CRITICAL: Return ALL state — missing returns breaks DevTools + SSR
  return { value, upperValue, setValue }
})
```

## Project Stores

| Store | File | Purpose |
|-------|------|---------|
| `useGameStore` | `stores/game.ts` | Phase, score, progress state |
| `useContentStore` | `stores/content.ts` | Fetched `flow.json` data |
| `useAudioStore` | `stores/audio.ts` | BGM + SFX playback state |

## AppPhase Type (game.ts)
```typescript
type AppPhase = 'loading' | 'welcome' | 'prologue' | 'journey1' | 'quiz1' | 'journey2' | 'quiz2' | 'end'
```

## Content Store (stores/content.ts)
```typescript
export const useContentStore = defineStore('content', () => {
  const data = ref<FlowConfig | null>(null)
  const isLoaded = ref(false)

  async function load() {
    const res = await fetch('/flow.json')
    data.value = await res.json()
    isLoaded.value = true
  }

  return { data, isLoaded, load }
})
```

## Common Gotchas

### Store destructuring breaks reactivity
```typescript
// ❌ Wrong — breaks reactivity
const { score } = useGameStore()

// ✅ Correct — use storeToRefs for reactive destructuring
import { storeToRefs } from 'pinia'
const gameStore = useGameStore()
const { score, phase } = storeToRefs(gameStore)
```

### Store method binding in templates
```vue
<!-- ❌ Wrong — loses context -->
<button @click="store.advance">

<!-- ✅ Correct — parentheses required -->
<button @click="store.advance()">
```

### "getActivePinia was called" error
- Always call `app.use(pinia)` before mounting the app in `main.ts`.
- Never call store composables outside Vue component setup or Pinia-aware context.

### Setup stores missing state in DevTools
- Return **every** `ref` and `reactive` from the store factory — not just what you use externally.

## Score Calculation
- Track correct answers per zone: `zone1Score`, `zone2Score`
- Total: `totalScore = zone1Score + zone2Score` (max 6)
- Badge class: determined by total score in `EndView`
