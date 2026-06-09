---
name: vue-testing-best-practices
description: "Use for Vue.js testing. Covers Vitest, Vue Test Utils, component testing, Playwright for E2E testing. Load when writing or fixing test files."
version: 1.0.0
license: MIT
metadata:
  author: github.com/vuejs-ai (adapted for heritage-game)
---

# Vue Testing Best Practices — Heritage Game

## Test Stack
- **Unit/Component**: Vitest + Vue Test Utils
- **E2E**: Playwright (headless Chromium mobile viewport)
- **Coverage**: via Vitest `--coverage`

## Component Testing Patterns

### Setup with Pinia
```typescript
import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import MyComponent from '@/components/MyComponent.vue'

test('renders correctly', () => {
  const wrapper = mount(MyComponent, {
    global: {
      plugins: [createTestingPinia({
        initialState: {
          game: { phase: 'journey1', score: 0 }
        }
      })]
    }
  })
  expect(wrapper.text()).toContain('expected text')
})
```

### Testing async setup components
```typescript
import { flushPromises } from '@vue/test-utils'

test('loads content asynchronously', async () => {
  const wrapper = mount(LoadingView, { /* ... */ })
  await flushPromises()  // Wait for all microtasks
  expect(wrapper.find('.progress-bar').exists()).toBe(true)
})
```

### Testing composables with lifecycle hooks
```typescript
// Wrap in a helper component to access inject/lifecycle
function createComposableWrapper(composable: () => unknown) {
  return defineComponent({
    setup() { return composable() },
    template: '<div />'
  })
}
```

## Playwright E2E Patterns (Mobile Viewport)

```typescript
// playwright.config.ts
export default defineConfig({
  use: {
    viewport: { width: 390, height: 844 },  // iPhone 14 Pro
    deviceScaleFactor: 3,
  }
})
```

```typescript
// tests/e2e/journey.spec.ts
import { test, expect } from '@playwright/test'

test('completes Zone 1 journey', async ({ page }) => {
  await page.goto('/')
  await page.waitForLoadState('networkidle')

  // Loading screen → welcome
  await expect(page.locator('.loading-screen')).toBeVisible()
  await page.waitForURL('/#/welcome', { timeout: 10000 })

  // Swipe through slides
  await page.locator('.story-slide').swipe('left')
})
```

### Touch events in Playwright
```typescript
// Simulate swipe left (go to next slide)
async function swipeLeft(page: Page, selector: string) {
  const el = page.locator(selector)
  const box = await el.boundingBox()
  if (!box) return
  await page.touchscreen.tap(box.x + box.width * 0.8, box.y + box.height / 2)
  await page.mouse.move(box.x + box.width * 0.8, box.y + box.height / 2)
  await page.mouse.down()
  await page.mouse.move(box.x + box.width * 0.2, box.y + box.height / 2)
  await page.mouse.up()
}
```

## What to Test in Heritage Game

| Component/Feature | Test Focus |
|-------------------|-----------|
| `LoadingView` | Progress reaches 100%, navigates to /welcome |
| `WelcomeView` | Curtain animation class applied, CTA button navigates |
| `JourneyView` | Correct slides load for zone=1 vs zone=2, swipe advances slide |
| `QuizView` | Correct answer → score increments, wrong → shake animation, completion → navigation |
| `EndView` | Badge shown, share button triggers Web Share API |
| `useSwipe` | touchstart/touchmove/touchend fires correct callback |
| `useHaptic` | navigator.vibrate called with correct pattern |

## Anti-patterns to Avoid
- ❌ Snapshot-only tests — they pass even when UI is broken
- ❌ Testing implementation details (internal ref values, method names)
- ❌ Not waiting for async operations before asserting
- ✅ Test from the user's perspective: "does this do what the user sees?"
