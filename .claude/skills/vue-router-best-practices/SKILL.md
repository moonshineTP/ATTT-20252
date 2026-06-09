---
name: vue-router-best-practices
description: "Vue Router 4 patterns, navigation guards, route params, and route-component lifecycle. Load when working on router/index.ts or any view that reads route.query.zone."
version: 1.0.0
license: MIT
metadata:
  author: github.com/vuejs-ai (adapted for heritage-game)
---

# Vue Router Best Practices — Heritage Game

## Routing Architecture

```
createWebHashHistory()  ← required for QR-link + PWA compatibility

/                     → LoadingView  (auto-advance after preload)
/#/welcome            → WelcomeView  (Intro + Curtain + Prologue)
/#/hub                → HubView      (Central node — zone selection)
/#/journey?zone=zone1 → JourneyView  (Zone 1–7 story slides)
/#/checkpoint?zone=X  → CheckpointView (Pre-quiz gate + note review)
/#/quiz?zone=zone1    → QuizView     (MCQ / Cloze quiz)
/#/memorial           → MemorialView (Card flip — gated ≥3 zones)
/#/badge              → BadgeView    (Assembly animation)
/#/end                → EndView      (Epilogue + Credits + Share)
```

## Reading Zone Query Param (required pattern)

```typescript
// In JourneyView.vue, CheckpointView.vue, QuizView.vue
import { useRoute, useRouter } from 'vue-router'
import { computed } from 'vue'

const route = useRoute()
const router = useRouter()

// Typed zone param — always validate
const zoneId = computed(() => route.query.zone as string)
```

## Navigation After Quiz Completion

```typescript
function onQuizComplete() {
  // All zones return to hub after quiz
  router.replace({ name: 'hub' })
}
```

## Navigation Guards (router/index.ts)

```typescript
// Hub-based whitelist — 6 event zones always open from hub
// Zone 7 + memorial gated by isUnlocked (≥3 completed)
// Direct URL access allowed for onboarded users
```

## Common Gotchas

### Stale data when navigating same route with different params
```typescript
// ❌ Wrong — lifecycle hooks don't re-run for same route with different query
// ✅ Correct — watch the zone param
watch(zoneId, (newZone) => {
  loadZoneContent(newZone)
}, { immediate: true })
```

### Navigation guard params change not triggering
- `beforeRouteEnter` does NOT trigger when only query params change on the same route.
- Use `watch(() => route.query.zone, ...)` inside the component instead.

### Async navigation guard pattern
```typescript
router.beforeEach(async (to, from) => {
  // Always await async operations
  await someAsyncCheck()
  return true  // explicitly return true to confirm navigation
})
```

### Infinite redirect loops
- Always check `to.path !== from.path` before redirecting in guards.
- Never redirect from '/' back to '/' unconditionally.

## Route Cleanup
- Remove event listeners and cancel async operations in `onUnmounted()`.
- Use `watch` cleanup functions for observers started on route entry.
